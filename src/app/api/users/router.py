from typing import Optional
from fastapi import APIRouter

from app.api.users.views import get_user_view, create_user_view, update_user_view
from app.api.users.output import UserOutSchema


router = APIRouter(
    tags=['Users'], 
    prefix='/api/v1/users',
)

router.add_api_route(
    '/{user_id}/',
    status_code=200,
    response_model=UserOutSchema,
    methods=['GET'],
    endpoint=get_user_view,
    responses={
        404: {"detail": "User not found"},
    }
)
router.add_api_route(
    '/',
    response_model=UserOutSchema,
    status_code=201,
    methods=['POST'],
    endpoint=create_user_view,
)

router.add_api_route(
    '/{user_id}/',
    response_model=UserOutSchema,
    status_code=201,
    methods=['PUT'],
    endpoint=update_user_view,
    responses={
        404: {"detail": "User not found"},
    }
)