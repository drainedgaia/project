import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
import joblib
import os

def train_and_save_model():
    """
    Trains a Naive Bayes model and saves it along with the scaler.
    """
    # Load the dataset
    try:
        df = pd.read_csv("data/synthetic_student_performance.csv")
    except FileNotFoundError:
        print("Error: 'data/synthetic_student_performance.csv' not found.")
        print("Please make sure the dataset is available in the 'data' directory.")
        return

    # Drop StudentID as it is not needed for training
    if "StudentID" in df.columns:
        df = df.drop("StudentID", axis=1)

    # Define features (X) and target (y)
    X = df.drop("GradeClass", axis=1)
    y = df["GradeClass"]

    # Save feature columns to a file to ensure prediction consistency
    os.makedirs("models", exist_ok=True)
    joblib.dump(X.columns.tolist(), "models/feature_columns.pkl")

    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train the Naive Bayes model
    model = GaussianNB()
    model.fit(X_scaled, y)

    # Save the model and the scaler
    joblib.dump(model, "models/naive_bayes_model.pkl")
    joblib.dump(scaler, "models/scaler.pkl")

    print("Model and scaler have been trained and saved to the 'models/' directory.")

if __name__ == "__main__":
    train_and_save_model()
