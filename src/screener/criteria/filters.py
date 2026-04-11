"""
Built-in screening criteria.

Add new criteria here (or in any module imported by ``criteria/__init__.py``)
by subclassing ``Criterion`` and applying the ``@register`` decorator.
"""
from .base import Criterion, FormField, register


@register
class OptionTypeFilter(Criterion):
    id = "option_type"
    name = "Option Type"
    description = "Show only puts, only calls, or both."

    def form_fields(self):
        return [
            FormField(
                name=self.field_name("type"),
                label="Type",
                field_type="select",
                default="PUT",
                choices=[
                    ("ALL", "All"),
                    ("PUT", "Puts only"),
                    ("CALL", "Calls only"),
                ],
            )
        ]

    def apply(self, options, underlying_price, form_data):
        option_type = form_data.get(self.field_name("type"), "ALL")
        if option_type == "ALL":
            return options
        return [o for o in options if o["putCall"] == option_type]


@register
class MoneyStatusFilter(Criterion):
    id = "money_status"
    name = "Money Status"
    description = "Restrict to in-the-money or out-of-the-money options."

    def form_fields(self):
        return [
            FormField(
                name=self.field_name("status"),
                label="Status",
                field_type="select",
                default="ITM",
                choices=[
                    ("ALL", "All"),
                    ("ITM", "In the money"),
                    ("OTM", "Out of the money"),
                ],
            )
        ]

    def apply(self, options, underlying_price, form_data):
        status = form_data.get(self.field_name("status"), "ALL")
        if status == "ITM":
            return [o for o in options if o.get("inTheMoney")]
        if status == "OTM":
            return [o for o in options if not o.get("inTheMoney")]
        return options


@register
class TimeValuePctFilter(Criterion):
    id = "time_value_pct"
    name = "Time Value %"
    description = "Keep options whose time value is at most N% of the underlying price."

    def form_fields(self):
        return [
            FormField(
                name=self.field_name("max_pct"),
                label="Max time value (% of price)",
                field_type="number",
                default=1.0,
                min=0,
                max=100,
                step=0.1,
            )
        ]

    def apply(self, options, underlying_price, form_data):
        if underlying_price <= 0:
            return options
        try:
            max_pct = float(form_data.get(self.field_name("max_pct"), 1.0))
        except (ValueError, TypeError):
            return options
        threshold = (max_pct / 100) * underlying_price
        return [o for o in options if o.get("timeValue", float("inf")) <= threshold]


@register
class DaysToExpirationFilter(Criterion):
    id = "dte"
    name = "Days to Expiration"
    description = "Filter by a minimum and/or maximum number of days until expiration."

    def form_fields(self):
        return [
            FormField(
                name=self.field_name("min"),
                label="Min DTE",
                field_type="number",
                default=0,
                min=0,
                step=1,
            ),
            FormField(
                name=self.field_name("max"),
                label="Max DTE",
                field_type="number",
                default=90,
                min=0,
                step=1,
            ),
        ]

    def apply(self, options, underlying_price, form_data):
        results = options
        raw_min = form_data.get(self.field_name("min"), "")
        raw_max = form_data.get(self.field_name("max"), "")
        if raw_min != "":
            try:
                min_dte = int(raw_min)
                results = [o for o in results if o.get("daysToExpiration", 0) >= min_dte]
            except (ValueError, TypeError):
                pass
        if raw_max != "":
            try:
                max_dte = int(raw_max)
                results = [o for o in results if o.get("daysToExpiration", 0) <= max_dte]
            except (ValueError, TypeError):
                pass
        return results


@register
class DeltaFilter(Criterion):
    id = "delta"
    name = "Delta Range"
    description = "Filter by absolute delta value (0 = far OTM, 1 = deep ITM)."

    def form_fields(self):
        return [
            FormField(
                name=self.field_name("min"),
                label="Min |delta|",
                field_type="number",
                default=0.0,
                min=0,
                max=1,
                step=0.01,
            ),
            FormField(
                name=self.field_name("max"),
                label="Max |delta|",
                field_type="number",
                default=1.0,
                min=0,
                max=1,
                step=0.01,
            ),
        ]

    def apply(self, options, underlying_price, form_data):
        try:
            min_d = float(form_data.get(self.field_name("min"), 0.0))
        except (ValueError, TypeError):
            min_d = 0.0
        try:
            max_d = float(form_data.get(self.field_name("max"), 1.0))
        except (ValueError, TypeError):
            max_d = 1.0
        return [o for o in options if min_d <= abs(o.get("delta", 0)) <= max_d]


@register
class OpenInterestFilter(Criterion):
    id = "open_interest"
    name = "Open Interest"
    description = "Require a minimum number of open contracts."

    def form_fields(self):
        return [
            FormField(
                name=self.field_name("min"),
                label="Minimum open interest",
                field_type="number",
                default=100,
                min=0,
                step=1,
            )
        ]

    def apply(self, options, underlying_price, form_data):
        try:
            min_oi = int(form_data.get(self.field_name("min"), 0))
        except (ValueError, TypeError):
            min_oi = 0
        return [o for o in options if o.get("openInterest", 0) >= min_oi]


@register
class StrikeRangeFilter(Criterion):
    id = "strike_range"
    name = "Strike Range"
    description = "Keep strikes within a percentage band around the current price."

    def form_fields(self):
        return [
            FormField(
                name=self.field_name("min_pct"),
                label="Min strike (% of price)",
                field_type="number",
                default=80,
                min=0,
                step=1,
            ),
            FormField(
                name=self.field_name("max_pct"),
                label="Max strike (% of price)",
                field_type="number",
                default=120,
                min=0,
                step=1,
            ),
        ]

    def apply(self, options, underlying_price, form_data):
        if underlying_price <= 0:
            return options
        try:
            min_pct = float(form_data.get(self.field_name("min_pct"), 0))
            max_pct = float(form_data.get(self.field_name("max_pct"), 999))
        except (ValueError, TypeError):
            return options
        lo = (min_pct / 100) * underlying_price
        hi = (max_pct / 100) * underlying_price
        return [o for o in options if lo <= o.get("strikePrice", 0) <= hi]
