/* Answerra · Meta Pixel + CAPI dedup loader
   - Loads pixel base code
   - Fires PageView client-side with a unique event_id
   - Beacons the same event_id to /api/capi-pageview so Meta dedups browser+server
   - One source of truth: change PIXEL here OR set PIXEL_ID in the backend env var. */
(function(){
  var PIXEL = '1511657447261837';

  // Standard Meta Pixel base code
  !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
  n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}
  (window,document,'script','https://connect.facebook.net/en_US/fbevents.js');

  // Unique event_id per pageview so browser pixel + CAPI server event dedup
  var eventId = (window.crypto && crypto.randomUUID)
    ? crypto.randomUUID()
    : (Date.now() + '-' + Math.random().toString(36).slice(2));

  fbq('init', PIXEL);
  fbq('track', 'PageView', {}, { eventID: eventId });

  // Server-side PageView via CAPI (sendBeacon — survives page unload)
  try {
    var payload = JSON.stringify({
      event_id: eventId,
      event_name: 'PageView',
      event_source_url: window.location.href,
      referrer: document.referrer || ''
    });
    if (navigator.sendBeacon) {
      var blob = new Blob([payload], { type: 'application/json' });
      navigator.sendBeacon('/api/capi-pageview', blob);
    } else {
      fetch('/api/capi-pageview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: payload,
        keepalive: true
      });
    }
  } catch(e) {}
})();
