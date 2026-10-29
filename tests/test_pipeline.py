import pytest
from src.pipeline import analyze_news
def test_analyze_news_returns_both_predictions():
    result = analyze_news(
        "You Won't Believe What Happened Next!",
        (
            "The article reports on a public policy announcement "
            "and describes the details of the decision."
        ),
    )

    assert "clickbait" in result
    assert "credibility" in result
    assert result["clickbait"]["predicted_label"] in {
        "clickbait",
        "no-clickbait",
    }
    assert result["credibility"]["predicted_class"] in {
        "Fake",
        "Real",
    }
def test_analyze_news_rejects_empty_headline():
    with pytest.raises(ValueError):
        analyze_news("", "This is the article text.")
def test_analyze_news_rejects_empty_article():
    with pytest.raises(ValueError):
        analyze_news("A sample headline", "")