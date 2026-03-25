document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;

    if      (path.endsWith('login.html'))                                        initLoginPage();
    else if (path.endsWith('index.html') || path === '/' || path.endsWith('/')) initIndexPage();
    else if (path.endsWith('place.html'))                                        initPlacePage();
    else if (path.endsWith('add_review.html'))                                   initAddReviewPage();
});

// ============================================================
//  CONFIG
// ============================================================
const API_URL  = 'http://127.0.0.1:5000';
const API_BASE = `${API_URL}/api/v1`;

// ============================================================
//  COOKIE HELPERS  (imposés par l'énoncé)
// ============================================================

// Function to get a cookie value by its name
function getCookie(name) {
    const match = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));
    return match ? match.split('=')[1] : null;
}

function getToken() {
    return getCookie('token');
}

function isLoggedIn() {
    return !!getToken();
}

// ============================================================
//  JWT HELPER — decode user_id from token
// ============================================================
function getUserIdFromToken() {
    const token = getToken();
    if (!token) return null;
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.sub || payload.identity || null;
    } catch {
        return null;
    }
}

// ============================================================
//  AUTH UI
// ============================================================
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

// ============================================================
//  API HELPER
// ============================================================
async function apiFetch(endpoint, options = {}) {
    const token = getToken();

    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...(options.headers || {})
    };

    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ message: response.statusText }));
        throw new Error(error.message || `HTTP error ${response.status}`);
    }

    return response.json();
}

// ============================================================
//  STAR RENDERING
// ============================================================
function renderStars(rating) {
    return '★'.repeat(rating) + '☆'.repeat(5 - rating);
}

// ============================================================
//  INDEX PAGE
// ============================================================

// Check authentication and fetch places (pattern de l'énoncé)
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

// GET /api/v1/places (pattern de l'énoncé)
async function fetchPlaces(token) {
    try {
        const response = await fetch(`${API_BASE}/places`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) throw new Error(response.statusText);
        const places = await response.json();
        displayPlaces(places);
    } catch (err) {
        const list = document.getElementById('places-list');
        if (list) list.innerHTML = `<p style="text-align:center;color:red;">Failed to load places: ${err.message}</p>`;
    }
}

// Display place cards (pattern de l'énoncé)
function displayPlaces(places) {
    const list = document.getElementById('places-list');
    if (!list) return;

    list.innerHTML = '';

    if (places.length === 0) {
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

    // Populate price filter and handle auth (pattern de l'énoncé)
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        // Still fetch places even if not logged in
        fetchPlaces('');
    } else {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    }

    // Price filter (pattern de l'énoncé)
    const filter = document.getElementById('price-filter');
    if (filter) {
        filter.addEventListener('change', (event) => {
            const selected = event.target.value;
            const cards = document.querySelectorAll('.place-card');
            cards.forEach(card => {
                const price = parseFloat(card.dataset.price);
                if (selected === 'all' || price <= parseFloat(selected)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

// ============================================================
//  PLACE DETAILS PAGE
// ============================================================

// Extract place ID from URL (pattern de l'énoncé)
function getPlaceIdFromURL() {
    return new URLSearchParams(window.location.search).get('id');
}

// Check authentication for place page (pattern de l'énoncé)
function checkAuthenticationPlace() {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        if (addReviewSection) addReviewSection.style.display = 'none';
    } else {
        if (addReviewSection) addReviewSection.style.display = 'block';
        const placeId = getPlaceIdFromURL();
        fetchPlaceDetails(token, placeId);
    }

    return token;
}

// GET /api/v1/places/<id> (pattern de l'énoncé)
async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`${API_BASE}/places/${placeId}`, {
            headers: {
                'Content-Type': 'application/json',
                ...(token ? { 'Authorization': `Bearer ${token}` } : {})
            }
        });
        if (!response.ok) throw new Error(response.statusText);
        const place = await response.json();
        displayPlaceDetails(place);
    } catch (err) {
        const detailsEl = document.getElementById('place-details');
        if (detailsEl) detailsEl.innerHTML = `<p style="color:red;">Failed to load place: ${err.message}</p>`;
    }
}

// Display place details (pattern de l'énoncé)
function displayPlaceDetails(place) {
    const titleEl     = document.getElementById('place-title');
    const detailsEl   = document.getElementById('place-details');
    const reviewsEl   = document.getElementById('reviews');

    // Title
    if (titleEl) titleEl.textContent = place.title;
    document.title = place.title;

    // Details card
    if (detailsEl) {
        const amenities = Array.isArray(place.amenities)
            ? place.amenities.map(a => a.name || a).join(', ')
            : place.amenities || 'N/A';

        const hostName = place.host
            ? `${place.host.first_name ?? ''} ${place.host.last_name ?? ''}`.trim()
            : place.owner ?? 'N/A';

        detailsEl.innerHTML = `
            <p class="place-info"><strong>Host:</strong> ${hostName}</p>
            <p class="place-info"><strong>Price per night:</strong> $${place.price}</p>
            <p class="place-info"><strong>Description:</strong> ${place.description || 'No description.'}</p>
            <p class="place-info"><strong>Amenities:</strong> ${amenities}</p>
        `;
    }

    // Reviews
    if (reviewsEl) {
        reviewsEl.innerHTML = '';
        const heading = document.createElement('h2');
        heading.textContent = 'Reviews';
        reviewsEl.appendChild(heading);

        const reviews = place.reviews || [];
        if (reviews.length === 0) {
            const msg = document.createElement('p');
            msg.style.color = '#888';
            msg.textContent = 'No reviews yet.';
            reviewsEl.appendChild(msg);
        } else {
            reviews.forEach(r => {
                const card = document.createElement('article');
                card.className = 'review-card';
                const userName = r.user
                    ? `${r.user.first_name ?? r.user.name ?? 'Anonymous'}`
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

    // Use pattern de l'énoncé
    const token = getCookie('token');
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
//  INLINE REVIEW FORM (place.html)
// ============================================================
function setupInlineReviewForm(placeId) {
    const form = document.getElementById('review-form');
    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const token    = getCookie('token');
        const text     = document.getElementById('review-text')?.value.trim();
        const rating   = parseInt(document.getElementById('rating').value);
        const submitBtn = form.querySelector('button[type="submit"]');

        if (!text) return;

        await submitReview(token, placeId, text, rating);
    });
}

// ============================================================
//  LOGIN PAGE — POST /api/v1/auth/login
// ============================================================

// Sends credentials and stores token as cookie (pattern de l'énoncé)
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
    if (isLoggedIn()) {
        window.location.href = 'index.html';
        return;
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email    = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }
}

// ============================================================
//  ADD REVIEW PAGE — POST /api/v1/reviews (pattern de l'énoncé)
// ============================================================

// Check authentication for add_review page (pattern de l'énoncé)
function checkAuthenticationReview() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

// POST /api/v1/reviews (pattern de l'énoncé)
async function submitReview(token, placeId, reviewText, rating) {
    const userId = getUserIdFromToken();

    const response = await fetch(`${API_BASE}/reviews`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            place_id: placeId,
            text:     reviewText,
            rating:   rating,
            user_id:  userId
        })
    });

    handleResponse(response);
}

// Handle review response (pattern de l'énoncé)
function handleResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!');
        const form = document.getElementById('review-form');
        if (form) form.reset();
    } else {
        alert('Failed to submit review');
    }
}

function initAddReviewPage() {
    // Check auth and redirect if not logged in (pattern de l'énoncé)
    const token = checkAuthenticationReview();
    const placeId = getPlaceIdFromURL();

    updateAuthUI();
    setupLogout();

    // Show place name in title
    if (placeId) {
        fetch(`${API_BASE}/places/${placeId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(r => r.json())
        .then(place => {
            const titleEl = document.getElementById('review-place-title');
            if (titleEl) titleEl.textContent = `Reviewing: ${place.title}`;
            document.title = `Add Review - ${place.title}`;
        })
        .catch(() => {});
    }

    // Review form (pattern de l'énoncé)
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review').value.trim();
            const rating     = parseInt(document.getElementById('rating').value);
            if (!reviewText) return;
            await submitReview(token, placeId, reviewText, rating);
        });
    }
}