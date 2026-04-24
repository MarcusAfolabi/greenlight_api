import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.models.user import UserRole
from app.schemas.user import Token, UserCreate, UserResponse
from app.services.organization import OrganizationService
from app.services.user_service import UserService

router = APIRouter()

logger = logging.getLogger("uvicorn.error")
logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    if UserService.get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    if UserService.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    if (
        user_data.role == UserRole.HOST
        and user_data.organization is not None
        and OrganizationService.get_by_subdomain(db, user_data.organization.subdomain)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization subdomain already taken",
        )

    if user_data.role == UserRole.HOST:
        return OrganizationService.create_host_with_organization(db, user_data)

    return UserService.create_user(db, user_data)


@router.post("/login", response_model=Token)
async def login(username: str, password: str, db: Session = Depends(get_db)):
    """Login user and return an access token."""
    user = UserService.get_user_by_login(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password",
        )

    return Token(
        access_token=create_access_token(
            {
                "sub": str(user.id),
                "role": user.role.value,
                "username": user.username,
                "email": user.email,
            }
        ),
        token_type="bearer",
        role=user.role,
        username=user.username,
        email=user.email,
        id=user.id,
        is_active=user.is_active,
        created_at=user.created_at,
        )


@router.post("/refresh")
async def refresh_token():
    """Refresh access token."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Refresh token flow not implemented yet",
    )
