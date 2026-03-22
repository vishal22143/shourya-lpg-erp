// Shourya ERP v24.1 — Service Worker (cache busted)
var CACHE = 'shourya-erp-v241';

self.addEventListener('install', function(e) {
  // Force activate immediately (don't wait for old SW)
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE).then(function(cache) {
      return cache.addAll(['/', '/index.html']);
    })
  );
});

self.addEventListener('activate', function(e) {
  // Delete ALL old caches
  e.waitUntil(
    caches.keys().then(function(names) {
      return Promise.all(
        names.map(function(n) {
          if (n !== CACHE) { console.log('Deleting old cache:', n); return caches.delete(n); }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function(e) {
  var url = new URL(e.request.url);
  
  // API calls — always network, never cache
  if (url.pathname.startsWith('/api/') || url.hostname === 'api.npoint.io') {
    e.respondWith(fetch(e.request).catch(function() {
      return new Response('{"offline":true}', {headers: {'Content-Type': 'application/json'}});
    }));
    return;
  }
  
  // HTML — network first, fallback to cache (ensures updates are picked up)
  if (e.request.mode === 'navigate' || url.pathname.endsWith('.html') || url.pathname === '/') {
    e.respondWith(
      fetch(e.request).then(function(resp) {
        if (resp.status === 200) {
          var clone = resp.clone();
          caches.open(CACHE).then(function(c) { c.put(e.request, clone); });
        }
        return resp;
      }).catch(function() {
        return caches.match(e.request).then(function(c) { return c || new Response('Offline', {status: 503}); });
      })
    );
    return;
  }
  
  // Everything else — cache first
  e.respondWith(
    caches.match(e.request).then(function(cached) {
      return cached || fetch(e.request).then(function(resp) {
        if (resp.status === 200) {
          var clone = resp.clone();
          caches.open(CACHE).then(function(c) { c.put(e.request, clone); });
        }
        return resp;
      });
    })
  );
});
