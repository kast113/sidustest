import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_health_check(
    ac: AsyncClient, session: AsyncSession
) -> None:
    response = await ac.get("/api/v1/health-check/")
    assert 200 == response.status_code
    assert {"success": True} == response.json()
