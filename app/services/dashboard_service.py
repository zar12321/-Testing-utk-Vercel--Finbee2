# app/services/dashboard_service.py

from sqlalchemy.orm import Session

import pandas as pd

from app.database.db import (
    get_transactions_by_user_id
)

from utils.format_currency import (
    calculate_balance
)

from fastapi import Query


# =====================================================
# LOAD USER TRANSACTIONS
# =====================================================
def load_dashboard_transactions(
    db: Session,
    user_id: int,
    month: int | None = None,
    year: int | None = None
) -> pd.DataFrame:

    df = get_transactions_by_user_id(
        db=db,
        user_id=user_id, 
    )

    if df.empty:
        return df

    df = df.copy()

    df["tanggal_transaksi"] = pd.to_datetime(
        df["tanggal_transaksi"]
    )

    if year is not None:
        df = df[
            df["tanggal_transaksi"].dt.year == year
        ]

    if month is not None:
        df = df[
            df["tanggal_transaksi"].dt.month == month
        ]

    return df


# =====================================================
# TOTAL INCOME
# =====================================================

def get_total_income(
    db: Session,
    user_id: int,
    month: int | None = None,
    year: int | None = None
) -> float:

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id, 
        month=month, 
        year=year
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
    user_id: int,
    month: int | None = None,
    year: int | None = None
) -> float:

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id, 
        month=month, 
        year=year
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
    user_id: int, 
    month: int | None = None,
    year: int | None = None
) -> float:

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id, 
        month=month, 
        year=year
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
    user_id: int, 
    month: int | None = None,
    year: int | None = None
) -> float:

    total_income = get_total_income(
        db=db,
        user_id=user_id, 
        month=month, 
        year=year
    )

    total_expense = get_total_expense(
        db=db,
        user_id=user_id, 
        month=month, 
        year=year
    )

    return calculate_balance(
        total_income,
        total_expense
    )

# =====================================================
# TOTAL TRANSACTION
# =====================================================

def get_total_transaction(
    db: Session,
    user_id: int, 
    month: int | None = None,
    year: int | None = None
) -> int:

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id, 
        month=month, 
        year=year
    )

    return len(df)

# =====================================================
# AVG TRANSACTION
# =====================================================

def get_avg_transaction(
    db: Session,
    user_id: int, 
    month: int | None = None,
    year: int | None = None
) -> float:

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id, 
        month=month, 
        year=year
    )

    if df.empty:
        return 0.0

    return float(
        df["amount"].mean()
    )

# =====================================================
# AVG DAILY
# =====================================================

def get_avg_daily(
    db: Session,
    user_id: int, 
    month: int | None = None,
    year: int | None = None
) -> float:

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id, 
        month=month, 
        year=year
    )

    if df.empty:
        return 0.0

    df = df.copy()

    df["tanggal_transaksi"] = pd.to_datetime(
        df["tanggal_transaksi"]
    )


    total_amount = df["amount"].sum()

    total_days = (
        df["tanggal_transaksi"].max()
        -
        df["tanggal_transaksi"].min()
    ).days + 1

    if total_days <= 0:
        total_days = 1

    return float(
        total_amount / total_days
    )

# =====================================================
# SAVING RATE
# =====================================================

def get_saving_rate(
    db: Session,
    user_id: int, 
    month: int | None = None,
    year: int | None = None
) -> float:

    income = get_total_income(
        db=db,
        user_id=user_id, 
        month=month, 
        year=year
    )

    expense = get_total_expense(
        db=db,
        user_id=user_id, 
        month=month, 
        year=year
    )

    if income == 0:
        return 0.0

    return float(
        (
            (income - expense)
            / income
        ) * 100
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
    user_id: int, 
    month: int | None=None, 
    year: int | None=None
):

    return {

        "total_income":
            get_total_income(
                db=db,
                user_id=user_id, 
                month=month, 
                year=year
            ),

        "total_expense":
            get_total_expense(
                db=db,
                user_id=user_id,
                month=month, 
                year=year
            ),

        "total_topup":
            get_total_topup(
                db=db,
                user_id=user_id, 
                month=month, 
                year=year
            ),

        "balance":
            get_current_balance(
                db=db,
                user_id=user_id, 
                month=month, 
                year=year
            ),

        "total_transaction":
            get_total_transaction(
                db=db,
                user_id=user_id, 
                month=month, 
                year=year
            ),

        "avg_transaction":
            get_avg_transaction(
                db=db,
                user_id=user_id, 
                month=month, 
                year=year
            ),

        "avg_daily":
            get_avg_daily(
                db=db,
                user_id=user_id, 
                month=month, 
                year=year
            ),

        "saving_rate":
            get_saving_rate(
                db=db,
                user_id=user_id, 
                month=month, 
                year=year
            )
    }

# =====================================================
# FINANCIAL HEALTH
# =====================================================

def get_financial_health(
    db: Session,
    user_id: int,
    month: int | None = None,
    year: int | None = None
):

    income = get_total_income(
        db=db,
        user_id=user_id,
        month=month,
        year=year
    )

    expense = get_total_expense(
        db=db,
        user_id=user_id,
        month=month,
        year=year
    )

    saving_rate = get_saving_rate(
        db=db,
        user_id=user_id,
        month=month,
        year=year
    )

    expense_ratio = 0

    if income > 0:
        expense_ratio = (
            expense / income
        ) * 100

    if saving_rate >= 20:

        status = "Sehat"
        icon = "🟢"

        message = (
            "Kondisi keuangan berada dalam kategori baik."
        )

    elif saving_rate >= 0:

        status = "Waspada"
        icon = "🟡"

        message = (
            "Pengeluaran mulai mendekati pemasukan."
        )

    else:

        status = "Bahaya"
        icon = "🔴"

        message = (
            "Pengeluaran melebihi pemasukan."
        )

    return {

        "icon": icon,

        "status": status,

        "saving_rate":
            round(
                saving_rate,
                2
            ),

        "expense_ratio":
            round(
                expense_ratio,
                2
            ),

        "message": message
    }

# =====================================================
# MONTHLY SNAPSHOT
# =====================================================

def get_monthly_snapshot(
    db: Session,
    user_id: int,
    month: int | None = None,
    year: int | None = None
):

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id,
        month=month,
        year=year
    )

    if df.empty:

        return {
            "top_income": None,
            "top_expense": None
        }

    # INCOME TERBESAR

    income_df = df[
        df["transaction_type"]
        == "income"
    ]

    top_income = None

    if not income_df.empty:

        grouped = (
            income_df
            .groupby("category_name")["amount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        top_income = {
            "category": grouped.index[0],
            "amount": float(grouped.iloc[0])
        }

    # EXPENSE TERBESAR

    expense_df = df[
        df["transaction_type"]
        == "expense"
    ]

    top_expense = None

    if not expense_df.empty:

        grouped = (
            expense_df
            .groupby("category_name")["amount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        top_expense = {
            "category": grouped.index[0],
            "amount": float(grouped.iloc[0])
        }

    return {

        "top_income": top_income,

        "top_expense": top_expense
    }   
# =============================
# SPENDING ALERTS
# =============================
def get_spending_alert(
    db: Session,
    user_id: int,
    month: int | None = None,
    year: int | None = None
):

    alerts = []

    df = load_dashboard_transactions(
        db=db,
        user_id=user_id,
        month=month,
        year=year
    )

    if df.empty:

        alerts.append({
            "status": "info",
            "icon": "📊",
            "title": "Belum Ada Data",
            "message": "Belum terdapat transaksi pada periode ini."
        })

        return alerts

    income = get_total_income(
        db=db,
        user_id=user_id,
        month=month,
        year=year
    )

    expense = get_total_expense(
        db=db,
        user_id=user_id,
        month=month,
        year=year
    )

    saving_rate = get_saving_rate(
        db=db,
        user_id=user_id,
        month=month,
        year=year
    )

    # ====================================
    # ALERT 1
    # Pengeluaran > Pemasukan
    # ====================================

    if income > 0 and expense > income:

        deficit = expense - income

        alerts.append({
            "status": "danger",
            "icon": "🚨",
            "title": "Pengeluaran Melebihi Pemasukan",
            "message":
                f"Defisit sebesar Rp {deficit:,.0f}"
        })

    # ====================================
    # ALERT 2
    # Saving Rate Rendah
    # ====================================

    if income > 0 and saving_rate < 10:

        alerts.append({
            "status": "warning",
            "icon": "📉",
            "title": "Saving Rate Rendah",
            "message":
                f"Saving rate hanya {saving_rate:.1f}%."
        })

    expense_df = df[
        df["transaction_type"] == "expense"
    ]

    if not expense_df.empty:

        # ====================================
        # ALERT 3
        # Kategori Terbesar
        # ====================================

        category_summary = (
            expense_df
            .groupby("category_name")["amount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        top_category = category_summary.index[0]

        top_amount = category_summary.iloc[0]

        percentage = (
            top_amount / expense
        ) * 100

        if percentage >= 40:

            alerts.append({
                "status": "warning",
                "icon": "🍔",
                "title": f"{top_category} Mendominasi Pengeluaran",
                "message":
                    f"Menyumbang {percentage:.1f}% dari total pengeluaran."
            })

        # ====================================
        # ALERT 4
        # Transaksi Kecil Berulang
        # ====================================

        small_transactions = expense_df[
            expense_df["amount"] <= 25000
        ]

        if len(small_transactions) >= 15:

            alerts.append({
                "status": "info",
                "icon": "☕",
                "title": "Pengeluaran Kecil Berulang",
                "message":
                    f"Terdapat {len(small_transactions)} transaksi di bawah Rp 25.000."
            })

        # ====================================
        # ALERT 5
        # Merchant / Deskripsi Terbanyak
        # ====================================

        if "description" in expense_df.columns:

            description_count = (
                expense_df["description"]
                .dropna()
                .value_counts()
            )

            if not description_count.empty:

                top_desc = description_count.index[0]

                top_desc_count = (
                    description_count.iloc[0]
                )

                if top_desc_count >= 5:

                    alerts.append({
                        "status": "info",
                        "icon": "🔁",
                        "title": "Transaksi Berulang Terdeteksi",
                        "message":
                            f"'{top_desc}' muncul sebanyak {top_desc_count} kali."
                    })

    # ====================================
    # ALERT 6
    # Top Up Tinggi
    # ====================================

    topup = get_total_topup(
        db=db,
        user_id=user_id,
        month=month,
        year=year
    )

    if income > 0:

        topup_ratio = (
            topup / income
        ) * 100

        if topup_ratio >= 50:

            alerts.append({
                "status": "warning",
                "icon": "📱",
                "title": "Top Up Relatif Tinggi",
                "message":
                    f"Top up mencapai {topup_ratio:.1f}% dari pemasukan."
            })

    # ====================================
    # Jika Tidak Ada Alert
    # ====================================

    if not alerts:

        alerts.append({
            "status": "success",
            "icon": "✅",
            "title": "Keuangan Relatif Sehat",
            "message":
                "Tidak ditemukan pola pengeluaran yang mengkhawatirkan."
        })

    return alerts