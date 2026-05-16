// /api/iclosed-slack.js
// Receives iClosed booking webhook. Logs the booking row in Supabase, pings Slack
// (#leads-booked or fallback to qualified webhook), and fires a Meta CAPI "Schedule" event
// for the booking. Optionally triggers Retell outbound (left as a stub flag).
//
// Designed to be set as the iClosed webhook URL: https://answerra.ai/api/iclosed-slack

import crypto from "node:crypto";

const PIXEL_ID = process.env.PIXEL_ID || "1511657447261837";
const META_API_VERSION = "v19.0";

function sha256(input) {
  if (!input) return undefined;
  return crypto.createHash("sha256").update(String(input).trim().toLowerCase()).digest("hex");
}
function normalisePhone(p) {
  if (!p) return undefined;
  const d = String(p).replace(/\D/g, "");
  if (!d) return undefined;
  if (d.startsWith("0") && d.length === 10) return "61" + d.slice(1);
  if (d.startsWith("61")) return d;
  return d;
}

async function supabaseUpsertBooking(row) {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) return { skipped: true };
  const r = await fetch(`${url}/rest/v1/bookings?on_conflict=booking_id`, {
    method: "POST",
    headers: {
      apikey: key,
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
      Prefer: "resolution=merge-duplicates,return=representation",
    },
    body: JSON.stringify([row]),
  });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) console.error("[iclosed-slack] supabase upsert failed " + JSON.stringify({ status: r.status, body }));
  return { ok: r.ok, status: r.status, body };
}

async function slackPost(text) {
  const url = process.env.SLACK_BOOKED_WEBHOOK || process.env.SLACK_QUALIFIED_WEBHOOK;
  if (!url) return { skipped: true };
  try {
    const r = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text, mrkdwn: true }) });
    return { ok: r.ok };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

async function fireCapiSchedule({ event_id, email, phone, first_name, niche, source_url, client_ip, client_ua }) {
  const token = process.env.META_CAPI_ACCESS_TOKEN;
  if (!token) return { skipped: true, reason: "no_token" };
  const user_data = { country: [sha256("au")] };
  if (email) user_data.em = [sha256(email)];
  if (phone) user_data.ph = [sha256(normalisePhone(phone))];
  if (first_name) user_data.fn = [sha256(first_name)];
  if (client_ip) user_data.client_ip_address = client_ip;
  if (client_ua) user_data.client_user_agent = client_ua;
  const payload = {
    data: [{
      event_name: "Schedule",
      event_time: Math.floor(Date.now() / 1000),
      event_id,
      action_source: "website",
      event_source_url: source_url || "https://answerra.ai",
      user_data,
      custom_data: { content_name: "Answerra Build Call Booked", niche }
    }]
  };
  try {
    const r = await fetch(
      `https://graph.facebook.com/${META_API_VERSION}/${PIXEL_ID}/events?access_token=${encodeURIComponent(token)}`,
      { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }
    );
    return { ok: r.ok, status: r.status };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

function pickNiche(payload) {
  const t = (payload.event_type || payload.event_name || payload.calendar_name || "").toLowerCase();
  if (t.includes("dental")) return "dental";
  if (t.includes("medspa") || t.includes("skin") || t.includes("injectable")) return "medspa";
  if (t.includes("plumb") || t.includes("trade") || t.includes("hvac")) return "plumbing";
  return payload.niche || null;
}

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method === "GET") {
    return res.status(200).json({
      ok: true,
      message: "iClosed → Slack/Supabase/CAPI webhook. POST iClosed payloads here.",
      env: {
        supabase: !!process.env.SUPABASE_URL && !!process.env.SUPABASE_SERVICE_ROLE_KEY,
        slack: !!(process.env.SLACK_BOOKED_WEBHOOK || process.env.SLACK_QUALIFIED_WEBHOOK),
        capi: !!process.env.META_CAPI_ACCESS_TOKEN,
      },
    });
  }
  if (req.method !== "POST") return res.status(405).json({ error: "method not allowed" });

  let body = req.body || {};
  if (typeof body === "string") { try { body = JSON.parse(body); } catch { body = {}; } }

  // iClosed payload shape varies by integration version. Pull common fields with fallbacks.
  const booking_id = body.id || body.booking_id || body.event_id || crypto.randomUUID();
  const first_name = body.first_name || body.firstName || (body.name || "").split(" ")[0] || null;
  const last_name  = body.last_name  || body.lastName  || (body.name || "").split(" ").slice(1).join(" ") || null;
  const email      = body.email || body.email_address || null;
  const phone      = body.phone || body.phone_number || null;
  const start_iso  = body.start_time || body.scheduled_at || body.event_start || null;
  const niche      = pickNiche(body);

  // 1. Persist to Supabase
  const supRow = {
    booking_id,
    first_name, last_name, email, phone,
    niche,
    booked_at: start_iso,
    source_url: body.source_url || body.utm_source || null,
    capi_event_id: booking_id,
    raw_payload: body,
  };
  await supabaseUpsertBooking(supRow);

  // 2. Slack notification — boxed with key fields
  const when = start_iso ? new Date(start_iso).toLocaleString("en-AU", { dateStyle: "medium", timeStyle: "short", timeZone: "Australia/Sydney" }) : "(no time)";
  const slackText = [
    `📅 *NEW BOOKING* — ${first_name || "?"} ${last_name || ""}`.trim(),
    `When: *${when}* AEST`,
    `Contact: ${email || "?"} · ${phone || "?"}`,
    niche ? `Niche: *${niche}*` : null,
    `iClosed ID: \`${booking_id}\``,
  ].filter(Boolean).join("\n");
  await slackPost(slackText);

  // 3. Fire Schedule CAPI event (no $value — that comes from quiz qualifying)
  const client_ip = req.headers["x-forwarded-for"]?.split(",")[0]?.trim() || req.headers["x-real-ip"];
  const client_ua = req.headers["user-agent"];
  await fireCapiSchedule({
    event_id: booking_id,
    email, phone, first_name, niche,
    source_url: body.source_url || "https://answerra.ai",
    client_ip, client_ua,
  });

  return res.status(200).json({ ok: true, booking_id });
}

export const config = { runtime: "nodejs" };
