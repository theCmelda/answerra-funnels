// iClosed webhook → Retell outbound call
// POSTed by iClosed when a booking is created.
// Maps niche (from referrer URL or event slug) to the right Aria agent and triggers the call.

const AGENT_MAP = {
  dental: "agent_2725c7e726f65714997eecdd0f",
  medspa: "agent_0849668d84d08f9eecf415ad9c",
  plumbing: "agent_f54be66feca18d5a89d0ef85ba",
};

const FROM_NUMBER = "+13185960765";

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

export default async function handler(req, res) {
  // Allow CORS for testing
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method === "GET") {
    return res.status(200).json({
      ok: true,
      message: "iClosed → Retell webhook. POST iClosed booking payloads here.",
      agents: Object.keys(AGENT_MAP),
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
  const firstName = pluck(body, [
    "first_name", "firstName", "invitee.first_name", "invitee.firstName",
    "name.first", "data.first_name", "booking.first_name", "contact.first_name",
  ]) || pluck(body, ["name", "full_name", "invitee.name"])?.split(" ")[0];

  const bookingTime = pluck(body, [
    "scheduled_at", "scheduled_time", "start_time", "starts_at", "booking_time",
    "data.scheduled_at", "booking.scheduled_at", "invitee.scheduled_at",
  ]) || "your booked slot";

  const niche = detectNiche(body);
  const agentId = AGENT_MAP[niche];

  if (!phone) {
    return res.status(400).json({ error: "no phone number in payload", body_keys: Object.keys(body) });
  }

  // Trigger Retell outbound call
  const r = await fetch("https://api.retellai.com/v2/create-phone-call", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${RETELL_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from_number: FROM_NUMBER,
      to_number: phone,
      override_agent_id: agentId,
      retell_llm_dynamic_variables: {
        first_name: firstName || "there",
        booking_time: bookingTime,
      },
      metadata: { source: "iclosed_booking", niche, vercel_request_id: req.headers["x-vercel-id"] },
    }),
  });

  const out = await r.json().catch(() => ({}));

  if (!r.ok) {
    console.error("Retell error", r.status, out);
    return res.status(500).json({ error: "retell call failed", status: r.status, retell: out });
  }

  return res.status(200).json({
    ok: true, niche, agent_id: agentId, phone_first6: phone.slice(0, 6) + "***",
    call_id: out.call_id, call_status: out.call_status,
  });
}

export const config = { runtime: "nodejs" };
