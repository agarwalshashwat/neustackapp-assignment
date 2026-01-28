# ML Report: Predictive Insurance Enrollment

## 📊 Data Observations
The synthetic dataset `employee_data.csv` contains 10,000 records of employee demographics and employment details.
- **Features**: Age, Gender, Marital Status, Salary, Employment Type, Region, Dependents, and Tenure.
- **Target**: `enrolled` (Binary classification: 1 for Yes, 0 for No).
- **Correlation**: During development, we observed that `salary`, `has_dependents`, and `tenure_years` were the most significant predictors of insurance enrollment in our synthetic logic.

## 🏗️ Model Choices & Rationale
We chose a **Random Forest Classifier** for this pilot:
1. **Handle Categorical Data**: It naturally handles high-cardinality categorical features (Region, Employment Type, Gender) without needing complex feature engineering beyond one-hot encoding.
2. **Non-linear Relationships**: Enrollment behavior often involves non-linear interactions (e.g., middle-aged parents with high salaries are significantly more likely to enroll than young singles with high salaries).
3. **Robustness**: It's less prone to overfitting than a single decision tree and provides `feature_importances` for business insights.

## 🧪 Evaluation Results
The model was evaluated using an 80/20 train-test split.
- **Accuracy**: ~73.6%
- **F1-Score (Enrolled)**: ~0.79
- **Insights**: The model shows good precision and recall for the positive class, ensuring we correctly identify potential enrollees for marketing targetting.

## 🚀 Key Takeaways & Next Steps
- **Takeaway**: Demographic data alone provides a strong baseline for enrollment prediction.
- **What's Next**:
    - **Hyperparameter Tuning**: Use GridSearch or RandomSearch to optimize `n_estimators` and `max_depth`.
    - **Feature Engineering**: Create interaction terms between `salary` and `has_dependents`.
    - **SHAP values**: Implement SHAP to explain exactly *why* a specific employee was predicted to enroll.
    - **Monitoring**: Integration with MLflow to track model versioning and performance drift over time.
