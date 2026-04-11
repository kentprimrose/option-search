import json
import logging

from django.shortcuts import render

from .criteria import filters  # noqa: F401 — registers all built-in criteria
from .criteria.base import get_all_criteria
from .schwab_client import get_option_chain

logger = logging.getLogger(__name__)

_SORT_FIELDS: dict[str, tuple[str, bool]] = {
    "strike": ("strikePrice", False),
    "expiration": ("expirationDate", False),
    "dte": ("daysToExpiration", False),
    "delta": ("delta", False),
    "tv_pct": ("timeValuePct", False),
    "mark": ("mark", False),
    "oi": ("openInterest", True),
}


def index(request):
    criteria = get_all_criteria()
    context = {
        "criteria": criteria,
        "form_data": {},
        "form_data_json": "{}",
        "error": None,
        "options": None,
        "underlying_price": None,
        "symbol": "",
        "sort_by": "strike",
        "result_count": 0,
        "sort_options": list(_SORT_FIELDS.keys()),
    }

    if request.method != "POST":
        return render(request, "screener/index.html", context)

    form_data = request.POST
    symbol = form_data.get("symbol", "").strip().upper()
    sort_by = form_data.get("sort_by", "strike")

    context["form_data"] = form_data
    context["form_data_json"] = json.dumps(form_data.dict())
    context["symbol"] = symbol
    context["sort_by"] = sort_by

    if not symbol:
        context["error"] = "Please enter a ticker symbol."
        return render(request, "screener/index.html", context)

    try:
        options, underlying_price = get_option_chain(symbol)
        context["underlying_price"] = underlying_price

        for criterion in criteria:
            if criterion.is_enabled(form_data):
                options = criterion.apply(options, underlying_price, form_data)

        sort_field, reverse = _SORT_FIELDS.get(sort_by, ("strikePrice", False))
        options.sort(key=lambda o: o.get(sort_field) or 0, reverse=reverse)

        context["options"] = options
        context["result_count"] = len(options)
    except FileNotFoundError as exc:
        context["error"] = str(exc)
    except Exception as exc:
        logger.exception("Error fetching options for %s", symbol)
        context["error"] = f"Error fetching options for {symbol}: {exc}"

    return render(request, "screener/index.html", context)
