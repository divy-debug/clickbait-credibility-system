from src.clickbait_predictor import predict_clickbait
from src.credibility_predictor import predict_credibility
def analyze_news(headline: str, article_text: str) -> dict:
    """
    Run both models on the same news item.
    Clickbait prediction uses the headline.
    Credibility prediction uses the headline and article text.
    """
    if not isinstance(headline, str) or not headline.strip():
        raise ValueError("Headline must be a non-empty string.")
    if not isinstance(article_text, str) or not article_text.strip():
        raise ValueError("Article text must be a non-empty string.")
    clickbait_result = predict_clickbait(headline)
    credibility_result = predict_credibility(
        headline,
        article_text
    )
    return {
        "headline": headline.strip(),
        "clickbait": clickbait_result,
        "credibility": credibility_result,
    }