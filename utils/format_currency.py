from core.constants import (
    CURRENCY_SYMBOL
)


def format_currency(
    amount: float | int | None
) -> str:

    if amount is None:
        amount = 0

    try:
        amount = float(amount)

    except (
        TypeError,
        ValueError
    ):
        amount = 0

    return (
        f"{CURRENCY_SYMBOL} "
        f"{amount:,.0f}"
    )


def format_currency_short(
    amount: float | int | None
) -> str:

    if amount is None:
        amount = 0

    try:
        amount = float(amount)

    except (
        TypeError,
        ValueError
    ):
        amount = 0

    if amount >= 1_000_000_000:
        return (
            f"{amount / 1_000_000_000:.1f}B"
        )

    if amount >= 1_000_000:
        return (
            f"{amount / 1_000_000:.1f}M"
        )

    if amount >= 1_000:
        return (
            f"{amount / 1_000:.1f}K"
        )

    return f"{amount:.0f}"


def parse_currency(
    value
) -> float:

    if value is None:
        return 0.0

    value = str(value)

    value = (
        value
        .replace(CURRENCY_SYMBOL, "")
        .replace(",", "")
        .replace(".", "")
        .strip()
    )

    try:
        return float(value)

    except (
        TypeError,
        ValueError
    ):
        return 0.0


def calculate_percentage(
    value: float | int,
    total: float | int
) -> float:

    if total == 0:
        return 0.0

    return round(
        (value / total) * 100,
        2
    )


def calculate_balance(
    total_income: float | int,
    total_expense: float | int
) -> float:

    return (
        float(total_income)
        - float(total_expense)
    )


def determine_budget_status(
    total_expense: float | int,
    target_budget: float | int
) -> str:

    if target_budget <= 0:
        return "Tidak Ada Target"

    ratio = (
        float(total_expense)
        / float(target_budget)
    )

    if ratio <= 0.80:
        return "Aman"

    if ratio <= 1.00:
        return "Waspada"

    if ratio <= 1.10:
        return "Melebihi Sedikit"

    return "Melebihi Target"