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
MODEL_PATH = MODEL_DIR / "incident_severity_model.joblib"

MODEL_DIR.mkdir(exist_ok=True)

def main():
    data = pd.read_csv(DATA_PATH)

    x_train, x_test, y_train, y_test = train_test_split(
        data["message"],
        data["severity"],
        test_size=0.25,
        random_state=42,
        stratify=data["severity"]
    )

    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("classifier", LogisticRegression(max_iter=1000))
    ])

    model.fit(x_train, y_train)

    predictions = model.predict(x_test)

    print("Model Evaluation:")
    print(classification_report(y_test, predictions, zero_division=0))

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    main()
