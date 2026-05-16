// /api/places-details.js
// Server-side proxy for Google Places Details. Returns the fields the quiz
// needs (name, formatted_address, formatted_phone_number, website, rating,
// user_ratings_total) in a flat JSON shape the frontend can drop into state.business.

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "GET") return res.status(405).json({ error: "method not allowed" });

  const key = process.env.GOOGLE_PLACES_API_KEY;
  if (!key) return res.status(500).json({ error: "GOOGLE_PLACES_API_KEY not set" });

  const place_id = (req.query.place_id || "").toString().trim();
  if (!place_id) return res.status(400).json({ error: "place_id required" });

  const url = new URL("https://maps.googleapis.com/maps/api/place/details/json");
  url.searchParams.set("place_id", place_id);
  url.searchParams.set("fields", "name,formatted_address,formatted_phone_number,international_phone_number,website,rating,user_ratings_total,url");
  url.searchParams.set("language", "en-AU");
  url.searchParams.set("key", key);

  try {
    const r = await fetch(url.toString());
    const data = await r.json();
    if (data.status !== "OK") {
      console.error("[places-details] google error", JSON.stringify({ status: data.status, error_message: data.error_message }));
      return res.status(200).json({ ok: false, error: data.status });
    }
    const p = data.result || {};
    const out = {
      place_id,
      name: p.name || "",
      address: p.formatted_address || "",
      phone: p.formatted_phone_number || p.international_phone_number || "",
      website: p.website ? p.website.replace(/^https?:\/\/(www\.)?/, "").replace(/\/$/, "") : "",
      rating: p.rating || null,
      reviews: p.user_ratings_total || 0,
      maps_url: p.url || "",
    };
    res.setHeader("Cache-Control", "s-maxage=300, stale-while-revalidate=600");
    return res.status(200).json({ ok: true, business: out });
  } catch (e) {
    console.error("[places-details] fetch failed", e.message);
    return res.status(200).json({ ok: false, error: e.message });
  }
}

export const config = { runtime: "nodejs" };
