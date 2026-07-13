from pathlib import Path
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "sample_incidents.csv"
MODEL_DIR = ROOT_DIR / "models"

MODEL_DIR.mkdir(exist_ok=True)


def train_model(version: str, ngram_range=(1, 1), c_value=1.0):
    data = pd.read_csv(DATA_PATH)

    x_train, x_test, y_train, y_test = train_test_split(
        data["message"],
        data["severity"],
        test_size=0.25,
        random_state=42,
        stratify=data["severity"]
    )

    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=ngram_range)),
        ("classifier", LogisticRegression(max_iter=1000, C=c_value))
    ])

    model.fit(x_train, y_train)

    predictions = model.predict(x_test)

    print(f"\nModel Evaluation for {version}:")
    print(classification_report(y_test, predictions, zero_division=0))

    model_path = MODEL_DIR / f"incident_severity_{version}.joblib"
    joblib.dump(model, model_path)

    print(f"Model {version} saved to {model_path}")


def main():
    train_model("v1", ngram_range=(1, 1), c_value=1.0)
    train_model("v2", ngram_range=(1, 2), c_value=0.8)


if __name__ == "__main__":
    main()
