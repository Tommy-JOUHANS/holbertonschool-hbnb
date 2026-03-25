document.addEventListener('DOMContentLoaded', () => {
  updateAuthUI();
  setupLogout();
  const path = window.location.pathname;
  if      (path.endsWith('login.html'))      initLoginPage();
  else if (path.endsWith('index.html') || path === '/' || path.endsWith('/')) initIndexPage();
  else if (path.endsWith('place.html'))      initPlacePage();
  else if (path.endsWith('add_review.html')) initAddReviewPage();
});

// ============================================================
//  SAMPLE DATA  (replace with real API calls when ready)
// ============================================================
const PLACES = [
    {
        id: 1,
        name: 'Beautiful Beach House',
        price: 150,
        host: 'John Doe',
        description: 'A beautiful beach house with amazing views...',
        amenities: ['WiFi', 'Pool', 'Air Conditioning'],
        reviews: [
            { user: 'Jane Smith',   text: 'Great place to stay!',                rating: 4 },
            { user: 'Robert Brown', text: 'Amazing location and very comfortable.', rating: 5 }
        ]
    },
    {
        id: 2,
        name: 'Cozy Cabin',
        price: 100,
        host: 'Alice Martin',
        description: 'A cozy cabin in the woods, perfect for a quiet retreat.',
        amenities: ['WiFi', 'Fireplace', 'Parking'],
        reviews: [
            { user: 'Tom Lee', text: 'Super peaceful and warm!', rating: 5 }
        ]
    },
    {
        id: 3,
        name: 'Modern Apartment',
        price: 200,
        host: 'Bob Wilson',
        description: 'A sleek modern apartment in the city centre.',
        amenities: ['WiFi', 'Gym', 'Rooftop'],
        reviews: []
    }
];
 
// ============================================================
//  AUTH HELPERS
// ============================================================
function isLoggedIn() {
    return !!localStorage.getItem('user_token');
}
 
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
            localStorage.removeItem('user_token');
            window.location.href = 'index.html';
        }
    });
}
 
// ============================================================
//  STAR RENDERING
// ============================================================
function renderStars(rating) {
    const full  = '★';
    const empty = '☆';
    return full.repeat(rating) + empty.repeat(5 - rating);
}
 
// ============================================================
//  INDEX PAGE
// ============================================================
function initIndexPage() {
    const list    = document.getElementById('places-list');
    const filter  = document.getElementById('price-filter');
    if (!list || !filter) return;
 
    function renderPlaces(maxPrice) {
        list.innerHTML = '';
        const filtered = maxPrice === 'all'
            ? PLACES
            : PLACES.filter(p => p.price <= parseInt(maxPrice));
 
        if (filtered.length === 0) {
            list.innerHTML = '<p style="text-align:center;color:#888;">No places match this price filter.</p>';
            return;
        }
 
        filtered.forEach(place => {
            const card = document.createElement('article');
            card.className = 'place-card';
            card.innerHTML = `
                <h2>${place.name}</h2>
                <p>Price per night: $${place.price}</p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            `;
            list.appendChild(card);
        });
    }
 
    renderPlaces('all');
 
    filter.addEventListener('change', () => {
        renderPlaces(filter.value);
    });
}
 
// ============================================================
//  PLACE DETAILS PAGE
// ============================================================
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return parseInt(params.get('id'));
}
 
function initPlacePage() {
    const placeId      = getPlaceIdFromURL();
    const place        = PLACES.find(p => p.id === placeId);
    const titleEl      = document.getElementById('place-title');
    const detailsEl    = document.getElementById('place-details');
    const reviewsEl    = document.getElementById('reviews');
    const addReviewEl  = document.getElementById('add-review');
 
    if (!place) {
        if (detailsEl) detailsEl.innerHTML = '<p>Place not found.</p>';
        return;
    }
 
    // Title
    if (titleEl) titleEl.textContent = place.name;
    document.title = place.name;
 
    // Details card
    if (detailsEl) {
        detailsEl.innerHTML = `
            <p class="place-info"><strong>Host:</strong> ${place.host}</p>
            <p class="place-info"><strong>Price per night:</strong> $${place.price}</p>
            <p class="place-info"><strong>Description:</strong> ${place.description}</p>
            <p class="place-info"><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
        `;
    }
 
    // Reviews
    if (reviewsEl) {
        const heading = reviewsEl.querySelector('h2') || (() => {
            const h = document.createElement('h2');
            reviewsEl.prepend(h);
            return h;
        })();
        heading.textContent = 'Reviews';
 
        if (place.reviews.length === 0) {
            reviewsEl.innerHTML += '<p style="color:#888;">No reviews yet.</p>';
        } else {
            place.reviews.forEach(r => {
                const card = document.createElement('article');
                card.className = 'review-card';
                card.innerHTML = `
                    <h3>${r.user}:</h3>
                    <p>${r.text}</p>
                    <p>Rating: ${renderStars(r.rating)}</p>
                `;
                reviewsEl.appendChild(card);
            });
        }
    }
 
    // Show add-review section only if logged in
    if (addReviewEl) {
        if (!isLoggedIn()) {
            addReviewEl.style.display = 'none';
        } else {
            const form = document.getElementById('review-form');
            if (form) {
                form.addEventListener('submit', (e) => {
                    e.preventDefault();
                    const text   = document.getElementById('review-text').value.trim();
                    const rating = parseInt(document.getElementById('rating').value);
                    if (!text) return;
 
                    const card = document.createElement('article');
                    card.className = 'review-card';
                    card.innerHTML = `
                        <h3>You:</h3>
                        <p>${text}</p>
                        <p>Rating: ${renderStars(rating)}</p>
                    `;
                    reviewsEl.appendChild(card);
                    form.reset();
                    alert('Review submitted!');
                });
            }
        }
    }
}
 
// ============================================================
//  LOGIN PAGE
// ============================================================
function initLoginPage() {
    const form = document.getElementById('login-form');
    if (!form) return;
 
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const email    = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
 
        // Simulated auth — replace with real API call
        if (email && password.length >= 4) {
            localStorage.setItem('user_token', btoa(email));
            window.location.href = 'index.html';
        } else {
            alert('Invalid credentials. Password must be at least 4 characters.');
        }
    });
}
 
// ============================================================
//  ADD REVIEW PAGE (standalone add_review.html)
// ============================================================
function initAddReviewPage() {
    // Redirect if not logged in
    if (!isLoggedIn()) {
        window.location.href = 'login.html';
        return;
    }
 
    // Show place name in title if id provided
    const placeId   = getPlaceIdFromURL();
    const place     = PLACES.find(p => p.id === placeId);
    const titleEl   = document.getElementById('review-place-title');
    if (titleEl && place) {
        titleEl.textContent = `Reviewing: ${place.name}`;
        document.title = `Add Review - ${place.name}`;
    }
 
    const form = document.getElementById('review-form');
    if (!form) return;
 
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const text   = document.getElementById('review').value.trim();
        const rating = document.getElementById('rating').value;
        if (!text) return;
 
        // In a real app, send to API here
        alert(`Review submitted!\nRating: ${rating} star(s)\n"${text}"`);
        form.reset();
        window.location.href = place ? `place.html?id=${place.id}` : 'index.html';
    });
}
 