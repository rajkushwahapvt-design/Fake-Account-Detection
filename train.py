import numpy as np, pandas as pd, joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

FEATURES = ["profile_pic", "username_digit_ratio", "fullname_words", "fullname_digit_ratio",
            "name_equals_username", "bio_length", "external_url", "private",
            "posts", "followers", "following"]

def make_data(n=3000):
    rng = np.random.default_rng(42)
    half = n // 2
    real = pd.DataFrame({
        "profile_pic": rng.choice([0, 1], half, p=[0.05, 0.95]),
        "username_digit_ratio": rng.choice([0, 0.1, 0.2], half, p=[0.6, 0.3, 0.1]),
        "fullname_words": rng.choice([1, 2, 3], half, p=[0.2, 0.65, 0.15]),
        "fullname_digit_ratio": np.zeros(half),
        "name_equals_username": rng.choice([0, 1], half, p=[0.8, 0.2]),
        "bio_length": rng.integers(0, 120, half),
        "external_url": rng.choice([0, 1], half, p=[0.8, 0.2]),
        "private": rng.choice([0, 1], half, p=[0.6, 0.4]),
        "posts": rng.integers(5, 800, half),
        "followers": rng.integers(50, 5000, half),
        "following": rng.integers(50, 1500, half),
        "fake": 0})
    fake = pd.DataFrame({
        "profile_pic": rng.choice([0, 1], half, p=[0.65, 0.35]),
        "username_digit_ratio": rng.choice([0, 0.3, 0.5, 0.7], half, p=[0.15, 0.25, 0.3, 0.3]),
        "fullname_words": rng.choice([1, 2, 3], half, p=[0.6, 0.3, 0.1]),
        "fullname_digit_ratio": rng.choice([0, 0.2, 0.4], half, p=[0.7, 0.2, 0.1]),
        "name_equals_username": rng.choice([0, 1], half, p=[0.9, 0.1]),
        "bio_length": rng.integers(0, 40, half),
        "external_url": rng.choice([0, 1], half, p=[0.7, 0.3]),
        "private": rng.choice([0, 1], half, p=[0.8, 0.2]),
        "posts": rng.integers(0, 15, half),
        "followers": rng.integers(0, 150, half),
        "following": rng.integers(300, 7500, half),
        "fake": 1})
    return pd.concat([real, fake]).sample(frac=1, random_state=1).reset_index(drop=True)

if __name__ == "__main__":
    # Real dataset use karna ho to: df = pd.read_csv("train.csv")  (last column 'fake' = 0/1)
    df = make_data()
    X, y = df[FEATURES], df["fake"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=150, random_state=42).fit(X_tr, y_tr)
    pred = model.predict(X_te)
    print("Accuracy:", round(accuracy_score(y_te, pred), 3))
    print(classification_report(y_te, pred, target_names=["Real", "Fake"]))
    joblib.dump(model, "model.pkl")
    print("model.pkl saved")
