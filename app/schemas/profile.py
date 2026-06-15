# app/schemas/profile.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


# =====================================================
# PROFILE RESPONSE
# =====================================================

class ProfileResponse(BaseModel):

    user_id: int

    nama: str

    login_identifier: str

    login_type: str

    umur: Optional[int] = None

    pekerjaan: Optional[str] = None

    created_at: Optional[datetime] = None

    profile_photo: Optional[str] = None



# =====================================================
# UPDATE PROFILE REQUEST
# =====================================================
from pydantic import model_validator

class ProfileUpdateRequest(BaseModel):

    nama: str = Field(
        ..., 
        min_length=1, 
        max_length=100
    )

    login_identifier: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    umur: Optional[int] = Field(
        default=None,
        ge=0,
        le=120
    )

    pekerjaan: Optional[str] = Field(
        ...,
        max_length=100
    )

    password: Optional[str] = None

    confirm_password: Optional[str] = None




# =====================================================
# CHANGE PASSWORD REQUEST
# =====================================================

class ChangePasswordRequest(BaseModel):

    current_password: str

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128
    )


# =====================================================
# PROFILE RESPONSE MESSAGE
# =====================================================

class ProfileUpdateResponse(BaseModel):

    success: bool

    message: str

    profile: Optional[ProfileResponse] = None