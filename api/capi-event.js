// /api/capi-event.js
// Meta Conversions API server-side event handler.
//
// Fires a Purchase event (default $30 AUD) to Meta Pixel 1511657447261837.
// Used to track booking → form completion → show-up commitment as a single
// $30 sales event for Meta ad optimisation.
//
// Required env var: META_CAPI_ACCESS_TOKEN (generate at Meta Business Manager
// → Events Manager → Pixel → Settings → Conversions API → Generate access token)
//
// Call from server (e.g. inside booking-confirm.js or quiz-submit.js):
//   await fetch('https://answerra.ai/api/capi-event', {
//     method:'POST', headers:{'Content-Type':'application/json'},
//     body: JSON.stringify({
//       event_name: 'Purchase', value: 30, currency: 'AUD',
//       event_id: 'unique-id', // for dedup with browser fbq
//       email, phone, first_name, last_name,
//       business_name, business_address,
//       client_ip_address, client_user_agent, source_url,
//     })
//   })
//
// Also callable from the browser via fbq() — use the SAME event_id on both
// so Meta deduplicates and counts it once.

import crypto from "node:crypto";

const PIXEL_ID = process.env.PIXEL_ID || "1511657447261837";
const META_API_VERSION = "v19.0";

function sha256(input) {
  if (!input) return undefined;
  return crypto.createHash("sha256").update(String(input).trim().toLowerCase()).digest("hex");
}

function normalisePhone(p) {
  if (!p) return undefined;
  // Strip everything except digits, then take last 11+ for AU (61XXXXXXXXX)
  const digits = String(p).replace(/\D/g, "");
  if (!digits) return undefined;
  // If starts with 0 (AU local format), convert to international 61...
  if (digits.startsWith("0") && digits.length === 10) return "61" + digits.slice(1);
  // If starts with 61, keep
  if (digits.startsWith("61")) return digits;
  // Otherwise return as-is
  return digits;
}

export default async function handler(req, res) {
  // CORS — allow browser POSTs from answerra.ai
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();

  if (req.method === "GET") {
    return res.status(200).json({
      ok: true,
      message: "Meta CAPI server endpoint. POST event payloads here.",
      pixel: PIXEL_ID,
      meta_api: META_API_VERSION,
      env_token_set: !!process.env.META_CAPI_ACCESS_TOKEN,
    });
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "method not allowed" });
  }

  const ACCESS_TOKEN = process.env.META_CAPI_ACCESS_TOKEN;
  if (!ACCESS_TOKEN) {
    return res.status(500).json({ error: "META_CAPI_ACCESS_TOKEN not configured in Vercel env" });
  }

  const body = (req.body || {});

  const event_name = body.event_name || "Purchase";
  const value      = body.value      ?? 30;
  const currency   = body.currency   || "AUD";
  const event_id   = body.event_id   || crypto.randomBytes(16).toString("hex");
  const event_time = body.event_time || Math.floor(Date.now() / 1000);

  // Build the hashed user_data block
  const user_data = {};
  if (body.email)      user_data.em = [sha256(body.email)];
  if (body.phone)      user_data.ph = [sha256(normalisePhone(body.phone))];
  if (body.first_name) user_data.fn = [sha256(body.first_name)];
  if (body.last_name)  user_data.ln = [sha256(body.last_name)];
  if (body.city)       user_data.ct = [sha256(body.city)];
  if (body.state)      user_data.st = [sha256(body.state)];
  if (body.zip)        user_data.zp = [sha256(body.zip)];
  if (body.country)    user_data.country = [sha256(body.country)];

  // Cookie/IP context — non-hashed
  const ip =
    body.client_ip_address ||
    req.headers["x-forwarded-for"]?.split(",")[0]?.trim() ||
    req.headers["x-real-ip"];
  const ua = body.client_user_agent || req.headers["user-agent"];
  if (ip) user_data.client_ip_address = ip;
  if (ua) user_data.client_user_agent = ua;
  if (body.fbc) user_data.fbc = body.fbc; // Facebook click ID cookie
  if (body.fbp) user_data.fbp = body.fbp; // Facebook browser ID cookie

  const custom_data = {
    value,
    currency,
    content_name: body.content_name || "Answerra AI Receptionist Build",
    content_type: body.content_type || "product",
    ...(body.business_name    && { business_name: body.business_name }),
    ...(body.business_address && { business_address: body.business_address }),
    ...(body.niche            && { niche: body.niche }),
    ...(body.funnel           && { funnel: body.funnel }),
  };

  const event_data = {
    data: [{
      event_name,
      event_time,
      event_id,
      action_source: "website",
      event_source_url: body.source_url || req.headers.referer || "https://answerra.ai",
      user_data,
      custom_data,
    }],
    // test_event_code: "TESTxxxxx", // uncomment + use a test code when verifying in Events Manager
  };

  const url = `https://graph.facebook.com/${META_API_VERSION}/${PIXEL_ID}/events?access_token=${encodeURIComponent(ACCESS_TOKEN)}`;

  try {
    const resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(event_data),
    });
    const result = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      console.error("[capi-event] Meta API error", resp.status, result);
      return res.status(502).json({ ok: false, status: resp.status, meta: result, event_id });
    }
    return res.status(200).json({
      ok: true,
      event_name,
      event_id,
      value,
      currency,
      events_received: result.events_received,
      messages: result.messages,
      fbtrace_id: result.fbtrace_id,
    });
  } catch (e) {
    console.error("[capi-event] exception", e);
    return res.status(500).json({ ok: false, error: e.message, event_id });
  }
}

export const config = { runtime: "nodejs" };
