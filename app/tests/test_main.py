from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"detail": "hello The MAMA AI"}


def test_invalid_dates_format_nasa():
    start_date = "2022/11/11"
    end_date = "2022/11/14"
    response = client.get(f"/objects?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 400 or response.status_code == 422


def test_valid_dates_format_nasa():
    start_date = "2022-11-11"
    end_date = "2022-11-14"
    response = client.get(f"/objects?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200


def test_invalid_dates_range_nasa():
    start_date = "2022-11-14"
    end_date = "2022-11-11"
    response = client.get(f"/objects?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 400


def test_missing_start_date():
    end_date = "2022-11-11"
    response = client.get(f"/objects?&end_date={end_date}")
    assert response.status_code == 400


def test_missing_end_date():
    start_date = "2022-11-11"
    response = client.get(f"/objects?&start_date={start_date}")
    assert response.status_code == 400
