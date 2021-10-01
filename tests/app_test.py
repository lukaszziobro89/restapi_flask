import pytest
from app.run import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_status(client):
    status_code = client.get('/student/luq').status_code
    assert status_code == 200
