self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('chat-cache-v1').then(cache => {
            return cache.addAll([
                '/',
                '/static/style.css',
                '/static/icon-192.png',
                '/static/icon-512.png'
            ]);
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});