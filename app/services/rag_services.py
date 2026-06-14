# app/services/rag_service.py

from sqlalchemy.orm import Session

from app.services.dashboard_service import (
    load_dashboard_transactions,
    get_dashboard_metrics,
    get_financial_health,
    get_monthly_snapshot,
    get_spending_alert
)

from app.services.analytics_service import (
    AnalyticsService
)


class RAGService:

    @staticmethod
    def build_financial_context(
        db: Session,
        user_id: int
    ) -> str:

        df = load_dashboard_transactions(
            db=db,
            user_id=user_id
        )

        if df.empty:

            return """
                User belum memiliki data transaksi.

                Jelaskan kepada user bahwa analisis
                belum dapat dilakukan karena data
                transaksi masih kosong.
                """.strip()

        # =====================================
        # DASHBOARD METRICS
        # =====================================

        metrics = get_dashboard_metrics(
            df
        )

        # =====================================
        # FINANCIAL HEALTH
        # =====================================

        health = get_financial_health(
            df
        )

        # =====================================
        # MONTHLY SNAPSHOT
        # =====================================

        snapshot = get_monthly_snapshot(
            df
        )

        # =====================================
        # SPENDING ALERT
        # =====================================

        alerts = get_spending_alert(
            df
        )

        # =====================================
        # CATEGORY ANALYSIS
        # =====================================

        category_analysis = (
            AnalyticsService
            .analyze_by_category(df)
        )

        # =====================================
        # TOP TRANSACTIONS
        # =====================================

        top_transactions = (
            AnalyticsService
            .get_top_transactions(
                transactions_df=df,
                n=5
            )
        )

        # =====================================
        # PREDICTION
        # =====================================

        prediction = (
            AnalyticsService
            .get_prediction(
                db=db,
                user_id=user_id
            )
        )

        # =====================================
        # BUILD CONTEXT
        # =====================================

        context = f"""
            FINANCIAL SUMMARY

            Total Income:
            {metrics.get("total_income", 0)}

            Total Expense:
            {metrics.get("total_expense", 0)}

            Total Topup:
            {metrics.get("total_topup", 0)}

            Current Balance:
            {metrics.get("balance", 0)}

            Saving Rate:
            {metrics.get("saving_rate", 0)}%

            Average Daily Expense:
            {metrics.get("avg_daily", 0)}

            Average Transaction:
            {metrics.get("avg_transaction", 0)}

            Total Transaction:
            {metrics.get("total_transaction", 0)}

            --------------------------------------------------

            FINANCIAL HEALTH

            Status:
            {health.get("status", "-")}

            Message:
            {health.get("message", "-")}

            --------------------------------------------------

            MONTHLY SNAPSHOT

            Top Income:
            {snapshot.get("top_income")}

            Top Expense:
            {snapshot.get("top_expense")}

            Top Topup:
            {snapshot.get("top_topup")}

            --------------------------------------------------

            SPENDING ALERTS

            {alerts}

            --------------------------------------------------

            CATEGORY ANALYSIS

            {
                category_analysis.to_dict("records")
                if not category_analysis.empty
                else []
            }

            --------------------------------------------------

            TOP TRANSACTIONS

            {
                top_transactions.to_dict("records")
                if not top_transactions.empty
                else []
            }

            --------------------------------------------------

            PREDICTION

            {prediction}
            """

        return context.strip()