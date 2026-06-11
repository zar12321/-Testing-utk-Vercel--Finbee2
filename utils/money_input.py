import re


def clean_money_input(
    value
) -> int:

    if value is None:
        return 0

    value = str(value)

    value = re.sub(
        r"[^0-9]",
        "",
        value
    )

    if not value:
        return 0

    return int(value)


def format_money_input(
    value
) -> str:

    amount = clean_money_input(
        value
    )

    return f"{amount:,}"


def money_to_float(
    value
) -> float:

    return float(
        clean_money_input(value)
    )


def money_to_int(
    value
) -> int:

    return clean_money_input(
        value
    )


def is_valid_amount(
    value
) -> bool:

    try:
        amount = float(value)

    except (
        TypeError,
        ValueError
    ):
        return False

    return amount > 0


def sanitize_amount(
    value
) -> float:

    if value is None:
        return 0.0

    try:
        amount = float(value)

    except (
        TypeError,
        ValueError
    ):
        return 0.0

    return abs(amount)