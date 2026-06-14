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
    prefix="/chatbot", 
    tags=["Chatbot"]
)

templates = Jinja2Templates(
    directory="app/templates"
)

# ==========================================
# CHATBOT PAGE
# ==========================================

@router.get("/page")
def chatbot_page(
    request: Request, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return templates.TemplateResponse(
        request=request, 
        name="chatbot/chatbot.html", 
        context={
            "request": request, 
            "user_name": current_user["nama"]
        }
    )