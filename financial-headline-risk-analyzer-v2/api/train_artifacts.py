import re
import string
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"

stop_words = set(ENGLISH_STOP_WORDS) - {"no", "not", "nor"}

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = text.split()
    tokens = [tok for tok in tokens if tok not in stop_words and len(tok) > 2]
    return " ".join(tokens)

def build_model():
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.95, sublinear_tf=True)),
        ("model", LogisticRegression(max_iter=3000, class_weight="balanced", solver="lbfgs")),
    ])

def main():
    train_path = BASE_DIR / "finance_train_advanced_v2.csv"
    df_train = pd.read_csv(train_path)

    df_train["clean_text"] = df_train["Sentence"].apply(clean_text)

    sent_model = build_model()
    topic_model = build_model()

    sent_model.fit(df_train["clean_text"], df_train["Label"])
    topic_model.fit(df_train["clean_text"], df_train["topic"])

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(sent_model, MODEL_DIR / "sentiment_model.joblib")
    joblib.dump(topic_model, MODEL_DIR / "topic_model.joblib")
    print("Saved trained artifacts to", MODEL_DIR)

if __name__ == "__main__":
    main()
