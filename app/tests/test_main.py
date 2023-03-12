from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"response": "hello The MAMA AI"}


def test_dates_nasa():
    start_date = "2022/11/11"
    end_date = "2022/11/14"
    response = client.get(f"/objects?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 400 or response.status_code == 422



