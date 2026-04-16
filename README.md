# option-search

A Django web app for screening options chains using the [Schwab API](https://developer.schwab.com/).

## Features

- Fetch live option chains for any ticker via the Schwab brokerage API
- Filter results by option type, moneyness, DTE, delta, open interest, strike range, and time value %
- Sort results by strike, expiration, DTE, delta, time value %, mark, or open interest
- Extensible criteria system — add new filters by subclassing `Criterion`

## Requirements

- Python 3.9+
- A Schwab developer account with an app registered at [developer.schwab.com](https://developer.schwab.com/)

## Setup

Install dependencies:

```sh
pup
```

Set required environment variables:

```sh
export SCHWAB_API_KEY=your_api_key
export SCHWAB_APP_SECRET=your_app_secret
export SCHWAB_CALLBACK_URL=https://127.0.0.1:8182   # must match your app registration
```

Authenticate with Schwab (one-time OAuth flow):

```sh
python src/manage.py schwab_auth
```

This opens a browser login, then prompts you to paste the redirect URL. The token is saved to `~/.schwab_token.json` and refreshed automatically on subsequent requests.

## Running

```sh
python src/manage.py runserver
```

Open `http://localhost:8000` in your browser.

## Configuration

All settings are environment-variable driven:

| Variable | Default | Description |
|---|---|---|
| `SCHWAB_API_KEY` | *(required)* | Schwab app API key |
| `SCHWAB_APP_SECRET` | *(required)* | Schwab app secret |
| `SCHWAB_CALLBACK_URL` | `https://127.0.0.1:8182` | OAuth redirect URL |
| `SCHWAB_TOKEN_PATH` | `~/.schwab_token.json` | Token file location |
| `DJANGO_SECRET_KEY` | insecure default | Django secret key (set in production) |
| `DJANGO_DEBUG` | `true` | Enable debug mode |
| `DJANGO_ALLOWED_HOSTS` | `localhost 127.0.0.1` | Space-separated allowed hosts |

## Adding Criteria

Subclass `Criterion` in `src/screener/criteria/filters.py` and apply `@register`:

```python
from .base import Criterion, FormField, register

@register
class MyFilter(Criterion):
    id = "my_filter"
    name = "My Filter"
    description = "What this filter does."

    def form_fields(self):
        return [FormField(name=self.field_name("value"), label="Value", field_type="number", default=0)]

    def apply(self, options, underlying_price, form_data):
        value = float(form_data.get(self.field_name("value"), 0))
        return [o for o in options if o["someField"] >= value]
```

The filter will appear automatically in the UI.
