from collections.abc import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.interface.routers import rttm_router


@pytest.fixture
def app() -> FastAPI:
    test_app = FastAPI()
    test_app.include_router(rttm_router, prefix="/rttm")

    return test_app


@pytest.fixture
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def clear_dependency_overrides(app: FastAPI) -> Generator[None, None, None]:
    app.dependency_overrides.clear()

    yield

    app.dependency_overrides.clear()