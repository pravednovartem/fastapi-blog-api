from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import app_http_error, auth_dependency, db_dependency, oauth2_form_dep
from app.exceptions import AppError
from app.models import User
from app.schemas import LoginRequest, RegisterRequest, TokenResponse, UserOut
from app.use_cases.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(data: RegisterRequest, db: AsyncSession = db_dependency):
    try:
        _, token = await AuthService(db).register(data)
    except AppError as exc:
        raise app_http_error(exc) from exc
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = oauth2_form_dep,
    db: AsyncSession = db_dependency,
):
    try:
        _, token = await AuthService(db).login(
            LoginRequest(username=form.username, password=form.password),
        )
    except AppError as exc:
        raise app_http_error(exc) from exc
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserOut)
async def me(current_user: User = auth_dependency):
    return current_user
