// /api/track-click.js
// Beacon target from /pixel.js. Upserts an attribution row in public.visits
// keyed on (visitor_id, landing_path). One row per visitor per landing page;
// subsequent pageviews update last_seen_at + pageview_count.

function pickNiche(path) {
  const p = (path || "").toLowerCase();
  if (p.includes("dental"))   return "dental";
  if (p.includes("medspa") || p.includes("skin") || p.includes("injectable")) return "medspa";
  if (p.includes("plumb") || p.includes("trades") || p.includes("hvac")) return "plumbing";
  return null;
}

function getCookie(req, name) {
  const cookie = req.headers.cookie || "";
  const match = cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
  return match ? decodeURIComponent(match[1]) : undefined;
}

async function upsertVisit(row) {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) return { skipped: true };

  // First try insert; on 409 conflict, update last_seen_at + bump pageview_count.
  // Postgres on_conflict via PostgREST: Prefer: resolution=merge-duplicates with the unique constraint.
  const r = await fetch(`${url}/rest/v1/visits?on_conflict=visitor_id,landing_path`, {
    method: "POST",
    headers: {
      apikey: key,
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
      Prefer: "resolution=merge-duplicates,return=minimal",
    },
    body: JSON.stringify([row]),
  });
  if (!r.ok) {
    const body = await r.json().catch(() => ({}));
    console.error("[track-click] supabase upsert failed " + JSON.stringify({ status: r.status, body }));
  }
  return { ok: r.ok, status: r.status };
}

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method === "GET") {
    return res.status(200).json({
      ok: true,
      message: "Click + campaign attribution endpoint. /pixel.js beacons land here.",
      env: { supabase: !!process.env.SUPABASE_URL && !!process.env.SUPABASE_SERVICE_ROLE_KEY },
    });
  }
  if (req.method !== "POST") return res.status(405).end();

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch { body = {}; } }
  body = body || {};

  // Required: visitor_id + landing_path. Skip if missing.
  if (!body.visitor_id || !body.landing_path) {
    return res.status(200).json({ skipped: true, reason: "missing visitor_id or landing_path" });
  }

  // Server-side fbc/fbp from cookies (browser may not have hashed them into the beacon)
  const fbc = body.fbc || getCookie(req, "_fbc");
  const fbp = body.fbp || getCookie(req, "_fbp");

  const row = {
    visitor_id:    body.visitor_id,
    fbclid:        body.fbclid    || null,
    fbc:           fbc            || null,
    fbp:           fbp            || null,
    gclid:         body.gclid     || null,
    ttclid:        body.ttclid    || null,
    msclkid:       body.msclkid   || null,
    utm_source:    body.utm_source   || null,
    utm_medium:    body.utm_medium   || null,
    utm_campaign:  body.utm_campaign || null,
    utm_content:   body.utm_content  || null,
    utm_term:      body.utm_term     || null,
    utm_id:        body.utm_id       || null,
    landing_path:  body.landing_path,
    niche:         body.niche || pickNiche(body.landing_path),
    referrer:      body.referrer || req.headers.referer || null,
    user_agent:    req.headers["user-agent"] || null,
    ip_address:    req.headers["x-forwarded-for"]?.split(",")[0]?.trim() || req.headers["x-real-ip"] || null,
    country:       (req.headers["x-vercel-ip-country"] || "AU").toUpperCase(),
    last_seen_at:  new Date().toISOString(),
  };

  const result = await upsertVisit(row);
  return res.status(200).json({ ok: !!result.ok, visitor_id: body.visitor_id });
}

export const config = { runtime: "nodejs" };
