"""
Management command: perform the initial Schwab OAuth flow and save the token.

Usage:
    python manage.py schwab_auth

This opens a browser for you to log in to Schwab.  After authorising the app,
copy the full redirect URL from your browser's address bar and paste it when
prompted.  The token is saved to SCHWAB_TOKEN_PATH (see settings.py) and will
be refreshed automatically on subsequent requests.
"""
import schwab
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Authenticate with the Schwab API and save the OAuth token."

    def handle(self, *args, **options):
        for setting in ("SCHWAB_API_KEY", "SCHWAB_APP_SECRET", "SCHWAB_CALLBACK_URL"):
            if not getattr(settings, setting, ""):
                self.stderr.write(
                    self.style.ERROR(f"{setting} is not configured. Set the environment variable.")
                )
                return

        self.stdout.write(f"Token will be saved to: {settings.SCHWAB_TOKEN_PATH}")
        self.stdout.write(f"Callback URL:           {settings.SCHWAB_CALLBACK_URL}")
        self.stdout.write("")

        try:
            schwab.auth.client_from_login_flow(
                api_key=settings.SCHWAB_API_KEY,
                app_secret=settings.SCHWAB_APP_SECRET,
                callback_url=settings.SCHWAB_CALLBACK_URL,
                token_path=settings.SCHWAB_TOKEN_PATH,
            )
            self.stdout.write(self.style.SUCCESS("Authentication successful — token saved."))
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"Authentication failed: {exc}"))
            raise SystemExit(1)
