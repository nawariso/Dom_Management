from datetime import date
from decimal import Decimal
from typing import Dict, List, Optional

from backend.app.models import Tariff


def _clamp_date(value: date, start: date, end: date) -> date:
    return max(start, min(value, end))


def prorate_amount(
    amount: Decimal,
    active_from: date,
    active_to: date,
    period_start: date,
    period_end: date,
) -> Decimal:
    """
    Calculate a prorated amount for a sub-period within a billing window.

    The active window is clamped within the billing period to gracefully handle
    room moves that overlap adjacent cycles.
    """

    clamped_start = _clamp_date(active_from, period_start, period_end)
    clamped_end = _clamp_date(active_to, period_start, period_end)
    total_days = (period_end - period_start).days or 1
    active_days = (clamped_end - clamped_start).days
    if active_days < 0:
        return Decimal("0.00")
    proportion = Decimal(active_days) / Decimal(total_days)
    return (amount * proportion).quantize(Decimal("0.01"))


def calculate_tariff_charge(consumption: float, tariff: Tariff) -> Decimal:
    """
    Compute total charge with optional tiered pricing. Tiers are expected to be a
    list of dicts [{'up_to': int, 'rate': float}]. Consumption beyond the last
    tier is billed using the tariff.rate_per_unit.
    """

    total = Decimal(tariff.base_fee or 0)
    remaining = Decimal(consumption)
    tiers: Optional[List[Dict[str, float]]] = tariff.tiers or []

    for tier in tiers:
        limit = Decimal(str(tier.get("up_to", 0)))
        rate = Decimal(str(tier.get("rate", tariff.rate_per_unit)))
        if remaining <= 0:
            break
        tier_usage = min(remaining, limit)
        total += tier_usage * rate
        remaining -= tier_usage

    if remaining > 0:
        total += remaining * Decimal(tariff.rate_per_unit)

    return total.quantize(Decimal("0.01"))
