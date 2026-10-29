import streamlit as st

from components import full_width_dataframe, history_dataframe

st.set_page_config(page_title="History")

st.title("History")
st.caption("Headlines checked in this browser session. History is cleared when the session ends.")

df = history_dataframe()

if df.empty:
    st.info("Nothing here yet. Check a headline on the main page and it will appear here.")
else:
    full_width_dataframe(
        df,
        hide_index=True,
        column_config={
            "time": "Time",
            "headline": "Headline",
            "clickbait_probability": st.column_config.ProgressColumn(
                "Clickbait", min_value=0.0, max_value=1.0, format="percent"
            ),
            "clickbait_verdict": "Clickbait verdict",
            "credibility_probability": st.column_config.ProgressColumn(
                "Credibility", min_value=0.0, max_value=1.0, format="percent"
            ),
            "credibility_verdict": "Credibility verdict",
        },
    )

    left, right = st.columns([1, 1])
    with left:
        st.download_button(
            "Download history (CSV)",
            data=df.to_csv(index=False),
            file_name="headline_history.csv",
            mime="text/csv",
        )
    with right:
        if st.button("Clear history"):
            st.session_state["history"] = []
            st.rerun()
