from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.authentication import JWTAuthentication
from ..models.user import User
from ..schemas.user import UserCreate, UserRead, UserUpdate
from .config import settings

DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_user_db():
    async with AsyncSessionLocal() as session:
        yield SQLAlchemyUserDatabase(User, session)

jwt_authentication = JWTAuthentication(secret=settings.SECRET_KEY, lifetime_seconds=3600, tokenUrl="auth/jwt/login")
auth_backends = [jwt_authentication]

fastapi_users = FastAPIUsers[User, str](
    get_user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserRead,
)
