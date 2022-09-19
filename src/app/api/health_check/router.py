from fastapi import APIRouter

from app.api.health_check.views import health_check


router = APIRouter(
    tags=['Health Check'], 
    prefix='/api/v1/health-check',
)

router.add_api_route(
    '/',
    status_code=200,
    methods=['GET'],
    endpoint=health_check,
)
