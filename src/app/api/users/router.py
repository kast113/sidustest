from fastapi import APIRouter

from app.api.users import views as user_views
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
    endpoint=user_views.get_user_view,
    responses={
        404: {"detail": "User not found"},
    }
)
router.add_api_route(
    '/',
    response_model=UserOutSchema,
    status_code=201,
    methods=['POST'],
    endpoint=user_views.create_user_view,
)

router.add_api_route(
    '/{user_id}/',
    response_model=UserOutSchema,
    status_code=200,
    methods=['PUT'],
    endpoint=user_views.update_user_view,
    responses={
        404: {"detail": "User not found"},
    }
)
