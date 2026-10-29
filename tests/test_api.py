from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_returns_both_model_results():
    response = client.post(
        "/predict",
        json={
            "headline": "You Won't Believe What Happened Next!",
            "article_text": (
                "The article reports on a public policy announcement "
                "and describes the details of the decision."
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert "clickbait" in data
    assert "credibility" in data


def test_predict_rejects_blank_headline():
    response = client.post(
        "/predict",
        json={
            "headline": "   ",
            "article_text": "This is a valid article text.",
        },
    )

    assert response.status_code == 422


def test_predict_rejects_blank_article_text():
    response = client.post(
        "/predict",
        json={
            "headline": "A valid headline",
            "article_text": "   ",
        },
    )

    assert response.status_code == 422