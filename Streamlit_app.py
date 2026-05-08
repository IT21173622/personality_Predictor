import streamlit as st
import requests

# ── CONFIG ────────────────────────────────────────────────────────────────────
API_URL = "https://personality-predictor-jvx8.onrender.com/predict"   
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Personality Predictor",
    page_icon="🧠",
    layout="centered",
)

st.title("🧠 Personality Predictor")
st.caption("Find out if you're an **Introvert** or **Extrovert** based on your behavioral traits.")
st.divider()

# ── INPUT FORM ────────────────────────────────────────────────────────────────
with st.form("prediction_form"):
    st.subheader("Enter your details")

    col1, col2 = st.columns(2)

    with col1:
        time_alone = st.slider(
            "⏱ Time spent alone (hrs/day)",
            min_value=0, max_value=11, value=5, step=1,
        )
        social_events = st.slider(
            "🎉 Social event attendance (per month)",
            min_value=0, max_value=10, value=4, step=1,
        )
        going_outside = st.slider(
            "🚶 Going outside (times/week)",
            min_value=0, max_value=7, value=4, step=1,
        )

    with col2:
        friends = st.slider(
            "👥 Friends circle size",
            min_value=0, max_value=15, value=7, step=1,
        )
        post_freq = st.slider(
            "📱 Social media posts (per week)",
            min_value=0, max_value=10, value=3, step=1,
        )
        stage_fear = st.radio(
            "🎤 Stage fear?",
            options=["No", "Yes"],
            horizontal=True,
        )
        drained = st.radio(
            "😓 Drained after socializing?",
            options=["No", "Yes"],
            horizontal=True,
        )

    submitted = st.form_submit_button("🔮 Predict Personality", use_container_width=True)

# ── PREDICTION ────────────────────────────────────────────────────────────────
if submitted:
    payload = {
        "Time_spent_Alone":          time_alone,
        "Stage_fear":                stage_fear,
        "Social_event_attendance":   social_events,
        "Going_outside":             going_outside,
        "Drained_after_socializing": drained,
        "Friends_circle_size":       friends,
        "Post_frequency":            post_freq,
    }

    with st.spinner("Calling prediction API..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=15)
            response.raise_for_status()
            result = response.json()

        except requests.exceptions.ConnectionError:
            st.error("❌ Could not reach the API. Make sure your Flask server is running and the URL is correct.")
            st.stop()
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. The API may be waking up (free tier). Try again in a moment.")
            st.stop()
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ API returned an error: {e}")
            st.stop()
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
            st.stop()

    # ── RESULT DISPLAY ────────────────────────────────────────────────────────
    st.divider()
    personality   = result["personality"]
    confidence    = result["confidence"]
    intro_prob    = result["probabilities"]["Introvert"]
    extro_prob    = result["probabilities"]["Extrovert"]

    is_extrovert = personality == "Extrovert"
    emoji  = "🟣" if is_extrovert else "🔵"
    color  = "violet" if is_extrovert else "blue"

    st.subheader("Result")
    st.markdown(f"## {emoji} You are an **:{color}[{personality}]**")

    m1, m2, m3 = st.columns(3)
    m1.metric("Prediction",   personality)
    m2.metric("Confidence",   f"{confidence * 100:.1f}%")
    m3.metric("Top feature",  "Stage fear" if stage_fear == "Yes" else "Social activity")

    st.write("#### Probability breakdown")
    st.progress(intro_prob, text=f"Introvert — {intro_prob * 100:.1f}%")
    st.progress(extro_prob, text=f"Extrovert — {extro_prob * 100:.1f}%")

    with st.expander("📦 Raw API response"):
        st.json(result)