// /api/admin-bookings.js — Returns recent bookings + attribution for the admin sales page.
// Auth via ?secret= matching ADMIN_SECRET.

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "GET") return res.status(405).end();

  const secret = process.env.ADMIN_SECRET;
  if (!secret || req.query.secret !== secret) {
    return res.status(401).json({ error: "unauthorized" });
  }

  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) return res.status(500).json({ error: "supabase env missing" });

  try {
    const r = await fetch(`${url}/rest/v1/attributed_leads?limit=100`, {
      headers: { apikey: key, Authorization: `Bearer ${key}` }
    });
    const rows = await r.json();
    return res.status(200).json({ ok: true, rows });
  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
}

export const config = { runtime: "nodejs" };
