import streamlit as st

st.set_page_config(page_title="How it works")

st.title("How it works")
st.write(
    "Paste a news headline and the app gives two separate scores: how much it "
    "looks like **clickbait**, and how much it reads like **credible news**."
)

st.header("The two models")

st.subheader("1. Clickbait detector")
st.markdown(
    """
- **Data:** 19,538 labelled headlines, about 24% clickbait.
- **Features:** word and two-word patterns (TF-IDF), plus 10 hand-built signals:
  exclamation marks, question marks, "you" and "your", a leading number, capital
  letters, headline length, curiosity phrases such as "won't believe", and
  superlatives such as "best" or "ultimate".
- **Model:** logistic regression with class weighting, so the rarer clickbait
  class is not ignored.
- **Decision rule:** a headline is flagged at a clickbait probability of 0.50,
  the cut-off that gave the best F1 score on the validation set.
"""
)

st.subheader("2. Credibility model")
st.markdown(
    """
- **Data:** 38,720 headlines from the ISOT dataset, real (Reuters) and fake
  news, after removing duplicates and any headline that appeared in both classes.
- **Features:** word and two-word patterns (TF-IDF) from the headline only.
- **Model:** logistic regression with class weighting.
- **Cleaning:** the "(Reuters)" tag was stripped from article text so the model
  cannot simply look for it.
"""
)

st.header("How well do they work?")
st.caption("Measured on the validation set. A final test-set score is still to be reported.")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Clickbait detector**")
    st.metric("ROC-AUC", "0.76")
    st.metric("F1 on the clickbait class", "0.54")
    st.caption("Precision 0.50, recall 0.60. It is a useful signal, not a verdict.")
with col2:
    st.markdown("**Credibility model**")
    st.metric("Accuracy", "94.7%")
    st.metric("ROC-AUC", "0.99")
    st.caption("Strong on this dataset. See the limits below before trusting it elsewhere.")

st.header("Read the results with care")
st.warning(
    "**Credibility is not fact-checking.** The model learned what real and fake "
    "headlines in one dataset *look like*. It never checks whether a claim is true."
)
st.markdown(
    """
- **Narrow training data.** The credibility data is US political news from
  2016 to 2017. Headlines about other topics, other years or other countries may
  score poorly even when they are accurate.
- **It partly learns style.** Words such as "says", "factbox" and "Brexit" push
  a headline toward *real*; "video", "watch", "breaking" and "just" push it toward
  *fake*. That is publisher style as much as truthfulness.
- **Clickbait is subjective.** The clickbait model gets about one in two flagged
  headlines right, and misses some real clickbait. Borderline scores are
  genuinely borderline.
- **Short text.** Both models see only the headline, not the article.
"""
)

st.header("Reading the colours")
st.success("Green: not clickbait, or reads like credible news.")
st.warning("Amber: borderline or uncertain.")
st.error("Red: likely clickbait, or reads like unreliable content.")
