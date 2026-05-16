// /api/booking-confirm.js
// iClosed webhook → 1) Retell outbound call, 2) Meta CAPI Purchase event ($30 AUD)
//
// Triggered by iClosed when a booking is created. We:
//   • map niche (from referrer URL or event slug) → Aria agent → fire Retell call
//   • POST a Purchase event to Meta CAPI (pixel 1511657447261837) for $30 AUD
//     so Meta ad delivery optimises toward people who actually book.
//
// Required env vars:
//   RETELL_API_KEY            — Retell secret
//   META_CAPI_ACCESS_TOKEN    — Meta CAPI access token (Events Manager → settings)

const AGENT_MAP = {
  dental: "agent_2725c7e726f65714997eecdd0f",
  medspa: "agent_0849668d84d08f9eecf415ad9c",
  plumbing: "agent_f54be66feca18d5a89d0ef85ba",
};

const FROM_NUMBER = "+13185960765";
const PIXEL_ID = process.env.PIXEL_ID || "1511657447261837";
const META_API_VERSION = "v19.0";
const PURCHASE_VALUE = 30;
const PURCHASE_CURRENCY = "AUD";

function detectNiche(payload) {
  const haystack = JSON.stringify(payload || {}).toLowerCase();
  if (haystack.includes("dental") || haystack.includes("dentist")) return "dental";
  if (haystack.includes("medspa") || haystack.includes("clinic") || haystack.includes("cosmetic") || haystack.includes("aesthetic")) return "medspa";
  if (haystack.includes("plumb") || haystack.includes("hvac") || haystack.includes("trade")) return "plumbing";
  return "dental"; // default
}

function pluck(obj, keys) {
  for (const k of keys) {
    const v = k.split(".").reduce((a, p) => (a ? a[p] : undefined), obj);
    if (v) return String(v);
  }
  return null;
}

// SHA256-lowercase per Meta CAPI spec
async function sha256(input) {
  if (!input) return undefined;
  const buf = new TextEncoder().encode(String(input).trim().toLowerCase());
  const hash = await crypto.subtle.digest("SHA-256", buf);
  return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, "0")).join("");
}

function normalisePhone(p) {
  if (!p) return undefined;
  const d = String(p).replace(/\D/g, "");
  if (!d) return undefined;
  if (d.startsWith("0") && d.length === 10) return "61" + d.slice(1);
  if (d.startsWith("61")) return d;
  return d;
}


// ===== Slack + Supabase helpers (added for consolidation) =====
async function slackPost(text) {
  const url = process.env.SLACK_BOOKED_WEBHOOK || process.env.SLACK_QUALIFIED_WEBHOOK;
  if (!url) return { skipped: true };
  try {
    const r = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text, mrkdwn: true }) });
    return { ok: r.ok };
  } catch (e) { return { ok: false, error: e.message }; }
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
  if (!r.ok) console.error("[booking-confirm] supabase upsert " + JSON.stringify({ status: r.status, body: await r.json().catch(()=>({}))}));
  return { ok: r.ok };
}

async function lookupVisitorFbc(visitor_id) {
  if (!visitor_id) return { fbc: null, fbp: null };
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) return { fbc: null, fbp: null };
  try {
    const r = await fetch(`${url}/rest/v1/visits?visitor_id=eq.${encodeURIComponent(visitor_id)}&select=fbc,fbp&order=first_seen_at.asc&limit=1`, {
      headers: { apikey: key, Authorization: `Bearer ${key}` }
    });
    if (!r.ok) return { fbc: null, fbp: null };
    const arr = await r.json();
    return arr[0] ? { fbc: arr[0].fbc || null, fbp: arr[0].fbp || null } : { fbc: null, fbp: null };
  } catch { return { fbc: null, fbp: null }; }
}

async function fireMetaCapi({ email, phone, first_name, last_name, niche, booking_id, source_url, client_ip, client_ua, fbc, fbp }) {
  const token = process.env.META_CAPI_ACCESS_TOKEN;
  if (!token) {
    console.warn("[booking-confirm] META_CAPI_ACCESS_TOKEN not set — skipping CAPI fire");
    return { skipped: true, reason: "no_token" };
  }

  const event_id = booking_id || (typeof crypto !== "undefined" && crypto.randomUUID ? crypto.randomUUID() : String(Date.now()));

  const user_data = {};
  const [em, ph, fn, ln] = await Promise.all([
    sha256(email), sha256(normalisePhone(phone)),
    sha256(first_name), sha256(last_name),
  ]);
  if (em) user_data.em = [em];
  if (ph) user_data.ph = [ph];
  if (fn) user_data.fn = [fn];
  if (ln) user_data.ln = [ln];
  user_data.country = [await sha256("au")];
  if (client_ip) user_data.client_ip_address = client_ip;
  if (client_ua) user_data.client_user_agent = client_ua;
  if (fbc) user_data.fbc = fbc;
  if (fbp) user_data.fbp = fbp;

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
        content_name: "Answerra AI Receptionist Build",
        content_type: "product",
        niche,
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
    const out = await r.json().catch(() => ({}));
    if (!r.ok) console.error("[booking-confirm] CAPI error", r.status, out);
    return { ok: r.ok, status: r.status, event_id, meta: out };
  } catch (e) {
    console.error("[booking-confirm] CAPI exception", e);
    return { ok: false, error: e.message, event_id };
  }
}

export default async function handler(req, res) {
  // CORS for testing
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method === "GET") {
    return res.status(200).json({
      ok: true,
      message: "iClosed → Retell + Meta CAPI webhook. POST iClosed booking payloads here.",
      agents: Object.keys(AGENT_MAP),
      pixel: PIXEL_ID,
      capi_enabled: !!process.env.META_CAPI_ACCESS_TOKEN,
    });
  }
  if (req.method !== "POST") return res.status(405).json({ error: "method not allowed" });

  const RETELL_KEY = process.env.RETELL_API_KEY;
  if (!RETELL_KEY) return res.status(500).json({ error: "RETELL_API_KEY not set" });

  const body = req.body || {};

  // Extract from common iClosed webhook field shapes
  const phone = pluck(body, [
    "phone", "phone_number", "invitee.phone", "data.phone",
    "booking.phone", "contact.phone", "fields.phone",
  ]);
  const email = pluck(body, [
    "email", "invitee.email", "data.email", "booking.email", "contact.email", "fields.email",
  ]);
  const firstName = pluck(body, [
    "first_name", "firstName", "invitee.first_name", "invitee.firstName",
    "name.first", "data.first_name", "booking.first_name", "contact.first_name",
  ]) || pluck(body, ["name", "full_name", "invitee.name"])?.split(" ")[0];
  const lastName = pluck(body, [
    "last_name", "lastName", "invitee.last_name", "invitee.lastName",
    "name.last", "data.last_name", "booking.last_name", "contact.last_name",
  ]);

  const bookingTime = pluck(body, [
    "scheduled_at", "scheduled_time", "start_time", "starts_at", "booking_time",
    "data.scheduled_at", "booking.scheduled_at", "invitee.scheduled_at",
  ]) || "your booked slot";

  const bookingId = pluck(body, [
    "id", "booking_id", "uuid", "data.id", "booking.id", "invitee.uuid",
  ]);

  const niche = detectNiche(body);
  const agentId = AGENT_MAP[niche];
  const sourceUrl = pluck(body, ["referrer", "url", "source_url", "data.url"]) || "https://answerra.ai";
  const clientIp = req.headers["x-forwarded-for"]?.split(",")[0]?.trim() || req.headers["x-real-ip"];
  const clientUa = req.headers["user-agent"];

  if (!phone) {
    return res.status(400).json({ error: "no phone number in payload", body_keys: Object.keys(body) });
  }

  // iClosed passes our visitor_id back via custom field, q-param or metadata
  const visitorId = pluck(body, ["visitor_id", "v_id", "data.visitor_id", "metadata.visitor_id", "fields.visitor_id", "fields.v_id"]);

  // Look up original click attribution (fbc/fbp) so CAPI Purchase ties to the originating ad
  const { fbc, fbp } = await lookupVisitorFbc(visitorId);

  // 1. Persist booking row (upsert on booking_id) — needed for /api/mark-sale to find it later
  await supabaseUpsertBooking({
    booking_id: bookingId,
    first_name: firstName, last_name: lastName, email, phone,
    niche,
    booked_at: bookingTime !== "your booked slot" ? bookingTime : null,
    source_url: sourceUrl,
    capi_event_id: bookingId,
    visitor_id: visitorId,
    raw_payload: body,
  });

  // 2. Slack ping
  const slackTime = (bookingTime && bookingTime !== "your booked slot")
    ? (() => { try { return new Date(bookingTime).toLocaleString("en-AU", { dateStyle: "medium", timeStyle: "short", timeZone: "Australia/Sydney" }) + " AEST"; } catch { return bookingTime; } })()
    : "(no time)";
  await slackPost([
    `📅 *NEW BOOKING* — ${firstName || "?"} ${lastName || ""}`.trim(),
    `When: *${slackTime}*`,
    `Contact: ${email || "?"} · ${phone || "?"}`,
    `Niche: *${niche}*  ·  Booking: \`${bookingId || "?"}\``,
    fbc ? `🎯 Ad-attributed (fbc cookie present)` : `⚠️ No fbclid attribution`,
  ].join("\n"));

  // 3. Fire Meta CAPI Purchase (Retell call moved to /api/quiz-submit so Aria has
  // the full quiz context — business name, revenue band, urgency, top benefit, etc).
  const capiResult = await fireMetaCapi({
    email, phone, first_name: firstName, last_name: lastName,
    niche, booking_id: bookingId, source_url: sourceUrl,
    client_ip: clientIp, client_ua: clientUa,
    fbc, fbp,
  }).catch(e => ({ ok: false, error: e.message }));
  // Retell stub — kept so downstream code that reads `retellResult` doesn't break
  const retellResult = { status: "fulfilled", value: { ok: true, skipped: true, reason: "moved_to_quiz_submit" } };

  // Always return success — Retell moved to quiz-submit; CAPI is best-effort
  const retell = retellResult.value;
  const capi   = capiResult;

  if (!retell.ok) {
    console.error("Retell error", retell);
    return res.status(500).json({ error: "retell call failed", retell, capi });
  }

  return res.status(200).json({
    ok: true,
    niche,
    agent_id: agentId,
    phone_first6: phone.slice(0, 6) + "***",
    call_id: retell.body?.call_id,
    call_status: retell.body?.call_status,
    capi: { ok: capi.ok, event_id: capi.event_id, events_received: capi.meta?.events_received },
  });
}

export const config = { runtime: "nodejs" };
