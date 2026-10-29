"""

Run:  streamlit run demo_app.py

Replace `fake_analyze` with real analyzer. , `run_analysis` and `add_to_history`.
"""
import streamlit as st

from components import add_to_history, run_analysis, show_result

st.set_page_config(page_title="Headline checker")


def fake_analyze(headline: str) -> dict:
    """Crude placeholder. NOT the real model."""
    lower = headline.lower()
    if "boom" in lower:
        raise RuntimeError("demo failure: analyzer crashed")
    bait_words = ["won't believe", "shocking", "secret", "you ", "!", "this is why"]
    hits = [w for w in bait_words if w in lower]
    click_p = min(0.1 + 0.25 * len(hits), 0.95)
    cred_p = max(0.9 - 0.3 * len(hits), 0.05)
    return {
        "headline": headline,
        "clickbait": {
            "probability": click_p,
            "reasons": [
                {"label": f"Contains “{w.strip()}”", "detail": "Common clickbait phrasing."}
                for w in hits
            ],
        },
        "credibility": {
            "probability": cred_p,
            "reasons": ["Sensational wording"] if hits else ["Neutral, report-style wording"],
        },
        "features": {
            "exclamation_count": headline.count("!"),
            "word_count": len(headline.split()),
            "char_count": len(headline),
        },
    }


st.title("Headline checker")
headline = st.text_input("Paste a headline", placeholder="e.g. Senate passes budget bill 52-48")

if st.button("Check headline", type="primary"):
    result = run_analysis(fake_analyze, headline)
    st.session_state["last_result"] = result
    if result is not None:
        add_to_history(result)

if st.session_state.get("last_result"):
    show_result(st.session_state["last_result"])
