import secrets
from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from ninja.security import HttpBearer

from common.models import SiteSettings
from users.models import AuthToken

User = get_user_model()


def _get_site_settings() -> SiteSettings:
    """Get or create SiteSettings for the current site."""
    site = Site.objects.get_current()
    obj, _ = SiteSettings.objects.get_or_create(site=site, defaults={})
    return obj


def _get_token_lifetime_days() -> int:
    """Get token lifetime from site config or default."""
    try:
        ss = _get_site_settings()
        sec = ss.get_security()
        return int(sec.get("token_lifetime_days", 7))
    except Exception:
        return 7


def generate_token() -> str:
    return secrets.token_urlsafe(48)


def create_token_for_user(user: User) -> AuthToken:
    lifetime_days = _get_token_lifetime_days()
    expires_at = datetime.now(timezone.utc) + timedelta(days=lifetime_days)
    token = AuthToken.objects.create(
        user=user,
        key=generate_token(),
        expires_at=expires_at,
    )
    return token


def get_user_from_token(token_key: str) -> User | None:
    try:
        token = AuthToken.objects.select_related("user").get(key=token_key)
        if token.user.is_active and not token.is_expired:
            return token.user
    except AuthToken.DoesNotExist:
        return None
    return None


def delete_user_tokens(user: User) -> int:
    return AuthToken.objects.filter(user=user).delete()[0]


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token: str) -> User | None:
        return get_user_from_token(token)


# ============================================================
# Role-based permission helpers
# ============================================================


def writer_required(user: User) -> User:
    if user.role not in (User.Role.WRITER, User.Role.EDITOR, User.Role.ADMIN):
        raise PermissionDenied("Writer role required.")
    return user


def editor_required(user: User) -> User:
    if user.role not in (User.Role.EDITOR, User.Role.ADMIN):
        raise PermissionDenied("Editor role required.")
    return user


def subscriber_required(user: User) -> User:
    if user.role not in (
        User.Role.SUBSCRIBER,
        User.Role.WRITER,
        User.Role.EDITOR,
        User.Role.ADMIN,
    ):
        raise PermissionDenied("Subscriber role required.")
    return user


# ============================================================
# Email verification helpers
# ============================================================


def create_verification_token(user: User) -> str:
    """Generate and store a verification token. Returns the raw token."""
    token = secrets.token_urlsafe(32)
    user.verification_token = token
    user.verification_token_expires = datetime.now(timezone.utc) + timedelta(hours=24)
    user.save(update_fields=["verification_token", "verification_token_expires"])
    return token


def verify_token(user: User, token: str) -> bool:
    """Check if a verification token is valid and not expired."""
    if not user.verification_token or user.verification_token != token:
        return False
    if (
        user.verification_token_expires
        and datetime.now(timezone.utc) >= user.verification_token_expires
    ):
        return False
    return True


def create_password_reset_token(user: User) -> str:
    """Generate and store a password reset token. Returns the raw token."""
    token = secrets.token_urlsafe(32)
    user.password_reset_token = token
    user.password_reset_token_expires = datetime.now(timezone.utc) + timedelta(hours=1)
    user.save(update_fields=["password_reset_token", "password_reset_token_expires"])
    return token


def verify_password_reset_token(user: User, token: str) -> bool:
    """Check if a password reset token is valid."""
    if not user.password_reset_token or user.password_reset_token != token:
        return False
    if (
        user.password_reset_token_expires
        and datetime.now(timezone.utc) >= user.password_reset_token_expires
    ):
        return False
    return True


def send_verification_email(user: User, token: str) -> None:
    """Send a verification email to the user. Uses console backend in DEBUG mode."""
    # The frontend verification URL can be configured from site settings
    verify_url = f"http://localhost:4321/auth/verify?token={token}&email={user.email}"
    subject = "Verify your MERIDIAN account"
    message = (
        f"Hello {user.first_name or user.username},\n\n"
        f"Please verify your email address by visiting:\n{verify_url}\n\n"
        f"This link expires in 24 hours.\n\n"
        f"If you did not create this account, you can ignore this email."
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL or "noreply@meridian.com",
        recipient_list=[user.email],
        fail_silently=True,
    )


def send_password_reset_email(user: User, token: str) -> None:
    """Send a password reset email. Uses console backend in DEBUG mode."""
    reset_url = (
        f"http://localhost:4321/auth/reset-password?token={token}&email={user.email}"
    )
    subject = "Reset your MERIDIAN password"
    message = (
        f"Hello {user.first_name or user.username},\n\n"
        f"You requested a password reset. Visit this link:\n{reset_url}\n\n"
        f"This link expires in 1 hour.\n\n"
        f"If you did not request this, you can ignore this email."
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL or "noreply@meridian.com",
        recipient_list=[user.email],
        fail_silently=True,
    )
