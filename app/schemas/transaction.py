# app/schemas/transaction.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


# =====================================================
# CREATE TRANSACTION
# =====================================================

class TransactionCreateRequest(BaseModel):

    category_id: int

    tanggal_transaksi: datetime

    transaction_type: str

    tujuan_transaksi: str = Field(
        ...,
        min_length=1,
        max_length=255
    )

    keterangan: Optional[str] = None

    payment_method: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    amount: float = Field(
        ...,
        gt=0
    )

    raw_category: Optional[str] = None


# =====================================================
# UPDATE TRANSACTION
# =====================================================

class TransactionUpdateRequest(BaseModel):

    category_id: int

    tanggal_transaksi: datetime

    transaction_type: str

    tujuan_transaksi: str = Field(
        ...,
        min_length=1,
        max_length=255
    )

    keterangan: Optional[str] = None

    payment_method: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    amount: float = Field(
        ...,
        gt=0
    )

    raw_category: Optional[str] = None


# =====================================================
# DELETE TRANSACTION
# =====================================================

class TransactionDeleteRequest(BaseModel):

    transaction_id: int


# =====================================================
# TRANSACTION RESPONSE
# =====================================================

class TransactionResponse(BaseModel):

    transaction_id: int

    user_id: int

    category_id: Optional[int] = None

    category_name: Optional[str] = None

    tanggal_transaksi: datetime

    transaction_type: str

    tujuan_transaksi: str

    keterangan: Optional[str] = None

    payment_method: str

    amount: float

    source: Optional[str] = None

    raw_category: Optional[str] = None


# =====================================================
# GENERAL RESPONSE
# =====================================================

class TransactionActionResponse(
    BaseModel
):
    success: bool
    message: str

    filename: str | None = None

    inserted_count: int | None = None
    skipped_count: int | None = None    