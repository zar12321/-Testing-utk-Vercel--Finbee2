# app/services/rag_service.py

from sqlalchemy.orm import Session

from app.services.dashboard_service import (
    load_dashboard_transactions,
    get_dashboard_metrics,
    get_financial_health,
    get_monthly_snapshot,
    get_spending_alert
)

from app.database.db import (
    get_user_by_id
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
        # PROFILE USER
        # =====================================    
        profile = get_user_by_id(
            db=db, 
            user_id=user_id
        )

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
        # SUMMARY METRICS
        # =====================================

        summary_metrics = (
            AnalyticsService
            .get_summary_metrics(df)
        )

        # =====================================
        # PAYMENT METHOD ANALYSIS
        # =====================================

        payment_analysis = (
            AnalyticsService
            .analyze_by_payment_method(df)
        )

        # =====================================
        # MONTHLY TREND
        # =====================================

        monthly_trend = (
            AnalyticsService
            .get_monthly_trend(df)
        )

        # =====================================
        # CHART DATA
        # =====================================

        chart_data = (
            AnalyticsService
            .get_chart_data(
                db=db,
                user_id=user_id
            )
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
        # Recent Transactions
        # =====================================
        recent_transactions = (
            df.head(10)
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
            Profile User:

            Nama: 
            {profile.nama if profile else "-"}

            Username: 
            {profile.login_identifier if profile else "-"}

            Umur:
            {profile.umur if profile else "-"}

            Pekerjaan:
            {profile.pekerjaan if profile else "-"}
            --------------------------------------------------

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
            --------------------------------------------------
            Total Transaction:
            {metrics.get("total_transaction", 0)}

            

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

            SUMMARY METRICS

            {summary_metrics}

            --------------------------------------------------

            PAYMENT METHOD ANALYSIS

            {
                payment_analysis.to_dict("records")
                if not payment_analysis.empty
                else []
            }

            --------------------------------------------------

            MONTHLY TREND

            {
                monthly_trend.tail(30)
                .to_dict("records")
                if not monthly_trend.empty
                else []
            }

            TOP TRANSACTIONS

            {
                top_transactions.to_dict("records")
                if not top_transactions.empty
                else []
            }

            --------------------------------------------------

            CASHFLOW TREND

            {chart_data.get("cashflow_trend", [])}

            --------------------------------------------------

            BREAKDOWN PREVIEW

            {chart_data.get("breakdown_preview", [])}

            --------------------------------------------------

            PAYMENT METHOD CHART

            {chart_data.get("payment_method_chart", [])}

            --------------------------------------------------

            RECENT TRANSACTION

            {
                recent_transactions.to_dict("records")
                if not recent_transactions.empty
                else []
            }

            PREDICTION

            Status:
            {prediction.get("success", False)}

            Message:
            {prediction.get("message", "-")}

            Forecast Data:
            {
                prediction.get("data")
                if prediction.get("success")
                else "-"
            }
            """
        


        return context.strip()