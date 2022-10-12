from fastapi import APIRouter, status

from app.api.users import views as user_views
from app.api.users.output import UserOutSchema


router = APIRouter(
    tags=['Users'],
    prefix='/api/v1/users',
)

router.add_api_route(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[UserOutSchema],
    methods=['GET'],
    endpoint=user_views.get_user_view_all
)

router.add_api_route(
    '/{user_id}/',
    status_code=200,
    response_model=UserOutSchema,
    methods=['GET'],
    endpoint=user_views.get_user_view,
    responses={
        status.HTTP_404_NOT_FOUND: {"detail": "User not found"},
    }
)
router.add_api_route(
    '/',
    response_model=UserOutSchema,
    status_code=status.HTTP_201_CREATED,
    methods=['POST'],
    endpoint=user_views.create_user_view
)

router.add_api_route(
    '/{user_id}/',
    response_model=UserOutSchema,
    status_code=status.HTTP_200_OK,
    methods=['PUT'],
    endpoint=user_views.update_user_view,
    responses={
        status.HTTP_403_FORBIDDEN: {"detail": "Forbidden"},
    }
)

router.add_api_route(
    '/{user_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
    methods=['DELETE'],
    endpoint=user_views.delete_user_view,
    responses={
        status.HTTP_403_FORBIDDEN: {"detail": "Forbidden"},
    }
)
