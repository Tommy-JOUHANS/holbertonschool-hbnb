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

// ============================================================
//  PAGINATION — style cercles avec ellipsis
// ============================================================
let allPlaces   = [];
let currentData = [];
const PAGE_SIZE = 9;
let currentPage = 1;

function renderPlacesPage(places, page) {
    const list = document.getElementById('places-list');
    if (!list) return;

    const start = (page - 1) * PAGE_SIZE;
    const slice = places.slice(start, start + PAGE_SIZE);

    list.innerHTML = '';
    slice.forEach(place => {
        const card = document.createElement('article');
        card.className     = 'place-card';
        card.dataset.price = place.price;
        card.innerHTML = `
            <h2>${place.title}</h2>
            <p>Price per night: $${place.price}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        list.appendChild(card);
    });

    renderPaginationControls(places, page);
}

function renderPaginationControls(places, page) {
    const container = document.getElementById('pagination');
    if (!container) return;

    const totalPages = Math.ceil(places.length / PAGE_SIZE);
    container.innerHTML = '';
    if (totalPages <= 1) return;

    // Crée un élément <a> style cercle
    function makeItem(label, targetPage, isActive, isDisabled, isEllipsis) {
        const a = document.createElement('a');
        a.textContent = label;
        a.href = '#!' + (isEllipsis ? '' : targetPage);

        if (isEllipsis) {
            a.className = 'cdp_i cdp-ellipsis';
        } else {
            a.className = 'cdp_i' + (isActive ? ' active' : '');
            if (!isDisabled) {
                a.addEventListener('click', (e) => {
                    e.preventDefault();
                    currentPage = targetPage;
                    renderPlacesPage(places, currentPage);
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                });
            } else {
                a.style.pointerEvents = 'none';
                a.style.opacity = '0.4';
            }
        }
        return a;
    }

    // Wrap CDP
    const cdp = document.createElement('div');
    cdp.className = 'cdp';
    cdp.setAttribute('actpage', page);

    // PREV
    cdp.appendChild(makeItem('prev', page - 1, false, page === 1, false));

    // Calcul des pages à afficher
    const pages = new Set([1, totalPages]);
    for (let i = Math.max(2, page - 2); i <= Math.min(totalPages - 1, page + 2); i++) {
        pages.add(i);
    }
    const sorted = [...pages].sort((a, b) => a - b);

    sorted.forEach((p, idx) => {
        if (idx > 0 && p - sorted[idx - 1] > 1) {
            cdp.appendChild(makeItem('...', null, false, false, true));
        }
        cdp.appendChild(makeItem(p, p, p === page, false, false));
    });

    // NEXT
    cdp.appendChild(makeItem('next', page + 1, false, page === totalPages, false));

    container.appendChild(cdp);
}

function displayPlaces(places) {
    const list = document.getElementById('places-list');
    if (!list) return;

    if (!places.length) {
        list.innerHTML = '<p style="text-align:center;color:#888;">No places available.</p>';
        return;
    }

    // Tri : dernière publication en haut, première en bas
    places.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

    allPlaces   = places;
    currentData = places;
    currentPage = 1;
    renderPlacesPage(currentData, currentPage);
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

    // Filtre prix
    const filter = document.getElementById('price-filter');
    if (filter) {
        filter.addEventListener('change', (e) => {
            const selected = e.target.value;
            currentData = selected === 'all'
                ? allPlaces
                : allPlaces.filter(p => parseFloat(p.price) <= parseFloat(selected));

            currentPage = 1;

            if (!currentData.length) {
                document.getElementById('places-list').innerHTML =
                    '<p style="text-align:center;color:#888;">No places match this filter.</p>';
                const pag = document.getElementById('pagination');
                if (pag) pag.innerHTML = '';
            } else {
                renderPlacesPage(currentData, currentPage);
            }
        });
    }
}

// ============================================================
//  PLACE DETAILS PAGE
// ============================================================
function getPlaceIdFromURL() {
    return new URLSearchParams(window.location.search).get('id');
}

// Fetch place + amenities + host
async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        };

        // 1. Détails de la place
        const placeRes = await fetch(`${API_BASE}/places/${placeId}`, { headers });
        if (!placeRes.ok) throw new Error(placeRes.statusText);
        const place = await placeRes.json();

        // 2. Amenities séparées si absentes
        if (!place.amenities || place.amenities.length === 0) {
            try {
                const amenRes = await fetch(`${API_BASE}/places/${placeId}/amenities`, { headers });
                if (amenRes.ok) place.amenities = await amenRes.json();
            } catch {}
        }

        // 3. Host — cherche l'ID du propriétaire dans la place
        const ownerId = place.owner_id || place.host_id || place.user_id;
        if (ownerId && !place.host && !place.owner) {
            try {
                const userRes = await fetch(`${API_BASE}/users/${ownerId}`, { headers });
                if (userRes.ok) place.host = await userRes.json();
            } catch {}
        }

        // 4. Reviews séparées si absentes dans l'objet place
        if (!place.reviews || place.reviews.length === 0) {
            try {
                const revRes = await fetch(`${API_BASE}/places/${placeId}/reviews`, { headers });
                if (revRes.ok) place.reviews = await revRes.json();
            } catch {}
        }

        // 5. Pour chaque review, charge le nom de l'auteur via user_id
        if (place.reviews && place.reviews.length > 0) {
            await Promise.all(place.reviews.map(async (review) => {
                if (!review.user && review.user_id) {
                    try {
                        const userRes = await fetch(`${API_BASE}/users/${review.user_id}`, { headers });
                        if (userRes.ok) review.user = await userRes.json();
                    } catch {}
                }
            }));
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

        // HOST — chargé via fetchPlaceDetails dans place.host
        let hostName = 'N/A';
        const hostObj = place.host || place.owner;
        if (hostObj && typeof hostObj === 'object') {
            hostName = `${hostObj.first_name ?? ''} ${hostObj.last_name ?? ''}`.trim() || 'N/A';
        } else if (typeof hostObj === 'string') {
            hostName = hostObj;
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

                // user peut être un objet {first_name, last_name}
                // ou absent (API retourne seulement user_id)
                let userName = 'Anonymous';
                if (r.user && typeof r.user === 'object') {
                    userName = r.user.first_name ?? r.user.name ?? 'Anonymous';
                } else if (r.user_name) {
                    userName = r.user_name;
                }

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

// Étape 1 — Vérifie l'authentification (pattern de l'énoncé)
// Si pas de token → redirige vers index.html
function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

// Étape 4 — POST /api/v1/reviews avec token + body JSON
// user_id est requis par l'API Flask (review_model validate=True)
// On le récupère depuis le token JWT
async function submitReview(token, placeId, reviewText, rating) {
    try {
        // Décode le user_id depuis le payload JWT
        const payload  = JSON.parse(atob(token.split('.')[1]));
        const userId   = payload.sub || payload.identity;

        const response = await fetch(`${API_BASE}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type':  'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text:     reviewText,
                rating:   rating,
                user_id:  userId   // ← requis par review_model Flask
            })
        });
        // Étape 5 — gère la réponse
        const data = await response.json().catch(() => null);
        handleResponse(response, data);
    } catch (err) {
        alert('Network error: ' + err.message);
    }
}

// Étape 5 — Succès : message + reset + redirect | Échec : message erreur
function handleResponse(response, data) {
    if (response.ok) {
        alert('Review submitted successfully!');
        const form = document.getElementById('review-form');
        if (form) form.reset();
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            window.location.href = `place.html?id=${placeId}`;
        }
    } else {
        const msg = data?.message || data?.error || `Error ${response.status}`;
        alert('Failed to submit review: ' + msg);
    }
}

// Point d'entrée add_review.html
function initAddReviewPage() {
    // Étape 1 — auth check (redirige si non connecté)
    const token = checkAuthentication();
    // Étape 2 — place ID depuis l'URL
    const placeId = getPlaceIdFromURL();

    updateAuthUI();
    setupLogout();

    // Affiche le nom de la place dans le titre
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

    // Étape 3 — event listener sur le formulaire
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review').value.trim();
            const ratingVal  = document.getElementById('rating').value;
            const rating     = parseInt(ratingVal);

            // Validation côté client
            if (!reviewText) {
                alert('Please write a review.');
                return;
            }
            if (!ratingVal || isNaN(rating)) {
                alert('Please select a rating.');
                return;
            }
            // Étape 4 — requête AJAX
            await submitReview(token, placeId, reviewText, rating);
        });
    }
}