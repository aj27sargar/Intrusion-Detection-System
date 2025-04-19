from utils import load_data, preprocess_data
from sklearn.ensemble import IsolationForest
import joblib

def train_nids_model():
    print("🔹 Loading training data...")
    df_train = load_data("data/KDDTrain+.txt")
    X_train, y_train = preprocess_data(df_train)

    print("🔹 Training Isolation Forest...")
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(X_train)

    print("✅ Saving model to nids_model.pkl")
    joblib.dump(model, "nids_model.pkl")

if __name__ == "__main__":
    train_nids_model()
