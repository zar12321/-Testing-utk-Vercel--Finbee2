from fastapi import (
    APIRouter,
    Request,
    Depends
)

from sqlalchemy.orm import Session

from fastapi.templating import (
    Jinja2Templates
)

from app.database.connection import (
    get_db
)

from app.dependencies.current_user import (
    get_current_user
)

from app.services import (
    dashboard_service
)

from utils.date_utils import (
    get_month_name
)

import pandas as pd

from fastapi import Query

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

templates = Jinja2Templates(
    directory="app/templates"
)

# =====================================================
# DASHBOARD Page
# =====================================================
@router.get("")
def dashboard_page(
    request: Request,
    month: str | None = Query(None),
    year: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    month_int = int(month) if month else None
    year_int = int(year) if year else None

    df = dashboard_service.load_dashboard_transactions(
        db=db,
        user_id=current_user["user_id"],
        month=month_int,
        year=year_int
    )

    metrics = dashboard_service.get_dashboard_metrics(
        df
    )

    financial_health = (
    dashboard_service.get_financial_health(
        df
    ))

    monthly_snapshot = (
    dashboard_service.get_monthly_snapshot(
        df
    ))

    spending_alert = (
    dashboard_service.get_spending_alert(
        df
    ))

    months = [
        (i, get_month_name(i))
        for i in range(1, 13)
    ]

    df = dashboard_service.load_dashboard_transactions(
        db=db,
        user_id=current_user["user_id"]
    )

    years = []

    if not df.empty:

        df = df.copy()

        df["tanggal_transaksi"] = pd.to_datetime(
            df["tanggal_transaksi"]
        )

        years = sorted(
            df["tanggal_transaksi"]
            .dt.year
            .unique()
            .tolist(),
            reverse=True
        )

    formatted_metrics = {
        "balance": f"Rp {metrics['balance']:,.0f}",
        "total_income": f"Rp {metrics['total_income']:,.0f}",
        "total_expense": f"Rp {metrics['total_expense']:,.0f}",
        "total_topup": f"Rp {metrics['total_topup']:,.0f}",
        "total_transaction": f"{metrics['total_transaction']:,}",
        "avg_transaction": f"Rp {metrics['avg_transaction']:,.0f}",
        "avg_daily": f"Rp {metrics['avg_daily']:,.0f}",
        "saving_rate": f"{metrics['saving_rate']:.2f}%"
    }

    return templates.TemplateResponse(
        request=request,
        name="dashboard/dashboard.html",
        context={
            "request": request,
            "user_name": current_user["nama"],
            "metrics": formatted_metrics, 
            "months": months, 
            "years": years, 
            "selected_month": (
                int(month)
                if month 
                else None
            ),
            "selected_year": (
                int(year)
                if year
                else None
            ), 
            "financial_health": financial_health, 
            "monthly_snapshot": monthly_snapshot, 
            "spending_alert": spending_alert
        }
    )


# =====================================================
# DASHBOARD Metrics
# =====================================================
@router.get("/metrics")
def get_dashboard_metrics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return dashboard_service.get_dashboard_metrics(
        db=db,
        user_id=current_user["user_id"]
    )


# =====================================================
# TOP Categories
# =====================================================
@router.get("/top-categories")
def get_top_categories(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return dashboard_service.get_top_expense_categories(
        db=db,
        user_id=current_user["user_id"],
        limit=limit
    )


# =====================================================
# Monthly Summary
# =====================================================
@router.get("/monthly-summary")
def get_monthly_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return dashboard_service.get_monthly_summary(
        db=db,
        user_id=current_user["user_id"]
    )


# =====================================================
# Income
# =====================================================
@router.get("/income")
def get_total_income(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return {
        "total_income": dashboard_service.get_total_income(
            db=db,
            user_id=current_user["user_id"]
        )
    }


# =====================================================
# Expense
# =====================================================
@router.get("/expense")
def get_total_expense(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return {
        "total_expense": dashboard_service.get_total_expense(
            db=db,
            user_id=current_user["user_id"]
        )
    }


# =====================================================
# TOPUP
# =====================================================
@router.get("/topup")
def get_total_topup(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return {
        "total_topup": dashboard_service.get_total_topup(
            db=db,
            user_id=current_user["user_id"]
        )
    }


# =====================================================
# BALANCE
# =====================================================
@router.get("/balance")
def get_balance(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return {
        "balance": dashboard_service.get_current_balance(
            db=db,
            user_id=current_user["user_id"]
        )
    }