# app/routers/analytics.py

from fastapi import (
    APIRouter, 
    Depends, 
    Request
)

from fastapi.templating import(
    Jinja2Templates
)

from sqlalchemy.orm import Session

from app.database.connection import(
    get_db
)

from app.dependencies.current_user import(
    get_current_user
)

from app.services.analytics_service import (
    AnalyticsService
)

router = APIRouter(
    prefix="/analytics", 
    tags=["Analytics"]
)

templates = Jinja2Templates(
    directory="app/templates"
)

# ==========================================
# ANALYTICS PAGE
# ==========================================

@router.get("/page")
def analytics_page(
    request: Request, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return templates.TemplateResponse(
        request=request, 
        name="analytics/analytics.html", 
        context={
            "request": request, 
            "user_name": current_user["nama"]
        }
    )

# analytics_router.py
@router.get("/chart-data")
def get_chart_data(
    month: int | None = None,
    year: int | None = None,
    period: str | None = None,
    category: str | None = None,
    subcategory_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return AnalyticsService.get_chart_data(
        db=db,
        user_id=current_user["user_id"],
        month=month,
        year=year,
        period=period,
        category=category,
        subcategory_id=subcategory_id
    )