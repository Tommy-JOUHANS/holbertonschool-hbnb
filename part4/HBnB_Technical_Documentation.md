# HBnB Evolution — Part 4: Simple Web Client

**Authors:** Tommy Jouhans & James Roussel

---

## Prerequisites

- Flask API (Part 3) running at `http://127.0.0.1:5000`
- A modern browser (Chrome, Firefox, Edge)
- A static file server — e.g. `python3 -m http.server 5500`

## Launch the Project

```bash
# 1. Start the backend (Part 3 folder)
python -m hbnb.run

# 2. Start the frontend static server (this folder)
python3 -m http.server 5500

# 3. Open in your browser
http://localhost:5500/index.html
```

---

## Task 0 — Design

### HTML Structure

The project contains **4 HTML pages**, each sharing the same header/footer layout:

| File | Page |
|---|---|
| `index.html` | List of places |
| `login.html` | Login form |
| `place.html` | Place details + reviews |
| `add_review.html` | Add a review form |

Every page includes:
- A `<header>` with the HBnB logo and a Login/Logout navigation link
- A `<main>` section with page-specific content
- A `<footer>` with copyright notice
- Links to the shared `styles.css` and `scripts.js`

### CSS Styles

All styles are defined in `styles.css` and shared across all pages:
- **Header/Footer** — orange background (`#FF9F43`), white text
- **Place cards** — white cards with border, shadow, and "View Details" button
- **Review cards** — white cards with author name, comment, and star rating
- **Forms** — login form and review form with consistent input styling
- **Pagination** — circular orange buttons with ellipsis for large datasets
- **Feedback messages** — `.error-msg` (red) and `.success-msg` (green) for inline validation
- **Accessibility** — `.visually-hidden` class for screen-reader-only headings

### Code Quality

- All HTML pages are **W3C valid** (no warnings or errors)
- `<section>` elements are only used where a visible heading exists; dynamic containers use `<div>`
- Classes and IDs follow a consistent naming convention across all files

---

## Task 1 — Login

### How it Works

The login page (`login.html`) authenticates the user against the Flask API and stores the JWT token as a browser cookie.

**Relevant function in `scripts.js`:** `loginUser()`, `initLoginPage()`

```
POST /api/v1/auth/login
Body: { "email": "...", "password": "..." }
Response: { "access_token": "<JWT>" }
```

The token is stored as:
```
document.cookie = `token=<JWT>; path=/`
```

### How to Test

1. Open `http://localhost:5500/login.html`
2. Enter the email and password of a user created via the API
3. Click **Login**

**Success:** Redirected to `index.html` — the Login button in the header disappears (replaced by Logout)

**Failure:** A red error message appears below the form — no page reload

4. To log out: click **Logout** in the header — the cookie is deleted and you are redirected to `index.html`
5. To verify the token: open DevTools → **Application** → **Cookies** → look for `token`

### Code Notes

- If the user is already logged in, visiting `login.html` redirects immediately to `index.html`
- Error handling uses `showMessage('login-error', ...)` — no `alert()` anywhere
- The form submission is handled with `addEventListener('submit', ...)` and `async/await`

---

## Task 2 — View Index

### How it Works

The index page (`index.html`) fetches all places from the API and displays them as cards. Two client-side filters allow the user to narrow results without any additional API call.

**Relevant functions in `scripts.js`:** `fetchPlaces()`, `displayPlaces()`, `renderPlacesPage()`, `initIndexPage()`

```
GET /api/v1/places
Headers: Authorization: Bearer <token>  (if logged in)
```

### How to Test

1. Open `http://localhost:5500/index.html`
2. Places are loaded and displayed automatically as cards (title + price per night + "View Details" button)
3. Use the **Max Price** filter to show only places within a price range — updates instantly, no reload
4. Use the **City** filter to show only places in a specific city — populated dynamically from the API data
5. Both filters can be combined

**Login link visibility:**
- Not logged in → Login button is visible in the header
- Logged in → Login button is hidden, Logout is shown instead

**Pagination:** If more than 9 places are returned, circular pagination controls appear at the bottom with ellipsis for large page counts.

### Code Notes

- Places are sorted by creation date (most recent first)
- Filtering is purely client-side — `allPlaces` is the full dataset, `currentData` is the filtered view
- If no places match the active filters, a friendly message is shown instead of an empty page

---

## Task 3 — View Place Details

### How it Works

The place details page (`place.html`) loads full information for a specific place using its ID from the URL query parameter (`?id=<uuid>`). It makes multiple sequential API calls to assemble all the data.

**Relevant functions in `scripts.js`:** `fetchPlaceDetails()`, `displayPlaceDetails()`, `initPlacePage()`

```
GET /api/v1/places/<id>           → place info
GET /api/v1/places/<id>/amenities → amenities (if not included)
GET /api/v1/users/<owner_id>      → host name
GET /api/v1/places/<id>/reviews   → reviews (if not included)
GET /api/v1/users/<user_id>       → review author names
```

### How to Test

1. From `index.html`, click **View Details** on any place card
2. The page displays: host name, price per night, description, amenities, and all reviews with star ratings

**Add a Review button:**
- Not logged in → the "Add a Review" section is **hidden**
- Logged in → the "Write a Review" button is **visible** and links to `add_review.html?id=<uuid>`

**Invalid place ID:** If the URL contains an unknown ID, an error message is displayed inside the `#place-details` container.

### Code Notes

- All API calls use `null`-safe fallbacks (`??`, optional chaining) to handle missing fields gracefully
- Host name is resolved from `owner_id`, `host_id`, or `user_id` depending on the API response shape
- Amenities support both string arrays and object arrays (`{ name: "..." }`)
- Review authors are loaded in parallel using `Promise.all()`

---

## Task 4 — Add Review

### How it Works

The add review page (`add_review.html`) allows a logged-in user to submit a review for a specific place. The place ID is read from the URL query parameter (`?id=<uuid>`).

**Relevant functions in `scripts.js`:** `checkAuthentication()`, `submitReview()`, `handleResponse()`, `initAddReviewPage()`

```
POST /api/v1/reviews
Headers: Authorization: Bearer <token>
Body: {
  "place_id": "<uuid>",
  "text": "...",
  "rating": 1–5,
  "user_id": "<uuid>"   ← decoded from JWT payload
}
```

The `user_id` is extracted client-side by decoding the JWT payload:
```js
const payload = JSON.parse(atob(token.split('.')[1]));
const userId  = payload.sub || payload.identity;
```

### How to Test

1. Log in (see Task 2)
2. From `index.html`, click **View Details** on a place
3. Click **Write a Review** — you are redirected to `add_review.html?id=<uuid>`
4. Fill in your review text and select a star rating (1 to 5)
5. Click **Submit Review**

**Success:** A green message appears — "Review successfully sent!" — then you are automatically redirected back to the place page after 1.5 seconds

**Failure (API error):** A red error message appears below the form with the specific error detail

**Validation errors:**
- Empty review text → red message: "Please write a review before submitting."
- No rating selected → red message: "Please select a rating."

**Without a valid token:** Redirected immediately to `index.html` (no form is shown)

**Corrupted JWT:** If the token cannot be decoded, a red message appears and the user is redirected to `login.html` after 2 seconds

### Code Notes

- `checkAuthentication()` is called first — the page never renders for unauthenticated users
- JWT decoding is wrapped in its own `try/catch` block, separate from the network request
- All error and success feedback uses `showMessage()` — zero `alert()` calls in the entire project
- The form is reset after a successful submission before the redirect

---

## File Structure

| File | Role |
|---|---|
| `index.html` | List of places with price/city filters and pagination |
| `login.html` | JWT authentication form |
| `place.html` | Place details, reviews, and add-review access |
| `add_review.html` | Review submission form |
| `scripts.js` | All JavaScript logic: routing, API calls, DOM updates |
| `styles.css` | Global styles shared across all 4 pages |
| `images/` | Logo, favicon, and UI icons |