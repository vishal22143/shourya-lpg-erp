// Shourya ERP v24 — Service Worker (PWA offline caching)
var CACHE = 'shourya-erp-v24';
var ASSETS = ['/', '/manifest.json'];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE).then(function(cache) {
      return cache.addAll(ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(names) {
      return Promise.all(
        names.filter(function(n) { return n !== CACHE; })
             .map(function(n) { return caches.delete(n); })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function(e) {
  var url = new URL(e.request.url);
  
  // API calls — always network first, never cache
  if (url.pathname.startsWith('/api/')) {
    e.respondWith(
      fetch(e.request).catch(function() {
        return new Response(JSON.stringify({ok: false, offline: true}), {
          headers: {'Content-Type': 'application/json'}
        });
      })
    );
    return;
  }
  
  // HTML/JS/CSS — cache first, fallback to network (PWA offline)
  e.respondWith(
    caches.match(e.request).then(function(cached) {
      if (cached) {
        // Return cache immediately, update in background
        fetch(e.request).then(function(resp) {
          if (resp.status === 200) {
            caches.open(CACHE).then(function(cache) { cache.put(e.request, resp); });
          }
        }).catch(function() {});
        return cached;
      }
      // Not in cache — fetch and cache
      return fetch(e.request).then(function(resp) {
        if (resp.status === 200) {
          var clone = resp.clone();
          caches.open(CACHE).then(function(cache) { cache.put(e.request, clone); });
        }
        return resp;
      }).catch(function() {
        return new Response('Offline', {status: 503});
      });
    })
  );
});
