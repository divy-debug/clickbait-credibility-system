from src.clickbait_predictor import predict_clickbait
def test_clickbait_predictor_returns_valid_result():
    result = predict_clickbait("You Won't Believe What Happened Next!")
    assert result["predicted_label"] in {"clickbait", "no-clickbait"}
    assert 0 <= result["clickbait_probability"] <= 1
    assert 0 <= result["no_clickbait_probability"] <= 1
    total = (
        result["clickbait_probability"]
        + result["no_clickbait_probability"]
    )
    assert abs(total - 1.0) <= 0.0002

def test_clickbait_predictor_rejects_empty_headline():
    try:
        predict_clickbait("")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for empty headline.")