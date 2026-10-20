# Financial Headline Risk Analyzer

A full-stack NLP prototype that turns a financial headline into sentiment, a topic, and an explainable risk label.

The project connects a Next.js interface to a FastAPI backend. Two scikit-learn pipelines classify sentiment and topic; a rule-based layer combines those results with keywords and confidence thresholds to produce a low, medium, or high risk label.

## Features

- Headline input with examples covering inflation, earnings, banking, trade, and housing.
- Positive, neutral, or negative sentiment with model confidence.
- Topic classification and topic confidence.
- A numeric risk score, matched keywords, and a plain-language explanation.
- Separate Python API and TypeScript frontend.
- A training script and checked-in model artifacts.

## Architecture

```text
Next.js / React interface
        |
POST /analyze {"headline": "..."}
        |
Text cleaning
        |
TF-IDF + Logistic Regression (sentiment and topic)
        |
Topic weights + keyword signals + confidence adjustments
        |
Sentiment, topic, risk label, score, keywords, explanation
```

## Run locally

Use Python 3.12 or later, as specified by `api/pyproject.toml`, and a Node.js version compatible with the frontend's Next.js 15 dependency. Run the following commands from this directory in two separate terminals.

### 1. Start the API

```bash
cd api
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload --port 8000
```

On Windows, use your virtual environment's Windows activation command. The API loads `model/sentiment_model.joblib` and `model/topic_model.joblib` at import time. Use the dependencies in `requirements.txt` to match the saved models.

### 2. Start the interface

```bash
cd web
npm install
npm run dev
```

Open [localhost:3000](http://localhost:3000). The frontend uses `http://localhost:8000` when `NEXT_PUBLIC_API_BASE_URL` is unset.

For a separately hosted API, set `NEXT_PUBLIC_API_BASE_URL` to that API's base URL in the frontend environment before building. The backend exposes `app:app` as its ASGI application.

## API example

Check that the API is running:

```bash
curl http://localhost:8000/
```

Analyze a headline:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"headline":"Major bank warns of rising defaults in commercial real estate"}'
```

The JSON response includes:

| Field | Meaning |
| --- | --- |
| `headline`, `cleaned_text` | Original input and normalized model input |
| `sentiment`, `sentiment_confidence` | Sentiment prediction and model probability |
| `topic`, `topic_confidence` | Topic prediction and model probability |
| `risk`, `risk_score` | Rule-based label and numeric score |
| `matched_keywords` | Keywords contributing to the score |
| `explanation` | Summary of how the score was assembled |

Interactive API documentation is available at [localhost:8000/docs](http://localhost:8000/docs) while FastAPI is running.

## Train the models

From `api/` with the virtual environment active:

```bash
python train_artifacts.py
```

The script reads `finance_train_advanced_v2.csv`, fits separate TF-IDF/Logistic Regression pipelines for `Label` and `topic`, and writes both artifacts into `model/`. It overwrites the existing artifacts. The test CSV is included but is not evaluated by this script.

## Interpreting the output

The risk score is a heuristic based on headline language. Topic weights, keyword matches, sentiment, and confidence adjustments are defined in `api/model_logic.py`. Model confidence is a classification probability, rather than a measured probability of an economic event. The repository does not implement time-series forecasting or a FRED/World Bank macroeconomic early-warning model.

## Repository map

```text
api/app.py                 FastAPI endpoints and request schema
api/model_logic.py         Text cleaning, inference, and risk rules
api/train_artifacts.py     Model training script
api/model/                 Saved scikit-learn pipelines
api/*.csv                  Training/test data
web/app/page.tsx           Interactive frontend and API calls
web/app/globals.css        Interface styling
```

Built by [Marcus Hunt](https://github.com/MarcusHunt090), exploring the intersection of machine learning, economics, and interpretable software.
