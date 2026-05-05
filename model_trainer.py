import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_fraud_model(df_transactions):
    """
    Trains an Advanced Random Forest classifier for fraud detection.
    Features: amount, hour, location_change, balance_ratio, txn_frequency
    Returns: trained model, test accuracy
    """
    X = df_transactions[['amount', 'hour', 'location_change', 'balance_ratio', 'txn_frequency']]
    y = df_transactions['is_fraud']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Advanced Model
    model = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    return model, accuracy

def predict_fraud(model, txn):
    """
    Predicts if a new transaction is fraud and returns probability score.
    """
    X_new = pd.DataFrame([{
        'amount': txn['amount'],
        'hour': txn['hour'],
        'location_change': txn['location_change'],
        'balance_ratio': txn['balance_ratio'],
        'txn_frequency': txn['txn_frequency']
    }])
    
    # Get both class prediction and probability of fraud (class 1)
    prediction = model.predict(X_new)[0]
    prob = model.predict_proba(X_new)[0][1] # Probability of being fraud
    
    return prediction, prob
