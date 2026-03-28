# HBnB Evolution — Part 4: Frontend
### Authors: Tommy Jouhans & James Roussel


## Prerequisites

- Flask API (Part 3) running at `http://127.0.0.1:5000`
- A modern browser
- A static file server (e.g., `python3 -m http.server 5500`)

## Launch the project
```bash
# In the backend folder (Part 3)
python -m hbnb.run

# In the frontend folder (this folder)
python3 -m http.server 5500
# Then open http://localhost:5500/index.html
```

## Task 2 — Test the connection

1. Open `http://localhost:5500/login.html`
2. Enter an email/password for a user created via the API
3. **Success**: redirection When redirecting to `index.html`, the Login button disappears.

4. **Failure**: Red error message displayed below the form.
5. To log out: Click "Logout" in the header.
6. Check the cookie in DevTools → Application → Cookies → `token`.

## Task 5 — Test adding a review

1. Log in (see Task 2).
2. From `index.html`, click "View Details" for a location.
3. Click the comment icon → redirects to `add_review.html?id=<uuid>`.
4. Fill in the text and select a rating (1 to 5 stars).
5. **Success**: Green message + automatic redirection to the location's page.
6. **Failure**: Red error message displayed below the form.
7. **Without token**: Automatic redirection to `index.html`.

## File Structure

| File | Role |

|---|---|

| `index.html` | List of locations with price filter and pagination |

| `login.html` | JWT login form |

| `place.html` | Location details + reviews |

| `add_review.html` | Review submission form |

| `scripts.js` | All JavaScript logic (routing, API, DOM) |

| `styles.css` | Global styles shared across the 4 pages |