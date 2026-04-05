import re
import string
from pathlib import Path
from typing import List, Tuple

import joblib
import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"

stop_words = set(ENGLISH_STOP_WORDS) - {"no", "not", "nor"}

sent_model = joblib.load(MODEL_DIR / "sentiment_model.joblib")
topic_model = joblib.load(MODEL_DIR / "topic_model.joblib")

sentiment_base_risk = {"positive": 0, "neutral": 1, "negative": 2}
topic_risk_adjustment = {
    "layoffs": 2,
    "inflation": 2,
    "recession": 2,
    "supply_chain": 1,
    "rates": 2,
    "housing": 1,
    "trade": 1,
    "oil": 1,
    "banking": 2,
    "retail": 1,
    "earnings": 0,
    "markets": 0,
    "technology": 0
}
high_risk_keywords = {
    "crash", "plunge", "collapse", "bankruptcy", "default",
    "layoffs", "lawsuit", "recession", "fraud", "shutdown",
    "decline", "drop", "loss", "slump", "disruption", "tariff"
}
medium_risk_keywords = {
    "inflation", "slowdown", "uncertain", "mixed", "pressure",
    "warning", "cut", "cuts", "weakness", "volatility", "fall",
    "rate", "housing", "trade"
}

def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = text.split()
    tokens = [tok for tok in tokens if tok not in stop_words and len(tok) > 2]
    return " ".join(tokens)

def keyword_risk_boost(text: str) -> Tuple[int, List[str]]:
    words = set(text.split())
    matched = sorted(words.intersection(high_risk_keywords.union(medium_risk_keywords)))
    score = 0
    if words.intersection(high_risk_keywords):
        score += 2
    if words.intersection(medium_risk_keywords):
        score += 1
    return score, matched

def confidence_adjustment(sentiment_conf: float, topic_conf: float) -> int:
    adj = 0
    if sentiment_conf > 0.85:
        adj += 1
    if topic_conf > 0.85:
        adj += 1
    return adj

def numeric_to_risk(score: int) -> str:
    if score <= 1:
        return "low"
    if score <= 3:
        return "medium"
    return "high"

def predict_headline(text: str):
    cleaned = clean_text(text)
    sentiment_probs = sent_model.predict_proba([cleaned])[0]
    topic_probs = topic_model.predict_proba([cleaned])[0]

    sentiment = sent_model.classes_[int(np.argmax(sentiment_probs))]
    topic = topic_model.classes_[int(np.argmax(topic_probs))]
    sentiment_conf = float(np.max(sentiment_probs))
    topic_conf = float(np.max(topic_probs))

    keyword_adj, matched = keyword_risk_boost(cleaned)
    base = sentiment_base_risk.get(sentiment, 1)
    topic_adj = topic_risk_adjustment.get(topic, 0)
    conf_adj = confidence_adjustment(sentiment_conf, topic_conf)
    total_score = base + topic_adj + keyword_adj + conf_adj
    risk = numeric_to_risk(total_score)

    explanation = (
        f"The model predicted {sentiment} sentiment and the topic {topic}. "
        f"Risk was adjusted using the topic weight ({topic_adj}), matched keywords ({keyword_adj}), "
        f"and confidence boost ({conf_adj})."
    )

    return {
        "headline": text,
        "cleaned_text": cleaned,
        "sentiment": sentiment,
        "sentiment_confidence": round(sentiment_conf, 4),
        "topic": topic,
        "topic_confidence": round(topic_conf, 4),
        "risk": risk,
        "risk_score": int(total_score),
        "matched_keywords": matched,
        "explanation": explanation,
    }
