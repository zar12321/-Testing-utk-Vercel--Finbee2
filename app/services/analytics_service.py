# app/services/analytics_service.py

from sqlalchemy.orm import Session

from app.database.db import (
    get_transactions_by_user_id
)

from core.prediction import (
    predict_next_month_expense
)

from app.repositories import (
    analytics_repository
)

import pandas as pd


class AnalyticsService:
    @staticmethod
    def get_chart_data(
        db,
        user_id,
        month=None,
        year=None,
        period=None,
        category=None,
        subcategory_id=None
    ):

        filters = {
            "month": month,
            "year": year,
            "period": period,
            "category": category,
            "subcategory_id": subcategory_id
        }

        return {
            "cashflow_trend":
                analytics_repository.get_cashflow_trend(
                    db=db,
                    user_id=user_id,
                    filters=filters
                ),

            "breakdown_chart":
                analytics_repository.get_breakdown_chart(
                    db=db,
                    user_id=user_id,
                    filters=filters
                ), 
            
            "breakdown_preview":
                analytics_repository.get_breakdown_preview(
                    db=db, 
                    user_id=user_id, 
                    filters=filters
                ), 

            "payment_method_chart":
                analytics_repository.get_payment_method_chart(
                    db=db, 
                    user_id=user_id, 
                    filters=filters
                )
        }

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