import re
from typing import Any, Optional

import pandas as pd

from core.constants import (
    CATEGORY_ALLOWANCE,
    CATEGORY_BILLS,
    CATEGORY_EDUCATION,
    CATEGORY_ENTERTAINMENT,
    CATEGORY_FOOD,
    CATEGORY_HEALTH,
    CATEGORY_SALARY,
    CATEGORY_SHOPPING,
    CATEGORY_TOPUP,
    CATEGORY_TRANSPORT,
    DEFAULT_CATEGORY,
    DEFAULT_PAYMENT_METHOD,
    SUPPORTED_DATE_FORMATS,
    TRANSACTION_TYPE_EXPENSE,
    TRANSACTION_TYPE_INCOME,
    TRANSACTION_TYPE_TOPUP,
)


def find_column_by_keywords(
    columns,
    keywords
) -> str | None:
    normalized_columns = {
        col: str(col).lower().strip()
        for col in columns
    }

    for original_col, normalized_col in normalized_columns.items():
        for keyword in keywords:
            if keyword in normalized_col:
                return original_col

    return None


def clean_amount(
    value: Any
) -> Optional[float]:
    if pd.isna(value):
        return None

    text = str(value).strip()

    text = text.replace("Rp", "")
    text = text.replace("rp", "")
    text = text.replace("IDR", "")
    text = text.replace("idr", "")
    text = text.replace(" ", "")

    is_negative = "-" in text

    text = re.sub(r"[^0-9,\.]", "", text)

    if "," in text and "." in text:
        text = text.replace(".", "")
        text = text.replace(",", ".")

    elif "," in text:
        text = text.replace(",", "")

    elif "." in text:
        parts = text.split(".")

        if len(parts[-1]) == 3:
            text = text.replace(".", "")

    if text == "":
        return None

    try:
        amount = float(text)

    except ValueError:
        return None

    if is_negative:
        amount = abs(amount)

    return amount


def parse_flexible_date(
    value: Any
):
    if pd.isna(value):
        return pd.Timestamp.today().normalize()

    for fmt in SUPPORTED_DATE_FORMATS:
        try:
            return pd.to_datetime(
                value,
                format=fmt
            )

        except Exception:
            continue

    parsed_date = pd.to_datetime(
        value,
        errors="coerce"
    )

    if pd.isna(parsed_date):
        return pd.Timestamp.today().normalize()

    return parsed_date


def normalize_transaction_type(
    value: Any
) -> str:

    if pd.isna(value):
        return TRANSACTION_TYPE_EXPENSE

    text = str(value).strip().lower()

    type_mapping = {
        "expense": TRANSACTION_TYPE_EXPENSE,
        "pengeluaran": TRANSACTION_TYPE_EXPENSE,
        "keluar": TRANSACTION_TYPE_EXPENSE,
        "debit": TRANSACTION_TYPE_EXPENSE,
        "debet": TRANSACTION_TYPE_EXPENSE,
        "out": TRANSACTION_TYPE_EXPENSE,
        "outcome": TRANSACTION_TYPE_EXPENSE,

        "income": TRANSACTION_TYPE_INCOME,
        "pemasukan": TRANSACTION_TYPE_INCOME,
        "masuk": TRANSACTION_TYPE_INCOME,
        "credit": TRANSACTION_TYPE_INCOME,
        "kredit": TRANSACTION_TYPE_INCOME,
        "in": TRANSACTION_TYPE_INCOME,
        "revenue": TRANSACTION_TYPE_INCOME,

        "topup": TRANSACTION_TYPE_TOPUP,
        "top up": TRANSACTION_TYPE_TOPUP,
        "isi saldo": TRANSACTION_TYPE_TOPUP,
        "e-wallet": TRANSACTION_TYPE_TOPUP,
    }

    return type_mapping.get(
        text,
        TRANSACTION_TYPE_EXPENSE
    )


def standardize_category(
    raw_category,
    description="",
    transaction_type=TRANSACTION_TYPE_EXPENSE
) -> str:

    raw_category = (
        ""
        if pd.isna(raw_category)
        else str(raw_category)
    )

    description = (
        ""
        if pd.isna(description)
        else str(description)
    )

    text = (
        f"{raw_category} {description}"
    ).lower()

    if transaction_type == TRANSACTION_TYPE_TOPUP:
        return CATEGORY_TOPUP

    if transaction_type == TRANSACTION_TYPE_INCOME:

        if any(
            word in text
            for word in [
                "gaji",
                "salary",
                "income",
                "pemasukan",
                "upah",
                "freelance",
                "honor",
                "bonus",
                "komisi",
                "transfer gaji"
            ]
        ):
            return CATEGORY_SALARY

        if any(
            word in text
            for word in [
                "allowance",
                "uang saku",
                "kiriman",
                "transfer orang tua",
                "uang bulanan"
            ]
        ):
            return CATEGORY_ALLOWANCE

        return CATEGORY_SALARY

    if any(
        word in text
        for word in [
            "food",
            "makan",
            "makanan",
            "minum",
            "minuman",
            "jajan",
            "groceries",
            "grocery",
            "belanja dapur",
            "sayur",
            "buah",
            "nasi",
            "ayam",
            "kopi",
            "cafe",
            "restoran",
            "restaurant",
            "warung",
            "kantin",
            "bakso",
            "mie",
            "gofood",
            "grabfood"
        ]
    ):
        return CATEGORY_FOOD

    if any(
        word in text
        for word in [
            "transport",
            "transportasi",
            "ojek",
            "grab",
            "gojek",
            "bus",
            "kereta",
            "bensin",
            "parkir",
            "tol",
            "angkot",
            "taxi",
            "taksi",
            "mrt",
            "lrt"
        ]
    ):
        return CATEGORY_TRANSPORT

    if any(
        word in text
        for word in [
            "bill",
            "bills",
            "tagihan",
            "listrik",
            "air",
            "internet",
            "wifi",
            "pulsa",
            "sewa",
            "kos",
            "kontrakan",
            "pln",
            "pdam"
        ]
    ):
        return CATEGORY_BILLS

    if any(
        word in text
        for word in [
            "shopping",
            "belanja",
            "baju",
            "sepatu",
            "tas",
            "aksesoris",
            "skincare",
            "barang",
            "marketplace",
            "tokopedia",
            "shopee",
            "lazada",
            "mall"
        ]
    ):
        return CATEGORY_SHOPPING

    if any(
        word in text
        for word in [
            "education",
            "pendidikan",
            "kuliah",
            "buku",
            "kursus",
            "kelas",
            "seminar",
            "pelatihan",
            "modul",
            "kampus",
            "sertifikat"
        ]
    ):
        return CATEGORY_EDUCATION

    if any(
        word in text
        for word in [
            "health",
            "kesehatan",
            "obat",
            "vitamin",
            "dokter",
            "rumah sakit",
            "klinik",
            "apotek",
            "masker",
            "suplemen"
        ]
    ):
        return CATEGORY_HEALTH

    if any(
        word in text
        for word in [
            "entertainment",
            "hiburan",
            "nonton",
            "bioskop",
            "game",
            "spotify",
            "netflix",
            "konser",
            "film",
            "popcorn"
        ]
    ):
        return CATEGORY_ENTERTAINMENT

    return DEFAULT_CATEGORY


def auto_clean_financial_file(
    df: pd.DataFrame
) -> pd.DataFrame:

    cleaned_df = pd.DataFrame()

    date_col = None

    priority_date_columns = [
        "tanggal transaksi",
        "transaction date",
        "date transaksi"
    ]

    for col in df.columns:

        col_lower = str(col).lower().strip()

        if col_lower in priority_date_columns:
            date_col = col
            break

    if date_col is None:

        date_col = find_column_by_keywords(
            df.columns,
            [
                "date",
                "tgl",
                "tanggal"
            ]
        )

    amount_col = find_column_by_keywords(
        df.columns,
        [
            "nominal",
            "amount",
            "jumlah",
            "total",
            "harga",
            "value",
            "nilai",
            "pengeluaran",
            "pemasukan"
        ]
    )

    tujuan_col = find_column_by_keywords(
        df.columns,
        [
            "tujuan transaksi",
            "tujuan"
        ]
    )

    desc_col = find_column_by_keywords(
        df.columns,
        [
            "keterangan",
            "deskripsi",
            "description",
            "catatan",
            "remark",
            "details"
        ]
    )

    payment_col = find_column_by_keywords(
        df.columns,
        [
            "bayar lewat",
            "metode pembayaran",
            "payment method",
            "payment",
            "metode",
            "wallet",
            "bank"
        ]
    )

    type_col = find_column_by_keywords(
        df.columns,
        [
            "transaction type",
            "jenis transaksi",
            "arus kas",
            "cashflow",
            "cash flow",
            "debit kredit",
            "debit/kredit",
            "type",
            "tipe",
            "jenis"
        ]
    )

    category_col = find_column_by_keywords(
        df.columns,
        [
            "kategori",
            "category"
        ]
    )

    if amount_col is None:
        raise ValueError(
            "Kolom nominal tidak ditemukan."
        )

    if date_col:

        cleaned_df["tanggal_transaksi"] = (
            df[date_col]
            .apply(parse_flexible_date)
        )

    else:

        cleaned_df["tanggal_transaksi"] = (
            pd.Timestamp.today().normalize()
        )

    if desc_col:

        cleaned_df["keterangan"] = (
            df[desc_col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        cleaned_df.loc[
            cleaned_df["keterangan"] == "", 
            "keterangan"
        ] = "-"

    else:
        cleaned_df["keterangan"] = ""

    if tujuan_col:

        cleaned_df["tujuan_transaksi"] = (
            df[tujuan_col]
            .fillna("")
            .astype(str)
            .str.strip()
        )


    else:

        cleaned_df["tujuan_transaksi"] = (
            cleaned_df["keterangan"]
        )

    cleaned_df["tujuan_transaksi"] = (
        df[tujuan_col]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    cleaned_df.loc[
        cleaned_df["tujuan_transaksi"] == "",
        "tujuan_transaksi"
    ] = "-"

    if payment_col:

        cleaned_df["payment_method"] = (
            df[payment_col]
            .fillna("-")
            .astype(str)
            .str.strip()
        )

        cleaned_df.loc[
            cleaned_df["payment_method"] == "",
            "payment_method"
        ] = "-"

    else:

        cleaned_df["payment_method"] = (
            DEFAULT_PAYMENT_METHOD
        )

    cleaned_df["amount"] = (
        df[amount_col]
        .apply(clean_amount)
    )

    if type_col:

        cleaned_df["transaction_type"] = (
            df[type_col]
            .apply(normalize_transaction_type)
        )

    elif category_col:

        cleaned_df["transaction_type"] = (
            df[category_col]
            .apply(normalize_transaction_type)
        )

    else:

        cleaned_df["transaction_type"] = (
            TRANSACTION_TYPE_EXPENSE
        )

    if category_col:

        cleaned_df["raw_category"] = (
            df[category_col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        cleaned_df.loc[
            cleaned_df["raw_category"] == "",
            "raw_category"
        ] = "-"

    else:

        cleaned_df["raw_category"] = ""

    cleaned_df["category_name"] = (
        cleaned_df.apply(
            lambda row: standardize_category(
                raw_category=row["raw_category"],
                description=(
                    str(row["tujuan_transaksi"])
                    + " "
                    + str(row["keterangan"])
                ),
                transaction_type=row["transaction_type"]
            ),
            axis=1
        )
    )

    cleaned_df = cleaned_df.dropna(
        subset=["amount"]
    )

    cleaned_df = cleaned_df[
        cleaned_df["amount"] > 0
    ]

    cleaned_df = cleaned_df[
        [
            "tanggal_transaksi",
            "raw_category",
            "category_name",
            "transaction_type",
            "tujuan_transaksi",
            "keterangan",
            "payment_method",
            "amount"
        ]
    ]

    return cleaned_df