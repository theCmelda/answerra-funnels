// /api/places-autocomplete.js
// Server-side proxy for Google Places Autocomplete (Legacy API).
// Restricts results to AU establishments. Server-side keeps the API key
// off the client, and keeps the HTTP referrer restriction (*.answerra.ai/*)
// from blocking direct fetch from /quiz pages.

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "GET") return res.status(405).json({ error: "method not allowed" });

  const key = process.env.GOOGLE_PLACES_API_KEY;
  if (!key) return res.status(500).json({ error: "GOOGLE_PLACES_API_KEY not set" });

  const q = (req.query.q || "").toString().trim();
  if (q.length < 2) return res.status(200).json({ predictions: [] });

  const url = new URL("https://maps.googleapis.com/maps/api/place/autocomplete/json");
  url.searchParams.set("input", q);
  url.searchParams.set("types", "establishment");
  url.searchParams.set("components", "country:au");
  url.searchParams.set("language", "en-AU");
  url.searchParams.set("key", key);

  try {
    const r = await fetch(url.toString());
    const data = await r.json();
    if (data.status !== "OK" && data.status !== "ZERO_RESULTS") {
      console.error("[places-autocomplete] google error", JSON.stringify({ status: data.status, error_message: data.error_message }));
      return res.status(200).json({ predictions: [], error: data.status });
    }
    const predictions = (data.predictions || []).slice(0, 5).map(p => ({
      place_id: p.place_id,
      description: p.description,
      main_text: p.structured_formatting?.main_text || p.description,
      secondary_text: p.structured_formatting?.secondary_text || "",
    }));
    // Cache for 60s — same query within a minute is the same answer
    res.setHeader("Cache-Control", "s-maxage=60, stale-while-revalidate=120");
    return res.status(200).json({ predictions });
  } catch (e) {
    console.error("[places-autocomplete] fetch failed", e.message);
    return res.status(200).json({ predictions: [], error: e.message });
  }
}

export const config = { runtime: "nodejs" };
