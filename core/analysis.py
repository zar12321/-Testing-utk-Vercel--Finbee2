import pandas as pd


def get_summary_metrics(
    transactions_df: pd.DataFrame
) -> dict:
    """
    Menghasilkan ringkasan metrik keuangan.
    """

    if transactions_df.empty:
        return {
            "total_expense": 0,
            "total_income": 0,
            "balance": 0,
            "transaction_count": 0,
            "average_transaction": 0
        }

    expense_df = transactions_df[
        transactions_df["transaction_type"] == "expense"
    ]

    income_df = transactions_df[
        transactions_df["transaction_type"] == "income"
    ]

    total_expense = float(
        expense_df["amount"].sum()
    )

    total_income = float(
        income_df["amount"].sum()
    )

    balance = total_income - total_expense

    transaction_count = int(
        len(transactions_df)
    )

    average_transaction = float(
        transactions_df["amount"].mean()
    )

    return {
        "total_expense": total_expense,
        "total_income": total_income,
        "balance": balance,
        "transaction_count": transaction_count,
        "average_transaction": average_transaction
    }


def analyze_by_category(
    transactions_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Analisis total pengeluaran berdasarkan kategori.
    """

    if transactions_df.empty:
        return pd.DataFrame()

    expense_df = transactions_df[
        transactions_df["transaction_type"] == "expense"
    ]

    if expense_df.empty:
        return pd.DataFrame()

    return (
        expense_df
        .groupby("category_name")["amount"]
        .sum()
        .reset_index()
        .sort_values(
            "amount",
            ascending=False
        )
    )


def analyze_by_payment_method(
    transactions_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Analisis nominal transaksi berdasarkan metode pembayaran.
    """

    if transactions_df.empty:
        return pd.DataFrame()

    return (
        transactions_df
        .groupby("payment_method")["amount"]
        .sum()
        .reset_index()
        .sort_values(
            "amount",
            ascending=False
        )
    )


def get_monthly_trend(
    transactions_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Tren transaksi harian berdasarkan tipe transaksi.
    """

    if transactions_df.empty:
        return pd.DataFrame()

    df = transactions_df.copy()

    df["tanggal_transaksi"] = pd.to_datetime(
        df["tanggal_transaksi"]
    )

    return (
        df
        .groupby(
            [
                "tanggal_transaksi",
                "transaction_type"
            ]
        )["amount"]
        .sum()
        .reset_index()
        .sort_values(
            "tanggal_transaksi"
        )
    )


def get_top_transactions(
    transactions_df: pd.DataFrame,
    n: int = 5
) -> pd.DataFrame:
    """
    Mengambil transaksi dengan nominal terbesar.
    """

    if transactions_df.empty:
        return pd.DataFrame()

    return (
        transactions_df
        .sort_values(
            "amount",
            ascending=False
        )
        .head(n)
    )