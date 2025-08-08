from fastapi import APIRouter, Depends
from fastapi_users import models
from ..core.auth import fastapi_users, auth_backends, jwt_authentication
from ..schemas.user import UserCreate, UserRead

router = APIRouter()

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth/jwt",
    tags=["auth"],
)
router.add_api_route(
    "/auth/me",
    endpoint=fastapi_users.current_user,
    methods=["GET"],
    dependencies=[Depends(jwt_authentication)],
    response_model=UserRead,
    tags=["auth"],
)
