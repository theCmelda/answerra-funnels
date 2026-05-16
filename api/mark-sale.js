// /api/mark-sale.js
// Mark a booking as a closed high-ticket sale. Joins back through visitor_id
// to the original click attribution and fires a Meta CAPI Purchase event with
// the stored fbc/fbp so Meta can attribute the sale to the originating ad.
//
// AUTH: requires header `x-admin-secret` matching env ADMIN_SECRET. Also accepts
// ?secret= query param so the admin HTML page can call it without custom headers.
//
// POST body: { booking_id, value, currency='AUD', notes? }

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
  if (d.startsWith("0") && d.length === 10) return "61" + d.slice(1);
  if (d.startsWith("61")) return d;
  return d;
}

async function supabaseRpc(path, init) {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) return { skipped: true };
  init.headers = Object.assign({}, init.headers, {
    apikey: key,
    Authorization: `Bearer ${key}`,
    "Content-Type": "application/json",
  });
  const r = await fetch(`${url}${path}`, init);
  const body = await r.json().catch(() => ({}));
  if (!r.ok) console.error("[mark-sale] supabase " + JSON.stringify({ path, status: r.status, body }));
  return { ok: r.ok, status: r.status, body };
}

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, x-admin-secret");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method === "GET") {
    return res.status(200).json({
      ok: true,
      message: "mark-sale endpoint. POST {booking_id, value, currency, notes}. Requires admin secret.",
    });
  }
  if (req.method !== "POST") return res.status(405).end();

  const secret = process.env.ADMIN_SECRET;
  const provided = req.headers["x-admin-secret"] || (req.query && req.query.secret);
  if (!secret || provided !== secret) {
    return res.status(401).json({ error: "unauthorized" });
  }

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch { body = {}; } }
  body = body || {};

  const { booking_id, value, currency = "AUD", notes = null } = body;
  if (!booking_id || typeof value !== "number" || value <= 0) {
    return res.status(400).json({ error: "booking_id and numeric value > 0 required" });
  }
  const cents = Math.round(value * 100);

  // 1. Mark booking as closed
  const upd = await supabaseRpc(`/rest/v1/bookings?booking_id=eq.${encodeURIComponent(booking_id)}`, {
    method: "PATCH",
    headers: { Prefer: "return=representation" },
    body: JSON.stringify({
      status: "closed",
      sale_value_cents: cents,
      sale_currency: currency,
      sale_closed_at: new Date().toISOString(),
      sale_notes: notes,
    }),
  });
  if (!upd.ok || !Array.isArray(upd.body) || !upd.body.length) {
    return res.status(404).json({ error: "booking_id not found", booking_id });
  }
  const booking = upd.body[0];

  // 2. Join to visits for original click attribution (fbc/fbp/fbclid)
  let fbc = null, fbp = null, fbclid = null;
  if (booking.visitor_id) {
    const vr = await supabaseRpc(
      `/rest/v1/visits?visitor_id=eq.${encodeURIComponent(booking.visitor_id)}&select=fbc,fbp,fbclid,utm_campaign,utm_content&order=first_seen_at.asc&limit=1`,
      { method: "GET" }
    );
    if (vr.ok && Array.isArray(vr.body) && vr.body[0]) {
      fbc = vr.body[0].fbc; fbp = vr.body[0].fbp; fbclid = vr.body[0].fbclid;
    }
  }

  // 3. Fire CAPI Purchase
  const token = process.env.META_CAPI_ACCESS_TOKEN;
  let capiResult = { skipped: true, reason: "no_token" };
  if (token) {
    const user_data = { country: [sha256("au")] };
    if (booking.email)      user_data.em = [sha256(booking.email)];
    if (booking.phone)      user_data.ph = [sha256(normalisePhone(booking.phone))];
    if (booking.first_name) user_data.fn = [sha256(booking.first_name)];
    if (fbc) user_data.fbc = fbc;
    if (fbp) user_data.fbp = fbp;

    const payload = {
      data: [{
        event_name: "Purchase",
        event_time: Math.floor(Date.now() / 1000),
        event_id: "sale_" + booking_id,
        action_source: "website",
        event_source_url: "https://answerra.ai/admin/sales",
        user_data,
        custom_data: {
          value: value,
          currency: currency,
          content_name: "Answerra High-Ticket Sale",
          content_type: "product",
          niche: booking.niche,
          order_id: booking_id,
        },
      }],
    };
    try {
      const r = await fetch(
        `https://graph.facebook.com/${META_API_VERSION}/${PIXEL_ID}/events?access_token=${encodeURIComponent(token)}`,
        { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }
      );
      capiResult = { ok: r.ok, status: r.status };
      if (!r.ok) console.error("[mark-sale] capi failed " + JSON.stringify(await r.json().catch(()=>({}))));
    } catch (e) {
      capiResult = { ok: false, error: e.message };
    }
  }

  // 4. Slack ping (use SLACK_SALES_WEBHOOK if set, fall back to qualified)
  try {
    const slackUrl = process.env.SLACK_SALES_WEBHOOK || process.env.SLACK_QUALIFIED_WEBHOOK;
    if (slackUrl) {
      const txt = [
        `💰 *HIGH-TICKET SALE CLOSED* — ${booking.first_name || "?"} ${booking.last_name || ""}`.trim(),
        `Value: *$${value.toLocaleString("en-AU")} ${currency}*`,
        `Niche: *${booking.niche || "?"}* · Booking: \`${booking_id}\``,
        fbclid ? `🎯 Attributed to fbclid: \`${fbclid.slice(0, 24)}...\`` : `⚠️ No fbclid attribution found`,
        notes ? `Notes: ${notes}` : null,
      ].filter(Boolean).join("\n");
      await fetch(slackUrl, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text: txt, mrkdwn: true }) });
    }
  } catch (e) {}

  return res.status(200).json({
    ok: true,
    booking_id,
    sale_value_cents: cents,
    sale_currency: currency,
    attribution: { fbclid, fbc_present: !!fbc, fbp_present: !!fbp, visitor_id: booking.visitor_id },
    capi: capiResult,
  });
}

export const config = { runtime: "nodejs" };
