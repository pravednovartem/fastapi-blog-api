from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import app_http_error, auth_dependency, db_dependency, oauth2_form_dep
from app.exceptions import AppError
from app.models import User
from app.schemas import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserOut,
)
from app.use_cases.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(data: RegisterRequest, db: AsyncSession = db_dependency):
    try:
        _, access, refresh = await AuthService(db).register(data)
    except AppError as exc:
        raise app_http_error(exc) from exc
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = oauth2_form_dep,
    db: AsyncSession = db_dependency,
):
    try:
        _, access, refresh = await AuthService(db).login(
            LoginRequest(username=form.username, password=form.password),
        )
    except AppError as exc:
        raise app_http_error(exc) from exc
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    data: RefreshTokenRequest,
    db: AsyncSession = db_dependency,
):
    try:
        access, new_refresh = await AuthService(db).refresh(data.refresh_token)
    except AppError as exc:
        raise app_http_error(exc) from exc
    return TokenResponse(access_token=access, refresh_token=new_refresh)


@router.post("/logout")
async def logout(
    data: RefreshTokenRequest,
    db: AsyncSession = db_dependency,
):
    await AuthService(db).logout(data.refresh_token)
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserOut)
async def me(current_user: User = auth_dependency):
    return current_user
