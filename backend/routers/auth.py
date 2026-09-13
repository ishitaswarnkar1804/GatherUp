import hashlib
import os
import secrets
from datetime import datetime, timedelta
from urllib.parse import quote

from dotenv import load_dotenv

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.email_service import send_verification_email
from backend.models import EmailVerification, User
from backend.schemas import (
    EmailOnlyRequest,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse
)
from backend.security import (
    create_access_token,
    get_current_user,
    verify_password
)


load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

password_hash = PasswordHash.recommended()
VERIFICATION_TTL_MINUTES = 30


def hash_verification_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_verification_token(db: Session, user: User) -> str:
    raw_token = secrets.token_urlsafe(32)
    token_hash = hash_verification_token(raw_token)
    expires_at = datetime.utcnow() + timedelta(minutes=VERIFICATION_TTL_MINUTES)

    record = (
        db.query(EmailVerification)
        .filter(EmailVerification.user_id == user.id)
        .first()
    )

    if record:
        record.token_hash = token_hash
        record.expires_at = expires_at
        record.verified_at = None
    else:
        record = EmailVerification(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
            verified_at=None
        )
        db.add(record)

    return raw_token


def build_verification_url(request: Request, token: str) -> str:
    configured_base = os.getenv("PUBLIC_BASE_URL", "").strip()

    if configured_base:
        base = configured_base.rstrip("/")
    else:
        base = str(request.base_url).rstrip("/")

    return f"{base}/auth/verify-email?token={quote(token)}"


def send_user_verification_email(
    request: Request,
    db: Session,
    user: User
):
    token = create_verification_token(db, user)
    verification_url = build_verification_url(request, token)

    send_verification_email(
        recipient=user.email,
        first_name=user.first_name,
        verification_url=verification_url
    )


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: RegisterRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists."
        )

    new_user = User(
        first_name=user_data.first_name.strip(),
        last_name=user_data.last_name.strip(),
        email=str(user_data.email).lower(),
        password_hash=password_hash.hash(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/resend-verification"
)
def resend_verification(
    data: EmailOnlyRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == str(data.email).lower())
        .first()
    )

    if not user:
        return {
            "message": "If an account exists for that email, a verification message has been sent."
        }

    verification = (
        db.query(EmailVerification)
        .filter(EmailVerification.user_id == user.id)
        .first()
    )

    if verification and verification.verified_at is not None:
        return {
            "message": "This email address is already verified."
        }

    try:
        send_user_verification_email(request, db, user)
        db.commit()
    except RuntimeError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error)
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="We could not send the verification email. Check the email delivery settings and try again."
        )

    return {
        "message": "A new verification email has been sent."
    }


@router.get(
    "/verify-email"
)
def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    token_hash = hash_verification_token(token)

    record = (
        db.query(EmailVerification)
        .filter(EmailVerification.token_hash == token_hash)
        .first()
    )

    if not record:
        return RedirectResponse(
            url="/verify-email?status=invalid",
            status_code=status.HTTP_303_SEE_OTHER
        )

    if record.verified_at is not None:
        return RedirectResponse(
            url="/verify-email?status=success",
            status_code=status.HTTP_303_SEE_OTHER
        )

    if not record.expires_at or record.expires_at < datetime.utcnow():
        return RedirectResponse(
            url="/verify-email?status=expired",
            status_code=status.HTTP_303_SEE_OTHER
        )

    record.verified_at = datetime.utcnow()
    record.token_hash = None
    record.expires_at = None

    db.commit()

    return RedirectResponse(
        url="/verify-email?status=success",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    user_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == str(user_data.email).lower())
        .first()
    )

    if not user or not verify_password(
        user_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verification = (
        db.query(EmailVerification)
        .filter(EmailVerification.user_id == current_user.id)
        .first()
    )

    return {
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "email_verified": bool(
            verification and verification.verified_at is not None
        )
    }
