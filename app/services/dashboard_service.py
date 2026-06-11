# app/services/dashboard_service.py

from sqlalchemy.orm import Session

import pandas as pd

from app.database.db import (
    get_transactions_by_user_id
)

from utils.format_currency import (
    calculate_balance
)


# =====================================================
# LOAD USER TRANSACTIONS
# =====================================================

def load_dashboard_transactions(
    db: Session,
    user_id: int
) -> pd.DataFrame:

    return get_transactions_by_user_id(
        db=db,
        user_id=user_id
    )


# =====================================================
# TOTAL INCOME
# =====================================================

def get_total_income(
    db: Session,
    user_id: int
) -> float:

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id
    )

    if df.empty:
        return 0.0

    return float(
        df.loc[
            df["transaction_type"] == "income",
            "amount"
        ].sum()
    )


# =====================================================
# TOTAL EXPENSE
# =====================================================

def get_total_expense(
    db: Session,
    user_id: int
) -> float:

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id
    )

    if df.empty:
        return 0.0

    return float(
        df.loc[
            df["transaction_type"] == "expense",
            "amount"
        ].sum()
    )


# =====================================================
# TOTAL TOPUP
# =====================================================

def get_total_topup(
    db: Session,
    user_id: int
) -> float:

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id
    )

    if df.empty:
        return 0.0

    return float(
        df.loc[
            df["transaction_type"] == "topup",
            "amount"
        ].sum()
    )


# =====================================================
# CURRENT BALANCE
# =====================================================

def get_current_balance(
    db: Session,
    user_id: int
) -> float:

    total_income = get_total_income(
        db=db,
        user_id=user_id
    )

    total_expense = get_total_expense(
        db=db,
        user_id=user_id
    )

    return calculate_balance(
        total_income,
        total_expense
    )


# =====================================================
# RECENT TRANSACTIONS
# =====================================================

def get_recent_transactions(
    db: Session,
    user_id: int,
    limit: int = 5
):

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id
    )

    if df.empty:
        return []

    df = df.sort_values(
        by="tanggal_transaksi",
        ascending=False
    )

    return (
        df.head(limit)
        .to_dict("records")
    )


# =====================================================
# TOP EXPENSE CATEGORIES
# =====================================================

def get_top_expense_categories(
    db: Session,
    user_id: int,
    limit: int = 5
):

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id
    )

    if df.empty:
        return []

    expense_df = df[
        df["transaction_type"]
        == "expense"
    ]

    if expense_df.empty:
        return []

    result = (
        expense_df
        .groupby("category_name")["amount"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(limit)
        .reset_index()
    )

    return result.to_dict(
        "records"
    )


# =====================================================
# MONTHLY SUMMARY
# =====================================================

def get_monthly_summary(
    db: Session,
    user_id: int
):

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id
    )

    if df.empty:
        return []

    df = df.copy()

    df["tanggal_transaksi"] = pd.to_datetime(
        df["tanggal_transaksi"]
    )

    df["month"] = (
        df["tanggal_transaksi"]
        .dt.strftime("%Y-%m")
    )

    summary = (
        df.groupby(
            [
                "month",
                "transaction_type"
            ]
        )["amount"]
        .sum()
        .reset_index()
    )

    return summary.to_dict(
        "records"
    )


# =====================================================
# DASHBOARD METRICS
# =====================================================

def get_dashboard_metrics(
    db: Session,
    user_id: int
):

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id
    )

    return {
        "total_income":
            get_total_income(
                db=db,
                user_id=user_id
            ),

        "total_expense":
            get_total_expense(
                db=db,
                user_id=user_id
            ),

        "total_topup":
            get_total_topup(
                db=db,
                user_id=user_id
            ),

        "balance":
            get_current_balance(
                db=db,
                user_id=user_id
            ),

        "transaction_count":
            len(df)
    }