# app/routers/ai.py

from fastapi import (
    APIRouter
)

from app.schemas.ai import (
    AIChatRequest,
    AIChatResponse,
    AIAnalysisRequest,
    AIAnalysisResponse
)

from app.services.ai_service import (
    AIService
)

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


# =====================================================
# CHATBOT
# =====================================================

@router.post(
    "/chat",
    response_model=AIChatResponse
)
def chat_with_ai(
    request: AIChatRequest
):

    response = AIService.generate_response(
        provider="Gemini",
        model_name="gemini-2.5-flash",
        prompt=request.message
    )

    return AIChatResponse(
        response=response,
        provider="Gemini"
    )


# =====================================================
# FINANCIAL ANALYSIS
# =====================================================

@router.post(
    "/analysis",
    response_model=AIAnalysisResponse
)
def analyze_financial_summary(
    request: AIAnalysisRequest
):

    summary = request.summary

    financial_summary = f"""
Total Income: {summary.total_income}
Total Expense: {summary.total_expense}
Total Topup: {summary.total_topup}
Balance: {summary.balance}
Transaction Count: {summary.transaction_count}
Top Categories: {', '.join(summary.top_categories)}
"""

    insight = AIService.generate_financial_advice(
        provider="Gemini",
        model_name="gemini-2.5-flash",
        financial_summary=financial_summary
    )

    return AIAnalysisResponse(
        insight=insight,
        recommendation=insight,
        risk_level="Medium",
        provider="Gemini"
    )