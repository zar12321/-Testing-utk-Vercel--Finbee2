# run.py

import uvicorn

from fastapi import (
    FastAPI
)

from fastapi.staticfiles import (
    StaticFiles
)

from fastapi.responses import (
    RedirectResponse
)

from starlette.middleware.sessions import (
    SessionMiddleware
)

from app.routers.auth import (
    router as auth_router
)

from app.routers.dashboard import (
    router as dashboard_router
)

from app.routers.transaction import (
    router as transaction_router
)

from app.routers.profile import (
    router as profile_router
)

from app.routers.analysis import (
    router as analysis_router
)

from app.routers.ai import (
    router as ai_router
)


app = FastAPI(
    title="FinBee",
    version="1.0.0"
)

# =====================================================
# SESSION
# =====================================================

app.add_middleware(
    SessionMiddleware,
    secret_key="finbee-secret-key"
)

# =====================================================
# STATIC FILES
# =====================================================

app.mount(
    "/static",
    StaticFiles(
        directory="static"
    ),
    name="static"
)

# =====================================================
# ROUTERS
# =====================================================

app.include_router(auth_router)

app.include_router(dashboard_router)

app.include_router(transaction_router)

app.include_router(profile_router)

app.include_router(analysis_router)

app.include_router(ai_router)

# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():

    return RedirectResponse(
        url="/auth/login"
    )

# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":

    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )