"""Thin wrapper around schwab-py for fetching and normalizing option chains."""
import logging
from pathlib import Path

import schwab
from django.conf import settings

logger = logging.getLogger(__name__)


def get_client() -> schwab.client.Client:
    token_path = Path(settings.SCHWAB_TOKEN_PATH)
    if not token_path.exists():
        raise FileNotFoundError(
            f"Schwab token not found at {token_path}. "
            "Run:  python manage.py schwab_auth"
        )
    return schwab.auth.client_from_token_file(
        token_path=str(token_path),
        api_key=settings.SCHWAB_API_KEY,
        app_secret=settings.SCHWAB_APP_SECRET,
    )


def get_option_chain(symbol: str) -> tuple[list[dict], float]:
    """
    Return (options, underlying_price) for *symbol*.

    *options* is a flat list of normalized option dicts (one per contract).
    """
    client = get_client()
    response = client.get_option_chain(symbol.upper())
    response.raise_for_status()
    data = response.json()

    underlying_price: float = data.get("underlyingPrice", 0.0) or 0.0
    options: list[dict] = []

    for put_call, date_map in (
        ("CALL", data.get("callExpDateMap", {})),
        ("PUT", data.get("putExpDateMap", {})),
    ):
        for exp_key, strikes in date_map.items():
            # exp_key format: "YYYY-MM-DD:DTE"
            expiration = exp_key.split(":")[0]
            for strike_str, contracts in strikes.items():
                for raw in contracts:
                    options.append(_normalize(raw, underlying_price))

    logger.debug("Fetched %d contracts for %s", len(options), symbol)
    return options, underlying_price


def _normalize(raw: dict, underlying_price: float) -> dict:
    """Flatten a raw Schwab contract dict and add derived fields."""
    time_value: float = raw.get("timeValue") or 0.0
    tv_pct = (time_value / underlying_price * 100) if underlying_price > 0 else 0.0

    return {
        "symbol": raw.get("symbol", ""),
        "putCall": raw.get("putCall", ""),
        "strikePrice": raw.get("strikePrice", 0.0),
        "expirationDate": raw.get("expirationDate", ""),
        "daysToExpiration": raw.get("daysToExpiration", 0),
        "bid": raw.get("bid") or 0.0,
        "ask": raw.get("ask") or 0.0,
        "mark": raw.get("mark") or 0.0,
        "last": raw.get("last") or 0.0,
        "delta": raw.get("delta") or 0.0,
        "gamma": raw.get("gamma") or 0.0,
        "theta": raw.get("theta") or 0.0,
        "vega": raw.get("vega") or 0.0,
        "openInterest": raw.get("openInterest") or 0,
        "volume": raw.get("totalVolume") or 0,
        "timeValue": time_value,
        "timeValuePct": round(tv_pct, 4),
        "intrinsicValue": raw.get("intrinsicValue") or 0.0,
        "inTheMoney": bool(raw.get("inTheMoney")),
        "volatility": raw.get("volatility") or 0.0,
    }
