# app/routers/profile.py

from fastapi import (
    APIRouter,
    Depends,
    Query, 
    Request, 
    File, 
    UploadFile, 
    HTTPException
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

from app.schemas.profile import (
    ProfileUpdateRequest
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

# =====================================================
# UPDATE PROFILE
# =====================================================
@router.put("/update")
def update_profile(
    payload: ProfileUpdateRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:

        result = ProfileService.update_profile(
            db=db,
            user_id=current_user["user_id"],
            payload=payload
        )

        request.session["nama"] = (
            payload.nama
        )

        request.session["login_identifier"] = (
            payload.login_identifier
        )

        request.session["pekerjaan"] = (
            payload.pekerjaan
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =====================================================
# CEK USERNAME UDH DIPAKE APA BELOM DI PROFILE
# =====================================================
from app.database.db import login_user_by_identifier

@router.get("/check-username-update")
def check_username_update(
    login_identifier: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = login_user_by_identifier(
        db=db,
        login_identifier=login_identifier
    )

    if not user:
        return {
            "available": True
        }

    if user.user_id == current_user["user_id"]:
        return {
            "available": True
        }

    return {
        "available": False
    }


# =====================================================
# UPLOAD PROFILE PHOTO
# =====================================================

@router.post("/upload-photo")
async def upload_profile_photo(
    request: Request,
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    
    print("MASUK ROUTER")
    try: 
        allowed_extensions = {
            ".jpg", 
            ".jpeg",
            ".png", 
            ".webp", 
        }

        extension = (
            "." + 
            file.filename.split(".")[-1].lower()
        )

        if extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Format file tidak didukung. "
                    "Gunakan JPG, JPEG, PNG, atau WEBP"
                )
            )
        
        contents = await file.read()

        max_size = 2 * 1024 * 1024

        if len(contents) > max_size:
            raise HTTPException(
                status_code=400, 
                detail=
                    "Ukuran file maksimal 2 MB"
            )
        
        result = ProfileService.upload_profile_photo(
            db=db, 
            user_id=current_user["user_id"], 
            file_contents=contents, 
            filename=file.filename
        )

        request.session["profile_photo"] = (
            result["profile_photo"]
        )

        print(
            "SESSION PHOTO:",
            request.session.get("profile_photo")
        )

        return result
    
    except HTTPException:
        raise

    except Exception as e:

        print(
            "Upload Error:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=
                "Terjadi kesalahan saat upload foto"
        )