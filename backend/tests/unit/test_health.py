from httpx import ASGITransport, AsyncClient

from src.main import app


async def test_health():  # ponytail: asyncio_mode=auto, sin marker
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/health")
    assert response.status_code == 500  # CAMBIO INTENCIONAL: 200 -> 500 (falla)
    assert response.json() == {"status": "ok"}
