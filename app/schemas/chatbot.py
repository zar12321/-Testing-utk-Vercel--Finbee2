# app/schemas/chatbot.py

from pydantic import (
    BaseModel,
    Field
)

from typing import Optional


# =====================================================
# CHAT REQUEST
# =====================================================

class ChatRequest(
    BaseModel
):

    provider: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    model_name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    api_key: str = Field(
        ...,
        min_length=1
    )

    message: str = Field(
        ...,
        min_length=1
    )

    temperature: float = Field(
        default=0.7, 
        ge=0, 
        le=1
    ) 

# =====================================================
# CHAT RESPONSE
# =====================================================

class ChatResponse(
    BaseModel
):

    success: bool

    response: str


# =====================================================
# TEST CONNECTION REQUEST
# =====================================================

class TestConnectionRequest(
    BaseModel
):

    provider: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    model_name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    api_key: str = Field(
        ...,
        min_length=1
    )


# =====================================================
# TEST CONNECTION RESPONSE
# =====================================================

class TestConnectionResponse(
    BaseModel
):

    success: bool

    message: str


# =====================================================
# CHAT HISTORY RESPONSE
# =====================================================

class ChatHistoryResponse(
    BaseModel
):

    chat_id: int

    role: str

    message: str

    provider: Optional[str] = None

    model_name: Optional[str] = None

    created_at: str


# =====================================================
# GENERAL RESPONSE
# =====================================================

class ChatbotActionResponse(
    BaseModel
):

    success: bool
    message: str