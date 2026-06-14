# app/routers/profile.py

from fastapi import (
    APIRouter,
    Depends,
    Query, 
    Request
)

from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.database.connection import (
    get_db
)

from app.dependencies.current_user import (
    get_current_user
)

from app.services.profile_service import (
    ProfileService
)

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


# =====================================================
# GET PROFILE
# =====================================================

@router.get("/")
def get_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return ProfileService.get_profile(
        db=db,
        user_id=current_user["user_id"]
    )

# =====================================================
# LOGOUT PROFILE
# =====================================================

@router.get("/logout")
def logout(request:Request):
    request.session.clear()

    return RedirectResponse(
        url="/auth/login", 
        status_code=303
    )