# app/schemas/profile.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

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

    @model_validator(mode="after")
    def validate_password_pair(self):

        if self.password:

            if len(self.password) < 8:
                raise ValueError(
                    "Password minimal 8 karakter."
                )

            if self.password != self.confirm_password:
                raise ValueError(
                    "Konfirmasi password tidak cocok."
                )

        return self



