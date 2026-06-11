import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression

from core.constants import (
    TRANSACTION_TYPE_EXPENSE
)


def prepare_monthly_expense(
    transactions_df: pd.DataFrame
) -> pd.DataFrame:

    if transactions_df.empty:
        return pd.DataFrame()

    required_columns = [
        "tanggal_transaksi",
        "transaction_type",
        "amount"
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in transactions_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Kolom wajib tidak ditemukan: {missing_columns}"
        )

    df = transactions_df.copy()

    df["tanggal_transaksi"] = pd.to_datetime(
        df["tanggal_transaksi"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["tanggal_transaksi"]
    )

    expense_df = df[
        df["transaction_type"]
        == TRANSACTION_TYPE_EXPENSE
    ]

    if expense_df.empty:
        return pd.DataFrame()

    monthly_expense = (
        expense_df
        .set_index("tanggal_transaksi")
        .resample("ME")["amount"]
        .sum()
        .reset_index()
    )

    monthly_expense = monthly_expense.rename(
        columns={
            "tanggal_transaksi": "bulan",
            "amount": "total_pengeluaran"
        }
    )

    monthly_expense["month_index"] = np.arange(
        len(monthly_expense)
    )

    return monthly_expense


def predict_next_month_expense(
    transactions_df: pd.DataFrame
) -> dict:

    monthly_expense = prepare_monthly_expense(
        transactions_df
    )

    if monthly_expense.empty:

        return {
            "prediction": 0.0,
            "method": "no_data",
            "monthly_data": monthly_expense,
            "message": (
                "Belum ada data pengeluaran "
                "untuk diprediksi."
            )
        }

    if len(monthly_expense) < 3:

        prediction = (
            monthly_expense[
                "total_pengeluaran"
            ]
            .mean()
        )

        return {
            "prediction": round(
                float(prediction),
                2
            ),
            "method": "monthly_average",
            "monthly_data": monthly_expense,
            "message": (
                "Data kurang dari 3 bulan. "
                "Prediksi menggunakan "
                "rata-rata pengeluaran bulanan."
            )
        }

    X = monthly_expense[
        ["month_index"]
    ]

    y = monthly_expense[
        "total_pengeluaran"
    ]

    model = LinearRegression()

    model.fit(
        X,
        y
    )

    next_month_index = pd.DataFrame(
        {
            "month_index": [
                len(monthly_expense)
            ]
        }
    )

    prediction = model.predict(
        next_month_index
    )[0]

    prediction = max(
        float(prediction),
        0.0
    )

    return {
        "prediction": round(
            prediction,
            2
        ),
        "method": "linear_regression",
        "monthly_data": monthly_expense,
        "message": (
            "Data minimal 3 bulan. "
            "Prediksi menggunakan "
            "Linear Regression."
        )
    }