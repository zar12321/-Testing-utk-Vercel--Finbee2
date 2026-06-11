# app/services/analysis_service.py

from sqlalchemy.orm import Session

from app.database.db import (
    get_transactions_by_user_id
)

from core.prediction import (
    predict_next_month_expense
)

import pandas as pd


class AnalysisService:

    @staticmethod
    def get_summary_metrics(
        transactions_df: pd.DataFrame
    ) -> dict:

        if transactions_df.empty:
            return {
                "total_expense": 0,
                "total_income": 0,
                "balance": 0,
                "transaction_count": 0,
                "average_transaction": 0
            }

        expense_df = transactions_df[
            transactions_df["transaction_type"]
            == "expense"
        ]

        income_df = transactions_df[
            transactions_df["transaction_type"]
            == "income"
        ]

        total_expense = float(
            expense_df["amount"].sum()
        )

        total_income = float(
            income_df["amount"].sum()
        )

        balance = (
            total_income
            - total_expense
        )

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

    @staticmethod
    def analyze_by_category(
        transactions_df: pd.DataFrame
    ) -> pd.DataFrame:

        if transactions_df.empty:
            return pd.DataFrame()

        expense_df = transactions_df[
            transactions_df["transaction_type"]
            == "expense"
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

    @staticmethod
    def analyze_by_payment_method(
        transactions_df: pd.DataFrame
    ) -> pd.DataFrame:

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

    @staticmethod
    def get_monthly_trend(
        transactions_df: pd.DataFrame
    ) -> pd.DataFrame:

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

    @staticmethod
    def get_top_transactions(
        transactions_df: pd.DataFrame,
        n: int = 5
    ) -> pd.DataFrame:

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

    @staticmethod
    def get_prediction(
        db: Session,
        user_id: int
    ) -> dict:

        transactions_df = (
            get_transactions_by_user_id(
                db=db,
                user_id=user_id
            )
        )

        return predict_next_month_expense(
            transactions_df
        )