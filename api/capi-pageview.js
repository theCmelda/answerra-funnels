// /api/capi-pageview.js — Server-side PageView for Meta CAPI
// Receives a beacon from /pixel.js with the event_id used by the browser pixel,
// fires the same PageView event to Meta CAPI for browser/server deduplication.

import crypto from "node:crypto";

const PIXEL_ID = process.env.PIXEL_ID || "1511657447261837";
const META_API_VERSION = "v19.0";

function sha256(input) {
  if (!input) return undefined;
  return crypto.createHash("sha256").update(String(input).trim().toLowerCase()).digest("hex");
}

function getCookie(req, name) {
  const cookie = req.headers.cookie || "";
  const match = cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
  return match ? decodeURIComponent(match[1]) : undefined;
}

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method === "GET") {
    return res.status(200).json({
      ok: true,
      message: "CAPI PageView endpoint. Beacon POSTs from /pixel.js arrive here.",
      env: { capi: !!process.env.META_CAPI_ACCESS_TOKEN, pixel_id: PIXEL_ID }
    });
  }
  if (req.method !== "POST") return res.status(405).end();

  const token = process.env.META_CAPI_ACCESS_TOKEN;
  if (!token) {
    return res.status(200).json({ skipped: true, reason: "no_token" });
  }

  // Body parsing: sendBeacon sends raw blob, fetch sends JSON. Both arrive on req.body in Vercel.
  let body = req.body;
  if (typeof body === "string") {
    try { body = JSON.parse(body); } catch { body = {}; }
  }
  body = body || {};

  const event_id = body.event_id || crypto.randomUUID();
  const event_name = body.event_name || "PageView";
  const source_url = body.event_source_url || req.headers.referer || "";

  const user_data = {
    country: [sha256("au")],
  };
  const ip = req.headers["x-forwarded-for"]?.split(",")[0]?.trim() || req.headers["x-real-ip"];
  const ua = req.headers["user-agent"];
  if (ip) user_data.client_ip_address = ip;
  if (ua) user_data.client_user_agent = ua;
  const fbp = getCookie(req, "_fbp");
  const fbc = getCookie(req, "_fbc");
  if (fbp) user_data.fbp = fbp;
  if (fbc) user_data.fbc = fbc;

  const payload = {
    data: [{
      event_name,
      event_time: Math.floor(Date.now() / 1000),
      event_id,
      action_source: "website",
      event_source_url: source_url,
      user_data,
    }],
  };

  try {
    const r = await fetch(
      `https://graph.facebook.com/${META_API_VERSION}/${PIXEL_ID}/events?access_token=${encodeURIComponent(token)}`,
      { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }
    );
    const out = await r.json().catch(() => ({}));
    if (!r.ok) {
      console.error("[capi-pageview] failed", JSON.stringify({ status: r.status, body: out }));
    }
    return res.status(200).json({ ok: r.ok, status: r.status });
  } catch (e) {
    console.error("[capi-pageview] exception", e.message);
    return res.status(200).json({ ok: false, error: e.message });
  }
}

export const config = { runtime: "nodejs" };
