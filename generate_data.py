import pandas as pd
import numpy as np
import uuid

def generate_employee_data(n=10000):
    np.random.seed(42)
    
    data = {
        'employee_id': [str(uuid.uuid4())[:8] for _ in range(n)],
        'age': np.random.randint(22, 65, size=n),
        'gender': np.random.choice(['Male', 'Female', 'Non-binary'], size=n),
        'marital_status': np.random.choice(['Single', 'Married', 'Divorced'], size=n),
        'salary': np.random.randint(30000, 150000, size=n),
        'employment_type': np.random.choice(['Full-time', 'Part-time', 'Contract'], size=n),
        'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], size=n),
        'has_dependents': np.random.choice(['Yes', 'No'], size=n),
        'tenure_years': np.random.randint(0, 40, size=n)
    }
    
    df = pd.DataFrame(data)
    
    # Synthetic logic for 'enrolled' target
    # People with dependents, higher salary, and more tenure are more likely to enroll
    has_dep_int = (df['has_dependents'] == 'Yes').astype(int)
    logits = (
        (df['age'] - 40) * 0.05 +
        (has_dep_int * 1.5) +
        (df['salary'] / 50000) +
        (df['tenure_years'] * 0.1) -
        4.0
    )
    
    # Sigmoid function
    probs = 1 / (1 + np.exp(-logits))
    df['enrolled'] = (np.random.rand(n) < probs).astype(int)
    
    df.to_csv('employee_data.csv', index=False)
    print(f"Generated {n} rows of synthetic employee data in employee_data.csv")

if __name__ == "__main__":
    generate_employee_data()
