"""Integración contra PostgreSQL real. Se omite si no hay conexión."""

import os
import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.db.database import get_db
from src.db.models import Base
from src.main import app

DB_URL = os.getenv(
    "TEST_DATABASE_URL",
    os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://app_user:app_password@localhost:5432/app_db",
    ),
)


@pytest.fixture
async def client():
    engine = create_async_engine(DB_URL)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    except OSError:
        pytest.skip("postgres no disponible")
    TestSession = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
    await engine.dispose()


async def test_create_item(client):
    response = await client.post(
        "/api/v1/items", json={"name": "Test", "description": "Test item"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test"


async def test_list_items(client):
    await client.post("/api/v1/items", json={"name": "A"})
    response = await client.get("/api/v1/items")
    assert response.status_code == 200
    assert any(i["name"] == "A" for i in response.json())


async def test_get_item(client):
    created = await client.post("/api/v1/items", json={"name": "B"})
    item_id = created.json()["id"]
    response = await client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id


async def test_get_item_404(client):
    response = await client.get(f"/api/v1/items/{uuid.uuid4()}")
    assert response.status_code == 404
