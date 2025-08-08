const CACHE_NAME = 'app-cache-v1';
const URLS_TO_CACHE = [
  '/',
  '/index.html',
  '/static/js/bundle.js',
  '/favicon.ico',
  '/manifest.json'
];

self.addEventListener('install', (event: ExtendableEvent) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(URLS_TO_CACHE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event: ExtendableEvent) => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event: FetchEvent) => {
  event.respondWith(
    caches.match(event.request).then(response =>
      response ||
      fetch(event.request).then(networkResponse => {
        if (event.request.method === 'GET') {
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, networkResponse.clone()));
        }
        return networkResponse;
      })
    )
  );
});
