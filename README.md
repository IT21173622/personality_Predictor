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

| Field | Type | Description | Range |
|-------|------|-------------|-------|
| `Time_spent_Alone` | float | Hours per day alone | 0–11 |
| `Stage_fear` | string | "Yes" or "No" | — |
| `Social_event_attendance` | float | Events per month | 0–10 |
| `Going_outside` | float | Times per week | 0–7 |
| `Drained_after_socializing` | string | "Yes" or "No" | — |
| `Friends_circle_size` | float | Number of close friends | 0–15 |
| `Post_frequency` | float | Social media posts per week | 0–10 |

> All fields are optional — missing values will be imputed automatically.

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

1. Push this folder to a **GitHub repository**
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Click **Deploy** — you'll get a public URL in ~2 minutes

The `render.yaml` file handles all configuration automatically.

---

## Local Development

```bash
pip install -r requirements.txt
python app.py
# API running at http://localhost:5000
```

---

## Files

```
├── app.py                          # Flask API
├── personality_model.pkl           # Trained Gradient Boosting model
├── requirements.txt                # Python dependencies
├── render.yaml                     # Render.com deployment config
├── Procfile                        # Gunicorn process file
├── personality_model_notebook.ipynb # Training notebook (deliverable)
└── README.md                       # This file
```
