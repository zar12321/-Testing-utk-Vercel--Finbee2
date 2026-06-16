# ml/datasets/daily_expense_dataset.py

import pandas as pd 

from sqlalchemy.orm import Session

from app.database.db import (
    get_transactions_by_user_id
)

def build_daily_expense_dataset(
    db: Session, 
    user_id: int, 
    category_id: int | None = None
):
    """
    Membentuk dataset time series harian 
    utk kebutuhan forecasting pengeluaran
    
    Output:
    ----------------------
    date         amount
    2025-01-01   50000
    2025-01-02   0
    """
    # ================================
    # Load transaksi user
    # ================================
    df = get_transactions_by_user_id(
        db=db, 
        user_id=user_id
    )
    if df.empty:
        return pd.DataFrame(
            columns=[
                "date", 
                "amount"
            ]
        )
    
    # ================================
    # Hanya pengeluaran
    # ================================
    df = df[
        df["transaction_type"]
        == "expense"
    ].copy()

    # ================================
    # Filter subkategori
    # ================================
    if category_id is not None:
        df = df[
            df["category_id"]
            == category_id
        ].copy()

    # ================================
    # Jika tidak ada data
    # ================================
    if df.empty:
        return pd.DataFrame(
            columns=[
                "date", 
                "amount"
            ]
        )
    
    # ================================
    # Pastikan format datetime
    # ================================
    df["tanggal_transaksi"] = pd.to_datetime(
        df["tanggal_transaksi"]
    )

    # ================================
    # Group harian
    # ================================
    daily_df = (
        df.groupby(
            "tanggal_transaksi", 
            as_index=False
        )["amount"]
        .sum()
    )

    # ================================
    # Rename tanggal transaksi jadi date 
    # ================================
    daily_df = daily_df.rename(
        columns={
            "tanggal_transaksi": "date"
        }
    )

    # ================================
    # Buat range tanggal lengkap 
    # ================================
    full_dates = pd.date_range(
        start=daily_df["date"].min(), 
        end=daily_df["date"].max(), 
        freq="D"
    )
    full_dates_df = pd.DataFrame(
        {
            "date": full_dates
        }
    )

    # ================================
    # Merge
    # ================================
    daily_df = full_dates_df.merge(
        daily_df, 
        on="date", 
        how="left"
    )

    # ================================
    # Isi hari kosong dengan 0
    # ================================
    daily_df["amount"] = (
        daily_df["amount"]
        .fillna(0)
        .astype(float)
    )

    # ================================
    # Sort
    # ================================
    daily_df = daily_df.sort_values(
        by="date"
    ).reset_index(
        drop=True
    )
    return daily_df












