# Option Search

A Django-based web application for screening stock options using the Schwab API. This tool allows users to fetch option chains for specific tickers and apply various filters to find contracts that meet specific criteria.

## Project Overview

- **Purpose:** Provide a web interface for filtering and screening stock options.
- **Main Technologies:**
    - **Backend:** Python 3.x, [Django](https://www.djangoproject.com/)
    - **API Integration:** [schwab-py](https://github.com/sinon78/schwab-py) for interacting with the Schwab API.
    - **Frontend:** Django Templates with CSS (likely styled within `screener/templates/`).
- **Architecture:** 
    - The project core is in `option_search/`.
    - The main application logic resides in `screener/`.
    - A modular "Criteria" system allows for easy addition of new screening filters (`screener/criteria/`).

## Building and Running

### Prerequisites
- Python 3.10+
- A Schwab Developer account with API credentials.

### Installation
1.  **Clone the repository** (if not already in it).
2.  **Install dependencies:**
    ```bash
    pip install django schwab-py
    # Or if a requirements.txt is provided in the root:
    # pip install -r requirements.txt
    ```
3.  **Configure Environment Variables:**
    Set the following variables in your environment or a `.env` file:
    - `DJANGO_SECRET_KEY`: Your Django secret key.
    - `SCHWAB_API_KEY`: Your Schwab App Key.
    - `SCHWAB_APP_SECRET`: Your Schwab App Secret.
    - `SCHWAB_CALLBACK_URL`: Your Schwab App Redirect URI (default: `https://127.0.0.1:8182`).
    - `SCHWAB_TOKEN_PATH`: Path where the OAuth token will be stored (default: `~/.schwab_token.json`).

### Setup & Authentication
1.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```
2.  **Authenticate with Schwab:**
    ```bash
    python manage.py schwab_auth
    ```
    Follow the prompts in the terminal to complete the OAuth flow.

### Running the Application
```bash
python manage.py runserver
```
Access the application at `http://127.0.0.1:8000/`.

## Development Conventions

### Adding New Screening Criteria
The application uses a registry-based system for filters. To add a new criterion:
1.  **Subclass `Criterion`** in `screener/criteria/filters.py` (or a new module in that directory).
2.  **Decorate the class** with `@register`.
3.  **Implement required methods:**
    - `form_fields()`: Define the parameters for the filter.
    - `apply()`: The logic to filter the list of options.
4.  **Registration:** Ensure the module is imported in `screener/criteria/__init__.py`.

### Code Style
- Follow PEP 8 guidelines.
- Use the `register` decorator for all new screening criteria to ensure they appear in the UI automatically.
- Logging is configured for the `screener` app; use `logger.debug()` for detailed execution logs.

## Directory Structure
- `option_search/`: Project configuration and settings.
- `screener/`: Main application logic.
    - `management/commands/`: Custom Django commands (e.g., `schwab_auth`).
    - `criteria/`: Logic for option screening filters.
    - `templates/`: HTML templates for the UI.
    - `schwab_client.py`: Wrapper for the Schwab API client.
