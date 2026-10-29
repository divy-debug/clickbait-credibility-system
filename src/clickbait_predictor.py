
import re
from pathlib import Path

import joblib
import pandas as pd

# --------------------------------------------------
# 1. Locate the project and saved model artifacts
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "models"

MODEL_PATH = MODEL_DIR / "clickbait_model.joblib"
TFIDF_PATH = MODEL_DIR / "clickbait_tfidf.joblib"
SCALER_PATH = MODEL_DIR / "clickbait_scaler.joblib"

for path in (MODEL_PATH, TFIDF_PATH, SCALER_PATH):
    if not path.exists():
        raise FileNotFoundError(f"Required model artifact not found: {path}")

clickbait_model = joblib.load(MODEL_PATH)
clickbait_tfidf = joblib.load(TFIDF_PATH)
clickbait_scaler = joblib.load(SCALER_PATH)

# --------------------------------------------------
# 2. Define handcrafted feature extraction
# --------------------------------------------------

CURIOSITY_PHRASES = [
    "won't believe",
    "wont believe",
    "this is why",
    "here's why",
    "heres why",
    "what happens next",
    "will blow your mind",
    "you need to know",
    "will make you",
    "doesn't want you to know",
    "doesnt want you to know",
    "unbelievable",
    "shocking",
    "secret",
]

SUPERLATIVE_WORDS = {
    "best", "worst", "biggest", "greatest", "most",
    "least", "largest", "smallest", "highest", "lowest",
    "fastest", "ultimate", "top"
}

def extract_handcrafted_features(headline: str) -> dict:
    """Extract the 10 handcrafted headline features."""

    text = headline.strip()
    lower_text = text.lower()

    words = re.findall(r"\b\w+\b", text)
    letters = [char for char in text if char.isalpha()]

    uppercase_ratio = (
        sum(char.isupper() for char in letters) / len(letters)
        if letters else 0.0
    )

    features = {
        "exclamation_count": text.count("!"),
        "question_count": text.count("?"),
        "you_count": len(re.findall(r"\byou\b", lower_text)),
        "your_count": len(re.findall(r"\byour\b", lower_text)),
        "starts_with_number": int(bool(re.match(r"^\s*\d", text))),
        "uppercase_ratio": uppercase_ratio,
        "word_count": len(words),
        "char_count": len(text),
        "curiosity_phrase_count": sum(
            lower_text.count(phrase) for phrase in CURIOSITY_PHRASES
        ),
        "has_superlative": int(
            any(word.lower() in SUPERLATIVE_WORDS for word in words)
        ),
    }

    return features

# --------------------------------------------------
# 3. Validate feature compatibility with training
# --------------------------------------------------

EXPECTED_FEATURES = [
    "exclamation_count",
    "question_count",
    "you_count",
    "your_count",
    "starts_with_number",
    "uppercase_ratio",
    "word_count",
    "char_count",
    "curiosity_phrase_count",
    "has_superlative",
]

if hasattr(clickbait_scaler, "feature_names_in_"):
    SCALER_FEATURES = list(clickbait_scaler.feature_names_in_)
else:
    SCALER_FEATURES = EXPECTED_FEATURES

if len(SCALER_FEATURES) != 10:
    raise ValueError(
        f"Expected 10 handcrafted features, got {len(SCALER_FEATURES)}."
    )

if clickbait_tfidf.transform(["test"]).shape[1] != len(
    clickbait_tfidf.vocabulary_
):
    raise ValueError("TF-IDF vocabulary and transformed dimensions disagree.")

expected_model_features = (
    clickbait_tfidf.transform(["test"]).shape[1]
    + len(SCALER_FEATURES)
)

if clickbait_model.n_features_in_ != expected_model_features:
    raise ValueError(
        "Classifier input dimension does not match TF-IDF plus handcrafted "
        f"features: model={clickbait_model.n_features_in_}, "
        f"expected={expected_model_features}."
    )

# --------------------------------------------------
# 4. Predict clickbait probability for a headline
# --------------------------------------------------

def predict_clickbait(headline: str) -> dict:
    """
    Return the clickbait label and model-estimated probability.

    IMPORTANT: The feature formulas must match the training notebook.
    """

    if not isinstance(headline, str) or not headline.strip():
        raise ValueError("Headline must be a non-empty string.")

    headline = headline.strip()

    # TF-IDF features
    tfidf_features = clickbait_tfidf.transform([headline])

    # Handcrafted features in the scaler's training order
    raw_features = extract_handcrafted_features(headline)
    feature_frame = pd.DataFrame(
        [[raw_features[name] for name in SCALER_FEATURES]],
        columns=SCALER_FEATURES,
    )

    scaled_features = clickbait_scaler.transform(feature_frame)

    # Combine sparse TF-IDF and handcrafted features
    from scipy.sparse import csr_matrix, hstack

    combined_features = hstack(
        [tfidf_features, csr_matrix(scaled_features)],
        format="csr",
    )

    if combined_features.shape[1] != clickbait_model.n_features_in_:
        raise ValueError(
            "Input feature count differs from the trained classifier."
        )

    probabilities = clickbait_model.predict_proba(combined_features)[0]
    classes = list(clickbait_model.classes_)

    clickbait_index = classes.index("clickbait")
    clickbait_probability = float(probabilities[clickbait_index])

    predicted_label = (
        "clickbait" if clickbait_probability >= 0.5 else "no-clickbait"
    )

    return {
        "predicted_label": predicted_label,
        "clickbait_probability": round(clickbait_probability, 4),
        "no_clickbait_probability": round(1.0 - clickbait_probability, 4),
    }