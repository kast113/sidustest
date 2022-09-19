import os
import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def test_app():

    # def mock_acached(rkey):
    #     def wrapper(func):
    #         async def wrapped(*args, **kwargs):
    #             return await func(*args, **kwargs)
    #         return wrapped
    #     return wrapper
    # mocker.patch('app.utils.cache.acached', mock_acached)
    
    client = TestClient(app)
    os.environ["IS_TESTING"] = "True"
    yield client 