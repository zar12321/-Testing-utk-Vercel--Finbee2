# app/services/profile_service.py

from datetime import datetime
from sqlalchemy.orm import Session

from app.database.db import (
    get_user_by_id,
    update_user_profile,
    get_transactions_by_user_id,
    load_monthly_plan,
    save_monthly_plan
)

from app.schemas.profile import (
    ProfileUpdateRequest,
    ProfileUpdateResponse
)



class ProfileService:

    @staticmethod
    def get_profile(
        db: Session,
        user_id: int
    ):

        user = get_user_by_id(
            db=db,
            user_id=user_id
        )

        if not user:
            raise ValueError(
                "User tidak ditemukan."
            )

        return user
    
    @staticmethod
    def update_profile(
        db: Session,
        user_id: int,
        payload
    ):

        user = get_user_by_id(
            db=db,
            user_id=user_id
        )

        if not user:
            raise ValueError(
                "User tidak ditemukan."
            )

        update_user_profile(
            db=db,
            user_id=user_id,
            nama=payload.nama,
            login_identifier=payload.login_identifier,
            umur=payload.umur,
            pekerjaan=payload.pekerjaan
        )

        return {
            "success": True,
            "message": "Profile berhasil diperbarui."
        }  
        

    @staticmethod
    def get_financial_summary(
        db: Session,
        user_id: int
    ):

        transactions_df = (
            get_transactions_by_user_id(
                db=db,
                user_id=user_id
            )
        )

        if transactions_df.empty:

            return {
                "total_income": 0,
                "total_expense": 0,
                "balance": 0,
                "total_transaction": 0,
                "saving_rate": 0
            }

        total_income = float(
            transactions_df[
                transactions_df[
                    "transaction_type"
                ] == "income"
            ]["amount"].sum()
        )

        total_expense = float(
            transactions_df[
                transactions_df[
                    "transaction_type"
                ] == "expense"
            ]["amount"].sum()
        )

        balance = (
            total_income
            - total_expense
        )

        total_transaction = len(
            transactions_df
        )

        saving_rate = (
            (balance / total_income) * 100
            if total_income > 0
            else 0
        )

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "total_transaction": total_transaction,
            "saving_rate": saving_rate
        }

    @staticmethod
    def get_monthly_plan(
        db: Session,
        user_id: int,
        bulan: int | None = None,
        tahun: int | None = None
    ):

        if bulan is None:
            bulan = datetime.now().month

        if tahun is None:
            tahun = datetime.now().year

        return load_monthly_plan(
            db=db,
            user_id=user_id,
            bulan=bulan,
            tahun=tahun
        )

    @staticmethod
    def save_monthly_target(
        db: Session,
        user_id: int,
        pemasukan_bulanan: float,
        target_bulanan: float,
        bulan: int | None = None,
        tahun: int | None = None
    ):

        if bulan is None:
            bulan = datetime.now().month

        if tahun is None:
            tahun = datetime.now().year

        save_monthly_plan(
            db=db,
            user_id=user_id,
            bulan=bulan,
            tahun=tahun,
            pemasukan_bulanan=pemasukan_bulanan,
            target_bulanan=target_bulanan
        )

        return True