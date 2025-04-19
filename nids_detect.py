from utils import load_data, preprocess_data
import joblib
from sklearn.metrics import classification_report

def test_nids_model():
    print("🔹 Loading test data...")
    df_test = load_data("data/KDDTest+.txt")
    X_test, y_test = preprocess_data(df_test)

    print("🔹 Loading trained model...")
    model = joblib.load("nids_model.pkl")

    print("🔹 Making predictions...")
    predictions = model.predict(X_test)

    # Isolation Forest outputs: 1 (normal), -1 (anomaly)
    # Convert to: 0 (normal), 1 (anomaly)
    y_pred = [0 if p == 1 else 1 for p in predictions]

    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    test_nids_model()
