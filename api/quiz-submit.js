// /api/quiz-submit.js
// Stores quiz response → Supabase, posts to Slack #leads-qualified, fires Meta CAPI
// Purchase event ($30 AUD) ONLY when both:
//   • revenue ≥ $1M  (i.e. one of "$1M-$2.5M", "$2.5M-$5M", "$5M-$10M", "$10M+")
//   • urgency ∈ {yesterday, today}
// Implements Jeremy Haynes' Venus Fly Trap 2.0 Section 6 pixel-conditioning principle.

import crypto from "node:crypto";

const PIXEL_ID = process.env.PIXEL_ID || "1511657447261837";
const META_API_VERSION = "v19.0";
const PURCHASE_VALUE = 30;
const PURCHASE_CURRENCY = "AUD";

const QUALIFYING_REVENUE = new Set(["$1M-$2.5M", "$2.5M-$5M", "$5M-$10M", "$10M+"]);
const QUALIFYING_URGENCY = new Set(["yesterday", "today"]);

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

async function supabaseInsert(row) {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) {
    console.warn("[quiz-submit] Supabase env vars missing — skipping insert");
    return { skipped: true };
  }
  const r = await fetch(`${url}/rest/v1/quiz_responses`, {
    method: "POST",
    headers: {
      apikey: key,
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
      Prefer: "return=representation",
    },
    body: JSON.stringify([row]),
  });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) {
    console.error("[supabase] insert failed", { status: r.status, body, hasUrl: !!url, urlPrefix: (url||"").slice(0,40), keyPrefix: (key||"").slice(0,12) });
  }
  return { ok: r.ok, status: r.status, body };
}

async function slackPost(payload) {
  const url = process.env.SLACK_QUALIFIED_WEBHOOK;
  if (!url) {
    console.warn("[quiz-submit] SLACK_QUALIFIED_WEBHOOK not set — skipping");
    return { skipped: true };
  }
  try {
    const r = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return { ok: r.ok, status: r.status };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

async function fireCapi({ event_id, email, phone, first_name, business_name, niche, source_url, client_ip, client_ua }) {
  const token = process.env.META_CAPI_ACCESS_TOKEN;
  if (!token) return { skipped: true, reason: "no_token" };

  const user_data = {};
  if (email)      user_data.em = [sha256(email)];
  if (phone)      user_data.ph = [sha256(normalisePhone(phone))];
  if (first_name) user_data.fn = [sha256(first_name)];
  user_data.country = [sha256("au")];
  if (client_ip) user_data.client_ip_address = client_ip;
  if (client_ua) user_data.client_user_agent = client_ua;

  const event_payload = {
    data: [{
      event_name: "Purchase",
      event_time: Math.floor(Date.now() / 1000),
      event_id,
      action_source: "website",
      event_source_url: source_url || "https://answerra.ai",
      user_data,
      custom_data: {
        value: PURCHASE_VALUE,
        currency: PURCHASE_CURRENCY,
        content_name: "Answerra Quiz Qualified Lead",
        content_type: "product",
        niche,
        business_name,
      },
    }],
  };

  const url = `https://graph.facebook.com/${META_API_VERSION}/${PIXEL_ID}/events?access_token=${encodeURIComponent(token)}`;
  try {
    const r = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(event_payload),
    });
    const body = await r.json().catch(() => ({}));
    return { ok: r.ok, status: r.status, body };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

function buildSlackPayload({ pixel_fired, showup_commitment, body, business }) {
  const qualBadge = pixel_fired ? "🟢 *QUALIFIED LEAD · pixel fired*" : "⚪ Standard lead · pixel not fired";
  const showupBadge = showup_commitment === "reschedule" ? "⚠️ *NEEDS RESCHEDULE*" : "✓ Confirmed";
  const benefits = (body.benefits || []).map(b => `• ${b}`).join("\n") || "_(none selected)_";
  const businessLine = business?.address
    ? `${business.address}${business.website ? " · " + business.website : ""}${business.rating ? " · " + business.rating + "★ (" + (business.reviews || 0) + " reviews)" : ""}`
    : "_(no business confirmation)_";

  const txt = [
    `${qualBadge}`,
    `*${body.business_name || "(no business)"}* — ${showupBadge}`,
    `${body.first_name || "?"}  ·  ${body.phone || "?"}  ·  ${body.email || "?"}`,
    `Niche: *${body.niche || "?"}*  ·  Revenue: *${body.revenue || "?"}*  ·  Urgency: *${body.urgency || "?"}*`,
    `Wants:\n${benefits}`,
    body.notes ? `Notes: _${body.notes}_` : null,
    `Google: ${businessLine}`,
  ].filter(Boolean).join("\n");
  return { text: txt, mrkdwn: true };
}

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();

  if (req.method === "GET") {
    return res.status(200).json({
      ok: true,
      message: "Quiz submit endpoint. POST form payloads here.",
      env: {
        supabase: !!process.env.SUPABASE_URL && !!process.env.SUPABASE_SERVICE_ROLE_KEY,
        slack: !!process.env.SLACK_QUALIFIED_WEBHOOK,
        capi: !!process.env.META_CAPI_ACCESS_TOKEN,
      },
    });
  }

  if (req.method !== "POST") return res.status(405).json({ error: "method not allowed" });

  const body = req.body || {};
  const business = body.business || {};

  // Pixel conditioning: only fire CAPI if BOTH revenue qualifies AND urgency is high
  const revenue_qualifies = QUALIFYING_REVENUE.has(body.revenue);
  const urgency_qualifies = QUALIFYING_URGENCY.has(body.urgency);
  const pixel_fired = revenue_qualifies && urgency_qualifies;

  // Use booking_id as event_id so it dedups with the booking-confirm CAPI fire
  const event_id = body.booking_id || crypto.randomUUID();
  const client_ip = req.headers["x-forwarded-for"]?.split(",")[0]?.trim() || req.headers["x-real-ip"];
  const client_ua = req.headers["user-agent"];

  // 1) Persist to Supabase
  const supRow = {
    booking_id: body.booking_id || null,
    first_name: body.first_name || null,
    email: body.email || null,
    phone: body.phone || null,
    niche: body.niche || null,
    business_name: business.name || body.business_name || null,
    business_address: business.address || null,
    business_phone: business.phone || null,
    business_website: business.website || null,
    business_place_id: business.place_id || null,
    business_rating: business.rating ?? null,
    business_reviews: business.reviews ?? null,
    revenue: body.revenue || null,
    benefits: body.benefits || [],
    notes: body.notes || null,
    urgency: body.urgency || null,
    showup_commitment: body.showup_commitment || null,
    pixel_fired,
    capi_event_id: event_id,
    user_agent: client_ua,
    ip_address: client_ip,
  };
  const supResult = await supabaseInsert(supRow);

  // 2) Slack notification — always (qualified or not, including reschedules)
  const slackResult = await slackPost(buildSlackPayload({ pixel_fired, showup_commitment: body.showup_commitment, body, business }));

  // 3) Fire CAPI ONLY if pixel_fired === true
  let capiResult = { skipped: true, reason: "not qualified" };
  if (pixel_fired) {
    capiResult = await fireCapi({
      event_id,
      email: body.email,
      phone: body.phone,
      first_name: body.first_name,
      business_name: business.name || body.business_name,
      niche: body.niche,
      source_url: req.headers.referer,
      client_ip,
      client_ua,
    });
  }

  return res.status(200).json({
    ok: true,
    pixel_fired,
    event_id,
    redirect: `/thanks?id=${encodeURIComponent(event_id)}`,
    supabase: supResult.skipped ? "skipped (no env)" : (supResult.ok ? "stored" : "error"),
    slack: slackResult.skipped ? "skipped (no env)" : (slackResult.ok ? "posted" : "error"),
    capi: capiResult.skipped ? `skipped (${capiResult.reason})` : (capiResult.ok ? "fired" : "error"),
  });
}

export const config = { runtime: "nodejs" };
