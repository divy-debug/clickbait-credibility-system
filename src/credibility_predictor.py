from pathlib import Path
import joblib
# Resolve the project root from this file's location
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "credibility_model.joblib"
VECTORIZER_PATH = MODEL_DIR / "credibility_tfidf.joblib"
# Load the trained artifacts once when this module is imported
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
if not VECTORIZER_PATH.exists():
    raise FileNotFoundError(
        f"TF-IDF vectorizer not found: {VECTORIZER_PATH}"
    )
credibility_model = joblib.load(MODEL_PATH)
credibility_tfidf = joblib.load(VECTORIZER_PATH)
def predict_credibility(headline: str, article_text: str) -> dict:
    """
    Predict the model's Fake/Real class from a headline and article text.
    Labels:
        0 = Fake
        1 = Real
    Probabilities are model estimates, not verified truth scores.
    """
    if not isinstance(headline, str) or not headline.strip():
        raise ValueError("Headline must be a non-empty string.")
    if not isinstance(article_text, str) or not article_text.strip():
        raise ValueError("Article text must be a non-empty string.")
    combined_text = headline.strip() + " " + article_text.strip()
    text_vector = credibility_tfidf.transform([combined_text])
    predicted_label = int(credibility_model.predict(text_vector)[0])
    probabilities = credibility_model.predict_proba(text_vector)[0]
    return {
        "predicted_class": "Real" if predicted_label == 1 else "Fake",
        "fake_probability": round(float(probabilities[0]), 4),
        "real_probability": round(float(probabilities[1]), 4),
    }