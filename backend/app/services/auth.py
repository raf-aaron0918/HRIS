from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserRole


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username=username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.full_name.asc(), User.username.asc()).all()


def create_user(
    db: Session,
    *,
    username: str,
    full_name: str,
    email: str,
    password: str,
    role: str,
    is_active: bool = True,
) -> User:
    user = User(
        username=username.strip(),
        full_name=full_name.strip(),
        email=email.strip().lower(),
        hashed_password=get_password_hash(password),
        role=UserRole(role),
        is_active=is_active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
