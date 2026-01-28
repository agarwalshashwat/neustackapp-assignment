import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

def build_model():
    # Load data
    df = pd.read_csv('employee_data.csv')
    
    # Define features and target
    X = df.drop(columns=['employee_id', 'enrolled'])
    y = df['enrolled']
    
    # Preprocessing
    categorical_features = ['gender', 'marital_status', 'employment_type', 'region', 'has_dependents']
    numerical_features = ['age', 'salary', 'tenure_years']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )
    
    # Define the pipeline
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train
    print("Training model...")
    model_pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model_pipeline.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    # Save the model
    joblib.dump(model_pipeline, 'enrollment_model.joblib')
    print("Model saved to enrollment_model.joblib")

if __name__ == "__main__":
    build_model()
