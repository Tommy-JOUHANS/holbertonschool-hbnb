document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;

    if      (path.endsWith('login.html'))                                        initLoginPage();
    else if (path.endsWith('index.html') || path === '/' || path.endsWith('/')) initIndexPage();
    else if (path.endsWith('place.html'))                                        initPlacePage();
    else if (path.endsWith('add_review.html'))                                   initAddReviewPage();
});

const API_URL  = 'http://127.0.0.1:5000';
const API_BASE = `${API_URL}/api/v1`;

function getCookie(name) {
    const match = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));
    return match ? match.split('=')[1] : null;
}
function getToken()   { return getCookie('token'); }
function isLoggedIn() { return !!getToken(); }

function updateAuthUI() {
    const loginLink = document.getElementById('login-link');
    if (!loginLink) return;
    if (isLoggedIn()) {
        loginLink.textContent = 'Logout';
        loginLink.href = '#';
        loginLink.id = 'logout-link';
    }
}

function setupLogout() {
    document.addEventListener('click', (e) => {
        if (e.target && e.target.id === 'logout-link') {
            e.preventDefault();
            document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
            window.location.href = 'index.html';
        }
    });
}

function renderStars(rating) {
    const n = Math.max(0, Math.min(5, parseInt(rating) || 0));
    return '★'.repeat(n) + '☆'.repeat(5 - n);
}

// ============================================================
//  INDEX PAGE
// ============================================================
async function fetchPlaces(token) {
    try {
        const response = await fetch(`${API_BASE}/places`, {
            headers: {
                'Content-Type': 'application/json',
                ...(token ? { 'Authorization': `Bearer ${token}` } : {})
            }
        });
        if (!response.ok) throw new Error(response.statusText);
        const places = await response.json();
        displayPlaces(places);
    } catch (err) {
        const list = document.getElementById('places-list');
        if (list) list.innerHTML =
            `<p style="text-align:center;color:red;">Failed to load places: ${err.message}</p>`;
    }
}

function displayPlaces(places) {
    const list = document.getElementById('places-list');
    if (!list) return;
    list.innerHTML = '';
    if (!places.length) {
        list.innerHTML = '<p style="text-align:center;color:#888;">No places available.</p>';
        return;
    }
    places.forEach(place => {
        const card = document.createElement('article');
        card.className = 'place-card';
        card.dataset.price = place.price;
        card.innerHTML = `
            <h2>${place.title}</h2>
            <p>Price per night: $${place.price}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        list.appendChild(card);
    });
}

function initIndexPage() {
    updateAuthUI();
    setupLogout();

    const token     = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        fetchPlaces('');
    } else {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    }

    const filter = document.getElementById('price-filter');
    if (filter) {
        filter.addEventListener('change', (e) => {
            const selected = e.target.value;
            document.querySelectorAll('.place-card').forEach(card => {
                const price = parseFloat(card.dataset.price);
                card.style.display =
                    (selected === 'all' || price <= parseFloat(selected)) ? '' : 'none';
            });
        });
    }
}

// ============================================================
//  PLACE DETAILS PAGE
// ============================================================
function getPlaceIdFromURL() {
    return new URLSearchParams(window.location.search).get('id');
}

// Fetch place + amenities séparées si besoin
async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        };

        const placeRes = await fetch(`${API_BASE}/places/${placeId}`, { headers });
        if (!placeRes.ok) throw new Error(placeRes.statusText);
        const place = await placeRes.json();

        console.log('Place reçue:', place);
        console.log('Amenities dans place:', place.amenities);

        // Si amenities vides/absentes → essaye l'endpoint séparé
        if (!place.amenities || place.amenities.length === 0) {
            try {
                const amenRes = await fetch(`${API_BASE}/places/${placeId}/amenities`, { headers });
                if (amenRes.ok) {
                    place.amenities = await amenRes.json();
                    console.log('Amenities chargées séparément:', place.amenities);
                }
            } catch {
                // endpoint séparé n'existe pas, on continue
            }
        }

        displayPlaceDetails(place);

    } catch (err) {
        const detailsEl = document.getElementById('place-details');
        if (detailsEl)
            detailsEl.innerHTML = `<p style="color:red;">Failed to load place: ${err.message}</p>`;
    }
}

function displayPlaceDetails(place) {
    // Titre
    const titleEl = document.getElementById('place-title');
    if (titleEl) titleEl.textContent = place.title;
    document.title = place.title;

    // Lien add_review
    const addReviewLink = document.getElementById('add-review-link');
    if (addReviewLink) addReviewLink.href = `add_review.html?id=${place.id}`;

    const detailsEl = document.getElementById('place-details');
    if (detailsEl) {

        // HOST
        let hostName = 'N/A';
        if (place.host && typeof place.host === 'object') {
            hostName = `${place.host.first_name ?? ''} ${place.host.last_name ?? ''}`.trim() || 'N/A';
        } else if (place.owner && typeof place.owner === 'object') {
            hostName = `${place.owner.first_name ?? ''} ${place.owner.last_name ?? ''}`.trim() || 'N/A';
        } else if (typeof place.owner === 'string') {
            hostName = place.owner;
        } else if (typeof place.host === 'string') {
            hostName = place.host;
        }

        // AMENITIES
        let amenities = 'N/A';
        const amenitiesRaw = place.amenities ?? place.place_amenities ?? [];
        if (Array.isArray(amenitiesRaw) && amenitiesRaw.length > 0) {
            amenities = amenitiesRaw.map(a => {
                if (typeof a === 'string') return a;
                return a.name ?? a.title ?? '?';
            }).join(', ');
        }

        detailsEl.innerHTML = '';

        const fields = [
            ['Host',            hostName],
            ['Price per night', `$${place.price}`],
            ['Description',     place.description || 'No description.'],
            ['Amenities',       amenities]
        ];

        fields.forEach(([label, value]) => {
            const p = document.createElement('p');
            p.className = 'place-info';
            p.innerHTML = `<strong>${label}:</strong> ${value}`;
            detailsEl.appendChild(p);
        });
    }

    // Reviews
    const reviewsEl = document.getElementById('reviews');
    if (reviewsEl) {
        reviewsEl.innerHTML = '';
        const heading = document.createElement('h2');
        heading.textContent = 'Reviews';
        reviewsEl.appendChild(heading);

        const reviews = place.reviews || [];
        if (!reviews.length) {
            const msg = document.createElement('p');
            msg.style.color = '#888';
            msg.textContent = 'No reviews yet.';
            reviewsEl.appendChild(msg);
        } else {
            reviews.forEach(r => {
                const card = document.createElement('article');
                card.className = 'review-card';
                const userName = r.user
                    ? (r.user.first_name ?? r.user.name ?? 'Anonymous')
                    : 'Anonymous';
                card.innerHTML = `
                    <h3>${userName}:</h3>
                    <p>${r.text || r.comment || ''}</p>
                    <p>Rating: ${renderStars(r.rating)}</p>
                `;
                reviewsEl.appendChild(card);
            });
        }
    }
}

function initPlacePage() {
    updateAuthUI();
    setupLogout();

    const placeId = getPlaceIdFromURL();
    if (!placeId) return;

    const token            = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        if (addReviewSection) addReviewSection.style.display = 'none';
        fetchPlaceDetails('', placeId);
    } else {
        if (addReviewSection) addReviewSection.style.display = 'block';
        fetchPlaceDetails(token, placeId);
        setupInlineReviewForm(placeId);
    }
}

// ============================================================
//  INLINE REVIEW FORM
// ============================================================
function setupInlineReviewForm(placeId) {
    const form = document.getElementById('review-form');
    if (!form) return;
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const token  = getCookie('token');
        const text   = document.getElementById('review-text')?.value.trim();
        const rating = parseInt(document.getElementById('rating').value);
        if (!text) return;
        await submitReview(token, placeId, text, rating);
    });
}

// ============================================================
//  LOGIN PAGE
// ============================================================
async function loginUser(email, password) {
    const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
    } else {
        alert('Login failed: ' + response.statusText);
    }
}

function initLoginPage() {
    if (isLoggedIn()) { window.location.href = 'index.html'; return; }
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email    = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }
}

// ============================================================
//  ADD REVIEW PAGE
// ============================================================
function checkAuthenticationReview() {
    const token = getCookie('token');
    if (!token) window.location.href = 'index.html';
    return token;
}

async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch(`${API_BASE}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type':  'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ place_id: placeId, text: reviewText, rating: rating })
        });
        const data = await response.json().catch(() => null);
        handleResponse(response, data);
    } catch (err) {
        alert('Network error: ' + err.message);
    }
}

function handleResponse(response, data) {
    if (response.ok) {
        alert('Review submitted successfully!');
        const form = document.getElementById('review-form');
        if (form) form.reset();
        const placeId = getPlaceIdFromURL();
        if (placeId && window.location.pathname.endsWith('add_review.html')) {
            window.location.href = `place.html?id=${placeId}`;
        }
    } else {
        const msg = data?.message || data?.error || `Error ${response.status}`;
        alert('Submission failed: ' + msg);
    }
}

function initAddReviewPage() {
    const token   = checkAuthenticationReview();
    const placeId = getPlaceIdFromURL();

    updateAuthUI();
    setupLogout();

    if (placeId) {
        fetch(`${API_BASE}/places/${placeId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(r => r.json())
        .then(place => {
            const titleEl = document.getElementById('review-place-title');
            if (titleEl) titleEl.textContent = `Reviewing: ${place.title}`;
            document.title = `Add Review — ${place.title}`;
        })
        .catch(() => {});
    }

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const reviewText = document.getElementById('review').value.trim();
            const rating     = parseInt(document.getElementById('rating').value);
            if (!reviewText) return;
            await submitReview(token, placeId, reviewText, rating);
        });
    }
}