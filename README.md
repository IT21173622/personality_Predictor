# Personality Predictor — Introvert vs Extrovert

A machine learning API that predicts whether a person is an **Introvert** or **Extrovert** from behavioral characteristics.

## Model Performance

| Metric            | Score  |
|-------------------|--------|
| Test Accuracy     | 92.2%  |
| AUC-ROC           | 0.961  |
| 5-Fold CV Accuracy| 96.6%  |
| F1-Score (both)   | 0.92   |

**Algorithm:** Gradient Boosting Classifier (200 estimators)

---

## API Reference

### `POST /predict`

Returns the predicted personality type.

**Request Body (JSON):**

```json
{
  "Time_spent_Alone": 8,
  "Stage_fear": "Yes",
  "Social_event_attendance": 1,
  "Going_outside": 2,
  "Drained_after_socializing": "Yes",
  "Friends_circle_size": 3,
  "Post_frequency": 2
}
```



**Response:**

```json
{
  "personality": "Introvert",
  "confidence": 0.9401,
  "probabilities": {
    "Introvert": 0.9401,
    "Extrovert": 0.0599
  }
}
```

### `GET /health`

```json
{ "status": "ok", "model_loaded": true }
```

---

## Quick Test

```bash
curl -X POST https://YOUR_RENDER_URL/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Time_spent_Alone": 8,
    "Stage_fear": "Yes",
    "Social_event_attendance": 1,
    "Going_outside": 2,
    "Drained_after_socializing": "Yes",
    "Friends_circle_size": 3,
    "Post_frequency": 2
  }'
```

---

## Deployment to Render.com (Free)
https://personality-predictor-jvx8.onrender.com/

## Streamlit Cloud
https://personality-predictor-cv3x6scmyej6rfvejp5tgs.streamlit.app/


---

## Local Development

```bash
pip install -r requirements.txt
python app.py
# API running at http://localhost:5000

streamlit run streamlit_app.py
http://localhost:8501
```



