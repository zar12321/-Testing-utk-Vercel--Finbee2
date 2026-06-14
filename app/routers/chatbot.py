# app/routers/chatbot.py

from fastapi import (
    APIRouter, 
    Depends, 
    Request, 
    HTTPException
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

from core.ai_model import (
    AI_MODELS
)

from app.services.chatbot_service import (
    ChatbotService
)

from app.schemas.chatbot import (
    ChatRequest,
    ChatResponse,
    TestConnectionRequest,
    ChatbotActionResponse
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
            "user_name": current_user["nama"], 
            "ai_models": AI_MODELS
        }
    )

# ==========================================
# CHATBOT ROUTER
# ==========================================
@router.get("/models")
def get_available_model():
    return {
        "success": True, 
        "models": AI_MODELS
    }

# ==========================================
# TEST CONNECTION
# ==========================================
@router.post(
    "/test-connection",
    response_model=ChatbotActionResponse
    )

def test_connection(
    request: TestConnectionRequest
):

    try:

        ChatbotService.test_connection(
            provider=request.provider,
            model_name=request.model_name,
            api_key=request.api_key
        )

        return ChatbotActionResponse(
            success=True,
            message="Berhasil terhubung ke model."
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# ==========================================
# SEND MESSAGE
# ==========================================
@router.post(
    "/send-message",
    response_model=ChatResponse
)
def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:

        ai_response = (
            ChatbotService.send_message(
                db=db,
                user_id=current_user["user_id"],
                provider=request.provider,
                model_name=request.model_name,
                api_key=request.api_key,
                message=request.message,
                temperature=request.temperature
            )
        )

        return ChatResponse(
            success=True,
            response=ai_response
        )

    except Exception as e:

        print("Error send message")
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# ==========================================
# GET CHAT HISTORY
# ==========================================
from app.repositories.chatbot_repository import (
    get_chat_history
)

@router.get("/history")
def load_chat_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    history = get_chat_history(
        db=db,
        user_id=current_user["user_id"]
    )

    return {
        "success": True,
        "history": history
    }

# ==========================================
# CLEAR CHAT HISTORY
# ==========================================
from app.repositories.chatbot_repository import (
    clear_chat_history
)

@router.delete("/history")
def delete_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    clear_chat_history(
        db=db,
        user_id=current_user["user_id"]
    )

    return {
        "success": True,
        "message": "Riwayat chat berhasil dihapus."
    }