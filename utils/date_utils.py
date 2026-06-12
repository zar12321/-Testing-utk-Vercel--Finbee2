from datetime import date
from datetime import datetime
from typing import Optional

import pandas as pd

from core.constants import (
    DEFAULT_DATE_FORMAT,
    DEFAULT_DATETIME_FORMAT,
    DEFAULT_MONTH_FORMAT
)


def to_datetime(
    value
) -> Optional[pd.Timestamp]:

    if value is None:
        return None

    try:
        return pd.to_datetime(
            value,
            errors="coerce"
        )

    except Exception:
        return None


def to_date(
    value
) -> Optional[date]:

    dt = to_datetime(value)

    if dt is None or pd.isna(dt):
        return None

    return dt.date()


def format_date(
    value
) -> str:

    dt = to_datetime(value)

    if dt is None or pd.isna(dt):
        return "-"

    return dt.strftime(
        DEFAULT_DATE_FORMAT
    )


def format_datetime(
    value
) -> str:

    dt = to_datetime(value)

    if dt is None or pd.isna(dt):
        return "-"

    return dt.strftime(
        DEFAULT_DATETIME_FORMAT
    )


def format_month(
    value
) -> str:

    dt = to_datetime(value)

    if dt is None or pd.isna(dt):
        return "-"

    return dt.strftime(
        DEFAULT_MONTH_FORMAT
    )


def get_current_date() -> date:
    return date.today()


def get_current_datetime() -> datetime:
    return datetime.now()


def get_current_month() -> int:
    return datetime.now().month


def get_current_year() -> int:
    return datetime.now().year


def get_month_name(
    month_number: int
) -> str:

    months = {
        1: "Januari",
        2: "Februari",
        3: "Maret",
        4: "April",
        5: "Mei",
        6: "Juni",
        7: "Juli",
        8: "Agustus",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Desember"
    }

    return months.get(
        month_number,
        "-"
    )


def get_month_year_label(
    month: int,
    year: int
) -> str:

    return (
        f"{get_month_name(month)} {year}"
    )


def get_month_start(
    month: int | None = None,
    year: int | None = None
) -> pd.Timestamp:

    if month is None:
        month = get_current_month()

    if year is None:
        year = get_current_year()

    return pd.Timestamp(
        year=year,
        month=month,
        day=1
    )


def get_month_end(
    month: int | None = None,
    year: int | None = None
) -> pd.Timestamp:

    start = get_month_start(
        month,
        year
    )

    return (
        start
        + pd.offsets.MonthEnd(1)
    )


def extract_month(
    value
) -> Optional[int]:

    dt = to_datetime(value)

    if dt is None or pd.isna(dt):
        return None

    return int(dt.month)


def extract_year(
    value
) -> Optional[int]:

    dt = to_datetime(value)

    if dt is None or pd.isna(dt):
        return None

    return int(dt.year)


def create_month_filter_options(
    transactions_df: pd.DataFrame
) -> list[str]:

    if transactions_df.empty:
        return []

    df = transactions_df.copy()

    df["tanggal_transaksi"] = (
        pd.to_datetime(
            df["tanggal_transaksi"],
            errors="coerce"
        )
    )

    df = df.dropna(
        subset=["tanggal_transaksi"]
    )

    options = (
        df["tanggal_transaksi"]
        .dt.to_period("M")
        .astype(str)
        .unique()
        .tolist()
    )

    options.sort(
        reverse=True
    )

    return options


def filter_by_month_year(
    transactions_df: pd.DataFrame,
    month: int,
    year: int
) -> pd.DataFrame:

    if transactions_df.empty:
        return transactions_df

    df = transactions_df.copy()

    df["tanggal_transaksi"] = (
        pd.to_datetime(
            df["tanggal_transaksi"],
            errors="coerce"
        )
    )

    df = df.dropna(
        subset=["tanggal_transaksi"]
    )

    return df[
        (
            df["tanggal_transaksi"]
            .dt.month
            == month
        )
        &
        (
            df["tanggal_transaksi"]
            .dt.year
            == year
        )
    ]