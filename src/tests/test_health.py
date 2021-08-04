"""
routes/health.py 테스트
"""
from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_index(client: TestClient, session: Session) -> None:
    """
    index 테스트
    :param client:
    :param session:
    :return:
    """
    # response = client.get(f"{settings.API_VERSION_PREFIX}/health")
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
