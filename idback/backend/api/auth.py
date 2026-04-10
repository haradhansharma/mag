import secrets
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import PermissionDenied
from ninja.security import HttpBearer

from users.models import AuthToken

User = get_user_model()


def generate_token() -> str:
    return secrets.token_urlsafe(48)


def create_token_for_user(user: User) -> AuthToken:
    token = AuthToken.objects.create(
        user=user,
        key=generate_token(),
    )
    return token


def get_user_from_token(token_key: str) -> User | None:
    try:
        token = AuthToken.objects.select_related("user").get(key=token_key)
        if token.user.is_active:
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
