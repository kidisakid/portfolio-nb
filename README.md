# Neo Balignasay — Portfolio

A Django + vanilla JS portfolio with parallax / 3D interactions, featuring a live-embedded Streamlit demo of the RDB App built during my Rythmos DB internship.

## Stack

- **Django 5** — templating, static file serving, routing
- **WhiteNoise** — compressed static files in production
- **Gunicorn** — WSGI server
- **Streamlit** (sidecar) — embedded RDB App demo
- **Vanilla CSS + JS** — parallax, 3D tilt, scroll reveal

## Local development

```bash
# 1. Install site deps
cd portfolio_site
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Run migrations + collect static
python manage.py migrate
python manage.py collectstatic --no-input

# 3. Start Django
DJANGO_DEBUG=True python manage.py runserver
#   → http://localhost:8000

# 4. In a second terminal, start the Streamlit demo
cd portfolio_site/rdb_demo
pip install -r requirements.txt
streamlit run app.py
#   → http://localhost:8501
```

The Django site embeds Streamlit via `<iframe>` pointing at
`STREAMLIT_URL` (default `http://localhost:8501`).

## Deployment to Render (free tier)

Both services are defined in [`render.yaml`](./render.yaml). Push the
repo to GitHub and use Render's "Blueprint" feature:

1. New → Blueprint → connect your repo
2. Render reads `render.yaml` and provisions **two free web services**:
   - `neo-portfolio` (Django) — served at `neo-portfolio.onrender.com`
   - `neo-portfolio-rdb` (Streamlit) — served at `neo-portfolio-rdb.onrender.com`
3. The Django service has `STREAMLIT_URL` pointed at the Streamlit
   service, so the `<iframe>` embeds resolve automatically.

> **Note on free-tier cold starts.** Render free services sleep after 15
> minutes idle. First request takes ~30s to wake. The embedded iframe has
> a loading spinner to cover this.

## File layout

```
portfolio_site/
├── config/              # Django project (settings, urls, wsgi)
├── main/                # Portfolio app (views, context)
├── templates/index.html # Single-page layout
├── static/
│   ├── css/styles.css   # Parallax + 3D styles
│   ├── js/main.js       # rAF parallax + tilt + reveal
│   ├── img/             # headshot, cert, mcy screenshot
│   └── docs/            # resume PDF
├── rdb_demo/            # Streamlit sidecar service
│   ├── app.py
│   └── requirements.txt
├── requirements.txt     # Django deps
├── build.sh             # Render build command
├── render.yaml          # Two-service blueprint
└── Procfile             # Fallback for non-blueprint deploys
```

## Environment variables

| Var                     | Purpose                                | Default                    |
|-------------------------|----------------------------------------|----------------------------|
| `DJANGO_SECRET_KEY`     | Django signing key                     | dev placeholder            |
| `DJANGO_DEBUG`          | `"True"` or `"False"`                  | `False`                    |
| `DJANGO_ALLOWED_HOSTS`  | Comma-separated hostnames              | `.onrender.com, localhost` |
| `DJANGO_CSRF_TRUSTED`   | Comma-separated origins                | `https://*.onrender.com`   |
| `STREAMLIT_URL`         | URL the iframe points to               | `http://localhost:8501`    |

## Accessibility

- Respects `prefers-reduced-motion` — all parallax + tilt + reveal animations become static.
- Semantic HTML landmarks (`nav`, `section`, `footer`).
- Link + button focus states maintained.

— Built end-to-end, April 2026.
