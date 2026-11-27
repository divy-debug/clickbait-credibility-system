import re
import requests
import streamlit as st

API_URL = "http://localhost:8000"   # change if your backend runs elsewhere

st.set_page_config(page_title="Headline Lab", page_icon="🏷️", layout="wide")

# Light theme, peach palette
BG, CARD, FIELD = "#fdf5ef", "#ffffff", "#ffffff"
INK, MUTED = "#2f2019", "#8d7268"            # warm near-black for rules & text
PEACH, PEACH_DARK, PEACH_SOFT = "#f2794b", "#d95f31", "#ffe9dd"
BORDER = "#f0dccf"
RED, GREEN, AMBER = "#c1432b", "#1a7b48", "#b9760f"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800;900&display=swap');
html, body, [class*="css"], .stApp {{ font-family: 'Manrope', sans-serif; }}
.stApp {{ background: {BG}; color: {INK}; }}
header[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ max-width: 1180px; padding-top: 2rem; }}

/* ---- header row ---- */
.brand {{ font-size: 21px; font-weight: 900; letter-spacing: .10em;
          text-transform: uppercase; color: {INK}; }}
.brand span {{ color: {PEACH}; }}
.tag {{ color: {MUTED}; text-align: right; font-size: 14px; padding-top: 8px; }}

/* ---- left column ---- */
.lede {{ font-size: 40px; font-weight: 900; line-height: 1.08; color: {INK};
         margin: 6px 0 14px 0; }}
.lede em {{ font-style: normal; color: {PEACH}; }}
.lede-sub {{ color: {MUTED}; font-size: 15px; max-width: 44ch; margin-bottom: 22px; }}

/* ---- inputs ---- */
.stTextInput input, .stTextArea textarea {{
    background: {FIELD} !important; color: {INK} !important;
    border: 2px solid {INK} !important; border-radius: 0px !important;
    font-size: 16px; padding: 13px 15px;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: {PEACH} !important; box-shadow: 0 0 0 3px {PEACH}33 !important;
}}
.stTextInput label p, .stTextArea label p {{
    color: {INK} !important; font-weight: 800; font-size: 14px;
}}

/* ---- button ---- */
.stButton button {{
    width: 100%; background: {INK}; color: #fff8f4; border: none;
    border-radius: 0; padding: 15px 0; font-weight: 800; font-size: 15px;
    letter-spacing: .12em; text-transform: uppercase;
}}
.stButton button:hover {{ background: {PEACH_DARK}; color: #ffffff; }}

/* ---- the facts label card ---- */
.label {{ background: {CARD}; border: 4px solid {INK}; border-radius: 0;
          padding: 16px 18px 12px; }}
.lt {{ font-size: 34px; font-weight: 900; letter-spacing: -.01em; color: {INK}; }}
.ls {{ font-size: 14px; color: {INK}; margin-top: 2px; }}
.thick {{ border-top: 4px solid {INK}; margin: 8px 0 4px; }}
.mid  {{ border-top: 9px solid {INK}; margin: 10px 0 2px; }} .soft {{ border-top: 3px solid {INK}; margin: 10px 0 2px; }}
.hairline {{ border-top: 1px solid {INK}; }}
div[data-testid="stTextInputRootElement"] {{ height: auto !important; overflow: visible !important; }}

/* overall credibility block */
.ov {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 0 8px; }}
.ovk {{ font-size: 14px; font-weight: 800; color: {INK}; }}
.ovv {{ font-size: 56px; font-weight: 900; line-height: 1; }}
.ovd {{ font-size: 22px; font-weight: 800; }}

/* metric rows */
.mrow {{ display: flex; align-items: center; gap: 12px; padding: 9px 0;
         border-top: 1px solid {INK}; }}
.mrow:first-of-type {{ border-top: none; }}
.mk {{ flex: 1; font-weight: 700; font-size: 15px; color: {INK}; }}
.mv {{ font-weight: 900; font-size: 18px; color: {INK}; }}

/* word badges (colour + word, so it works without colour) */
.bdg {{ color: #fff; font-weight: 800; font-size: 11px; letter-spacing: .08em;
        text-transform: uppercase; padding: 5px 11px; border-radius: 0;
        white-space: nowrap; }}
.bdg.big {{ font-size: 13px; padding: 8px 14px; }}

.foot {{ color: {MUTED}; font-size: 12px; margin-top: 10px; line-height: 1.5; }}
.err {{ border: 2px solid {RED}; background: {RED}14; color: {INK};
        border-radius: 0; padding: 12px 14px; font-weight: 700; }}
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=60, show_spinner=False)
def call_backend(headline: str, article: str):
    r = requests.post(f"{API_URL}/predict",
                      json={"headline": headline, "article_text": article}, timeout=30)
    r.raise_for_status()
    return r.json()

SOURCE_HINTS = ["according to", "study", "studies", "university", "dr.", "professor",
                "researchers", "said", "reported", "journal", "official", "spokesperson",
                "survey", "data", "evidence"]
HYPE = {"shocking", "unbelievable", "won't believe", "weird trick", "hate", "secret",
        "amazing", "insane", "overnight", "miracle", "you need", "this one", "goes viral"}


def analyse(headline: str, article: str):
    """Quick checks done in this app (not from the ML models)."""
    h, a = headline.lower(), article.lower()
    words = lambda t: {w for w in re.findall(r"[a-z]{4,}", t)}
    hw, aw = words(h), words(a)

    support = int(100 * len(hw & aw) / len(hw)) if hw else 0
    sources = sum(1 for k in SOURCE_HINTS if k in a)

    loud = article.count("!") + len(re.findall(r"\b[A-Z]{4,}\b", article))
    calm = max(0, min(100, 100 - loud * 20))

    hype = any(k in h for k in HYPE) or sum(c.isupper() for c in headline) > len(headline) * 0.3
    numbers = min(len(re.findall(r"\d+", article)), 4)
    report = min(100, 20 + numbers * 12 + (18 if sources else 0)
                     + (0 if hype else 20) + (15 if 30 <= len(article.split()) <= 400 else 0))

    return support, sources, calm, report


def badge(value, good_word, mid_word, bad_word, cut_good, cut_bad):
    if value >= cut_good:
        return good_word, GREEN
    if value >= cut_bad:
        return mid_word, AMBER
    return bad_word, RED


def badge_high_is_bad(value, low_word, mid_word, high_word, cut_low, cut_mid):
    """For scores where a bigger number is worse (clickbait wording)."""
    if value >= cut_mid:
        return high_word, RED
    if value >= cut_low:
        return mid_word, AMBER
    return low_word, GREEN


def verdict_word(cb, cr):
    if cr >= 60 and cb < 50:
        return "Safe to share", GREEN
    if cr >= 40:
        return "Check first", AMBER
    return "Do not trust", RED


h1, h2 = st.columns([1, 1])
h1.markdown('<div class="brand">Headline <span>Lab</span></div>', unsafe_allow_html=True)
h2.markdown('<div class="tag">Read the label before you share</div>', unsafe_allow_html=True)
st.write("")

left, right = st.columns([1, 1.15], gap="medium")

with left:
    st.markdown('<div class="lede">Does it pass the<br/><em>label test?</em></div>'
                '<div class="lede-sub">Paste the headline and the article. We print a facts '
                'label for it, like the one on food packets.</div>',
                unsafe_allow_html=True)

    headline = st.text_input("Article headline",
        value="Doctors HATE This One Weird Trick to Melt Belly Fat Overnight")
    article = st.text_area("Article text", height=220,
        value="A new diet plan is gaining attention online. Posts claim it can melt belly "
              "fat overnight. The plan involves eating at set times of day. No clinical "
              "trial or named expert is cited, and the author says results vary.")
    clicked = st.button("Print the label", use_container_width=True)

if clicked:
    if not headline.strip() or not article.strip():
        st.session_state.error = "Please fill in both the headline and the article text."
        st.session_state.result = None
    else:
        try:
            with st.spinner("Printing the label..."):
                st.session_state.result = (call_backend(headline, article), headline, article)
                st.session_state.error = None
        except requests.RequestException:
            st.session_state.error = f"Cannot reach the backend at {API_URL}. Is it running?"
            st.session_state.result = None

with right:
    err = st.session_state.get("error")
    res = st.session_state.get("result")

    if err:
        st.markdown(f'<div class="err">{err}</div>', unsafe_allow_html=True)
    elif not res:
        st.markdown('<div class="label"><div class="lt">Credibility Facts</div>'
                    '<div class="ls">Per 1 headline + 1 article</div>'
                    '<div class="thick"></div>'
                    '<div class="mk" style="padding:26px 0;">Paste a headline and an article '
                    'on the left, then press <b>Print the label</b>.</div></div>',
                    unsafe_allow_html=True)
    else:
        data, hl, art = res
        cb = round(data["clickbait"]["clickbait_probability"] * 100)
        cr = round(data["credibility"]["real_probability"] * 100)
        support, sources, calm, report = analyse(hl, art)

        v_word, v_col = verdict_word(cb, cr)
        c_word, c_col = badge_high_is_bad(cb, "Low", "Medium", "High", 40, 60)
        s_word, s_col = badge(support, "Good", "Okay", "Low", 60, 35)
        n_word, n_col = badge(sources, "Good", "Few", "None", 3, 1)
        t_word, t_col = badge(calm, "Good", "Fair", "Loud", 70, 40)
        r_word, r_col = badge(report, "Good", "Fair", "Weak", 60, 35)

        rows = "".join(
            f'<div class="mrow"><span class="mk">{k}</span>'
            f'<span class="mv">{v}</span>'
            f'<span class="bdg" style="background:{col};">{w}</span></div>'
            for k, v, w, col in [
                ("Clickbait wording", cb, c_word, c_col),
                ("Article backs headline", f"{support}%", s_word, s_col),
                ("Sources named", sources, n_word, n_col),
                ("Calm, neutral tone", f"{calm}%", t_word, t_col),
                ("Reads like a report", f"{report}%", r_word, r_col),
            ])

        st.markdown(f"""
        <div class="label">
          <div class="lt">Credibility Facts</div>
          <div class="ls">Per 1 headline + 1 article</div>
          <div class="thick"></div>
          <div class="ov">
            <div>
              <div class="ovk">Overall credibility</div>
              <div class="ovv" style="color:{v_col};">{cr}<span class="ovd">/100</span></div>
            </div>
            <div class="bdg big" style="background:{v_col};">{v_word}</div>
          </div>
          <div class="mid"></div>
          {rows}
          <div class="soft"></div>
          <div class="foot">Credibility and clickbait scores come from the FastAPI backend.
          The last four rows are quick checks done in this app. Red marks and green marks
          always carry a word too, so they work without colour.</div>
        </div>""", unsafe_allow_html=True)