from __future__ import annotations

import json
from datetime import datetime

import pandas as pd
import streamlit as st

# Thresholds. 0.50 is the best-F1 cut-off from the clickbait notebook (02).
# The other bands are display choices for the colour-coding, not model outputs.
CLICKBAIT_THRESHOLD = 0.50
CLICKBAIT_WARN = 0.35
CREDIBILITY_HIGH = 0.70
CREDIBILITY_LOW = 0.40

_LEVEL_RENDERERS = {
    "good": st.success,
    "mixed": st.warning,
    "bad": st.error,
}


# --------------------------------------------------------------------------
# Verdict logic (pure functions, easy to unit test)
# --------------------------------------------------------------------------
def clickbait_verdict(prob: float) -> tuple[str, str]:
    """Return (level, text) for a clickbait probability."""
    if prob >= CLICKBAIT_THRESHOLD:
        return "bad", "Likely clickbait"
    if prob >= CLICKBAIT_WARN:
        return "mixed", "Borderline: some clickbait signals"
    return "good", "Not clickbait"


def credibility_verdict(prob: float) -> tuple[str, str]:
    """Return (level, text) for a probability that the headline looks real."""
    if prob >= CREDIBILITY_HIGH:
        return "good", "Reads like credible news"
    if prob >= CREDIBILITY_LOW:
        return "mixed", "Uncertain credibility"
    return "bad", "Reads like unreliable content"


def _probability(section: dict, name: str) -> float:
    """Pull a 0..1 probability out of a result section or raise a clear error."""
    if not isinstance(section, dict) or "probability" not in section:
        raise ValueError(f"result['{name}'] must be a dict with a 'probability' key")
    value = float(section["probability"])
    if value != value:  # NaN
        raise ValueError(f"result['{name}']['probability'] is NaN")
    return min(max(value, 0.0), 1.0)


def _normalise_reasons(reasons) -> list[dict]:
    """Accept strings or dicts and always return [{'label', 'detail'}]."""
    out = []
    for item in reasons or []:
        if isinstance(item, str):
            out.append({"label": item, "detail": ""})
        elif isinstance(item, dict):
            out.append(
                {
                    "label": str(item.get("label", "")),
                    "detail": str(item.get("detail", "")),
                }
            )
    return out


# --------------------------------------------------------------------------
# Rendering helpers
# --------------------------------------------------------------------------
def _render_verdict(level: str, text: str) -> None:
    _LEVEL_RENDERERS[level](text)


def _score_block(title: str, prob: float, help_text: str) -> None:
    st.metric(title, f"{prob:.0%}", help=help_text)
    st.progress(prob)


def _reasons_block(reasons: list[dict], empty_text: str) -> None:
    if not reasons:
        st.caption(empty_text)
        return
    for r in reasons[:3]:
        st.markdown(f"- {r['label']}")
    with st.expander("See details"):
        detail_rows = [r for r in reasons if r["detail"]]
        if detail_rows:
            for r in detail_rows:
                st.markdown(f"**{r['label']}**  \n{r['detail']}")
        else:
            st.caption("No further detail for this result.")


def full_width_dataframe(df: pd.DataFrame, **kwargs) -> None:
    """st.dataframe at full width on both old and new Streamlit versions."""
    try:
        st.dataframe(df, width="stretch", **kwargs)
    except (TypeError, st.errors.StreamlitAPIException):
        st.dataframe(df, use_container_width=True, **kwargs)


def _download_button(result: dict) -> None:
    payload = json.dumps(result, indent=2, default=str)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    kwargs = dict(
        label="Download result (JSON)",
        data=payload,
        file_name=f"headline_check_{stamp}.json",
        mime="application/json",
        key="download_current_result",
    )
    try:
        # Newer Streamlit: don't rerun the app when the button is clicked.
        st.download_button(on_click="ignore", **kwargs)
    except TypeError:
        st.download_button(**kwargs)


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------
def show_result(result: dict) -> None:
    """Render one analysis result. Never raises: bad input shows st.error."""
    try:
        _show_result(result)
    except Exception as exc:  # noqa: BLE001 - UI boundary, show anything
        st.error(f"Could not display this result: {exc}")


def _show_result(result: dict) -> None:
    if not isinstance(result, dict):
        raise ValueError("result must be a dict")
    if result.get("error"):
        st.error(f"The analyzer reported an error: {result['error']}")
        return

    click = result.get("clickbait")
    cred = result.get("credibility")
    click_p = _probability(click, "clickbait")
    cred_p = _probability(cred, "credibility")

    headline = result.get("headline")
    if headline:
        st.subheader(f"“{headline}”")

    col_click, col_cred = st.columns(2)

    with col_click:
        st.markdown("#### Clickbait")
        _score_block(
            "Clickbait likelihood",
            click_p,
            "Probability that the headline is clickbait. Higher is worse.",
        )
        _render_verdict(*clickbait_verdict(click_p))
        _reasons_block(
            _normalise_reasons(click.get("reasons")),
            "No specific signals were reported.",
        )

    with col_cred:
        st.markdown("#### Credibility")
        _score_block(
            "Credibility score",
            cred_p,
            "Probability that the headline resembles real news reporting. Higher is better.",
        )
        _render_verdict(*credibility_verdict(cred_p))
        _reasons_block(
            _normalise_reasons(cred.get("reasons")),
            "No specific signals were reported.",
        )

    features = result.get("features")
    if features:
        with st.expander("Headline features the model measured"):
            full_width_dataframe(
                pd.DataFrame(
                    {"feature": list(features), "value": list(features.values())}
                ),
                hide_index=True,
            )

    st.caption(
        "Credibility here means the headline's wording resembles real news reports. "
        "It does not check whether the story is true."
    )
    _download_button(result)


def run_analysis(analyze_fn, headline: str):
    """Call the analyzer safely. Returns its result, or None after st.error."""
    text = (headline or "").strip()
    if not text:
        st.warning("Enter a headline first.")
        return None
    try:
        return analyze_fn(text)
    except Exception as exc:  # noqa: BLE001 - show any analyzer failure
        st.error(
            "The analyzer failed on this headline. Please try again, or try a "
            f"different headline.\n\nDetails: {type(exc).__name__}: {exc}"
        )
        return None


# --------------------------------------------------------------------------
# History (kept in the browser session; used by pages/2_History.py)
# --------------------------------------------------------------------------
def add_to_history(result: dict) -> None:
    """Append a finished result to this session's history."""
    try:
        click_p = _probability(result.get("clickbait"), "clickbait")
        cred_p = _probability(result.get("credibility"), "credibility")
    except ValueError:
        return  # don't record results we could not display
    history = st.session_state.setdefault("history", [])
    history.append(
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "headline": result.get("headline", ""),
            "clickbait_probability": round(click_p, 4),
            "clickbait_verdict": clickbait_verdict(click_p)[1],
            "credibility_probability": round(cred_p, 4),
            "credibility_verdict": credibility_verdict(cred_p)[1],
        }
    )


def history_dataframe() -> pd.DataFrame:
    return pd.DataFrame(st.session_state.get("history", []))
