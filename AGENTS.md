# AGENTS.md — project context and development guidelines for AI coding agents

## Project Overview

option-search is a Django web application that lets a user enter a stock ticker symbol, select screening criteria, and view the matching options contracts fetched live from the Schwab brokerage API.

## Directory Layout

```
option-search/
  AGENTS.md               — this file
  pyproject.toml          — package metadata (name: option-search)
  requirements            — runtime Python dependencies (plain text, one per line)
  requirements_dev        — development-only Python dependencies
  src/
    manage.py             — Django management entry point
    option_search/        — Django project package (settings, root URLs, WSGI)
      settings.py         — all config driven by environment variables (see below)
      urls.py             — root URL conf; includes screener.urls
      wsgi.py
    screener/             — the single Django app
      views.py            — one view (index) handles GET and POST
      urls.py
      schwab_client.py    — thin wrapper around schwab-py; fetches & normalises
                            option chains from the Schwab API
      criteria/
        base.py           — Criterion base class, FormField, and the @register
                            decorator / registry
        filters.py        — all built-in screening criteria (register new ones here)
        __init__.py       — imports filters so criteria are registered at startup
      templates/screener/
        index.html        — Bootstrap 5 single-page UI (form + results table)
      management/commands/
        schwab_auth.py    — `manage.py schwab_auth` runs the OAuth login flow
```

## Key Concepts

### Criteria system

Each screening criterion is a class that subclasses `Criterion` (`criteria/base.py`) and is decorated with `@register`. The decorator adds it to a module-level registry dict keyed by `criterion.id`. The view calls `get_all_criteria()` to retrieve every registered criterion, renders their `form_fields()` in the UI, and calls their `apply()` method in sequence when the form is submitted.

To add a new criterion:
1. Open `src/screener/criteria/filters.py`.
2. Subclass `Criterion`, set `id`/`name`/`description`, implement `form_fields()` and `apply(options, underlying_price, form_data)`.
3. Decorate the class with `@register`.

That is all — no further wiring is needed.

### Schwab authentication

The app reads from a token file (`SCHWAB_TOKEN_PATH`, default `~/.schwab_token.json`). Run the one-time OAuth flow with:

```sh
python src/manage.py schwab_auth
```

The schwab-py library handles token refresh automatically thereafter.

### Environment variables

All optional during development; set via `.envrc` (direnv).

| Variable | Description | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django secret key | insecure dev value |
| `DJANGO_DEBUG` | `"true"` / `"false"` | `"true"` |
| `DJANGO_ALLOWED_HOSTS` | Space-separated hostnames | `localhost 127.0.0.1` |
| `SCHWAB_API_KEY` | Schwab developer app API key | — |
| `SCHWAB_APP_SECRET` | Schwab developer app secret | — |
| `SCHWAB_CALLBACK_URL` | OAuth redirect URL | `https://127.0.0.1` |
| `SCHWAB_TOKEN_PATH` | Path to stored OAuth token JSON | `~/.schwab_token.json` |

## Development Guidelines

### Running the dev server

```sh
cd src
python manage.py runserver
```

### Adding or updating Python dependencies

1. Add the package (with a version pin if appropriate) to `requirements` for runtime dependencies, or `requirements_dev` for development-only ones.
2. Run the `pup` alias to install and sync the environment:
   ```sh
   find . \( -name "requirements*" -o -name "py-reqs*" \) -exec pip install --upgrade -Ur {} \;
   ```

Do **not** install packages directly with pip or uv outside of this workflow.

### Code style

- Follow PEP 8. Keep lines under 100 characters.
- Type annotations are not required, but are welcome on new public APIs.
- Do not add docstrings or comments to code you did not write or change.
- Prefer editing existing files over creating new ones.

### Templates

- The single template is `src/screener/templates/screener/index.html`.
- It uses Bootstrap 5 loaded from CDN — no build step required.
- Keep JavaScript minimal and inline; no bundler is in use.

### Django conventions

- There is no database; no models, migrations, or `django.contrib.auth` are used.
- All configuration comes from environment variables (see `settings.py`).
- The app has no media or user-uploaded files.
