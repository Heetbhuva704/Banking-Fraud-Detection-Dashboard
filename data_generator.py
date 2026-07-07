import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def get_granular_location(city, mode):
    city_areas = {
        'Mumbai': ['Andheri', 'Bandra', 'Nariman Point', 'Borivali', 'Dadar'],
        'Delhi': ['Connaught Place', 'Saket', 'Karol Bagh', 'Dwarka', 'South Ex'],
        'Bangalore': ['Koramangala', 'Indiranagar', 'Whitefield', 'Jayanagar', 'MG Road'],
        'Hyderabad': ['Banjara Hills', 'HITEC City', 'Kukatpally', 'Secunderabad'],
        'Chennai': ['T Nagar', 'Adyar', 'Velachery', 'Anna Nagar'],
        'Kolkata': ['Salt Lake', 'Park Street', 'New Town', 'Howrah'],
        'Pune': ['Kothrud', 'Hinjewadi', 'Viman Nagar', 'Baner'],
        'Ahmedabad': ['Navrangpura', 'Satellite', 'Bopal', 'Vastrapur']
    }
    area = random.choice(city_areas[city])
    
    if mode == 'ATM':
        return f"{city} ({area} ATM #{random.randint(100,999)})"
    elif mode == 'POS':
        return f"{city} ({area} Merchant)"
    elif mode == 'Branch':
        return f"{city} ({area} Branch)"
    elif mode == 'Locker Vault':
        return f"{city} ({area} Vault Vault-A)"
    else:
        return f"{city} (Digital IP/Online)"

def generate_initial_data(num_customers=800, num_transactions=4000):
    np.random.seed(42)
    random.seed(42)
    
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']
    account_types = ['Savings', 'Current', 'Salary']
    loan_types = ['Home', 'Gold', 'Personal', 'Auto', 'Education', 'None']
    locker_types = ['None', 'None', 'None', 'Small', 'Medium', 'Large']
    
    # 1. Customers
    customers = []
    for i in range(1, num_customers + 1):
        acc_type = random.choice(account_types)
        min_bal = 1000 if acc_type != 'Salary' else 0
            
        bal = round(random.uniform(100, 1900), 2)
        min_bal_violation = 1 if bal < min_bal else 0
            
        customers.append({
            'customer_id': f'CUST{i:04d}',
            'name': f'Customer_{i}',
            'phone_number': f'+91-{random.randint(7000000000, 9999999999)}',
            'age': random.randint(18, 75),
            'city': random.choice(cities),
            'account_type': acc_type,
            'balance': bal,
            'min_balance': min_bal,
            'min_bal_violation': min_bal_violation,
            'credit_score': random.randint(300, 850),
            'kyc_status': random.choice(['Verified', 'Verified', 'Verified', 'Pending']),
            'risk_category': random.choice(['Low', 'Low', 'Medium', 'High']),
            'locker_type': random.choice(locker_types)
        })
    df_customers = pd.DataFrame(customers)
    
    # 2. Banking Products
    products = []
    for i in range(1, num_customers + 1):
        loan = random.choice(loan_types)
        loan_amount = 0
        int_rate = 0
        npa_status = 'Active'
        if loan != 'None':
            loan_amount = round(random.uniform(5000, 150000), 2)
            int_rate = random.uniform(7.5, 14.5)
            if random.random() < 0.05: npa_status = 'NPA (Default)'
            
        fd_amt = round(random.uniform(5000, 50000), 2) if random.random() > 0.4 else 0
        rd_amt = round(random.uniform(100, 1000), 2) if random.random() > 0.6 else 0
            
        products.append({
            'customer_id': f'CUST{i:04d}',
            'loan_type': loan,
            'loan_amount': loan_amount,
            'interest_rate': round(int_rate, 2),
            'npa_status': npa_status,
            'fd_amount': fd_amt,
            'rd_amount': rd_amt,
            'total_interest_earned': round((fd_amt * 0.07) + (rd_amt * 0.05), 2)
        })
    df_products = pd.DataFrame(products)
    
    # 3. Transactions
    transactions = []
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)
    
    for i in range(1, num_transactions + 1):
        cust = random.choice(customers)
        cust_id = cust['customer_id']
        cust_city = cust['city']
        cust_balance = cust['balance']
        
        tx_time = start_time + timedelta(seconds=random.randint(0, int((end_time - start_time).total_seconds())))
        amount = round(random.uniform(10, 500), 2)
        location_city = cust_city if random.random() > 0.15 else random.choice(cities)
        txn_frequency = random.randint(1, 5)
        
        category = random.choices(
            ['Fund Transfer', 'FD Operation', 'Locker Access', 'Loan EMI', 'RD Deposit'], 
            weights=[70, 10, 5, 10, 5]
        )[0]
        
        is_fraud = 0
        pattern_alert = "None"
        
        if category == 'Fund Transfer':
            tx_mode = random.choice(['ATM', 'Online', 'UPI', 'POS'])
            tx_type = random.choice(['Credit', 'Debit'])
            if random.random() < 0.05:
                is_fraud = 1
                fraud_type = random.choice(['high_amount', 'odd_hour', 'location_mismatch', 'high_freq'])
                if fraud_type == 'high_amount':
                    amount = round(random.uniform(2000, 10000), 2)
                    pattern_alert = f"Unusually high {tx_mode} transfer"
                elif fraud_type == 'odd_hour':
                    tx_time = tx_time.replace(hour=random.randint(1, 4))
                    pattern_alert = "Activity during unusual late hours"
                elif fraud_type == 'location_mismatch':
                    location_city = random.choice([c for c in cities if c != cust_city])
                    pattern_alert = f"Sudden location jump to {location_city}"
                elif fraud_type == 'high_freq':
                    txn_frequency = random.randint(10, 25)
                    pattern_alert = "Multiple rapid transactions in 5 mins"
                    
        elif category == 'FD Operation':
            tx_mode = 'Online'
            tx_type = random.choice(['FD Creation', 'FD Premature Liquidation'])
            amount = round(random.uniform(1000, 20000), 2)
            if tx_type == 'FD Premature Liquidation' and random.random() < 0.1:
                is_fraud = 1
                pattern_alert = "Suspicious massive FD liquidation to unverified payee"
                
        elif category == 'Locker Access':
            tx_mode = 'Locker Vault'
            tx_type = 'Physical Access'
            amount = 0
            if random.random() < 0.08:
                is_fraud = 1
                tx_time = tx_time.replace(hour=random.choice([22, 23, 0, 1, 2]))
                pattern_alert = "Vault access attempted outside banking hours"
                
        elif category == 'Loan EMI':
            tx_mode = 'Auto-Debit'
            tx_type = 'Debit'
            amount = round(random.uniform(100, 500), 2)
            if random.random() < 0.02:
                is_fraud = 1
                pattern_alert = "Multiple failed EMI bounce attempts"
                
        elif category == 'RD Deposit':
            tx_mode = 'Auto-Debit'
            tx_type = 'Debit'
            amount = round(random.uniform(50, 200), 2)
            
        hour = tx_time.hour
        day_of_week = tx_time.strftime('%A')
        location_change = 1 if location_city != cust_city else 0
        balance_ratio = round(amount / (cust_balance + 1), 4)
        
        exact_location = get_granular_location(location_city, tx_mode)
        
        transactions.append({
            'transaction_id': f'TXN{i:06d}',
            'customer_id': cust_id,
            'category': category,
            'amount': amount,
            'type': tx_type,
            'mode': tx_mode,
            'timestamp': tx_time,
            'location': exact_location,
            'is_fraud': is_fraud,
            'hour': hour,
            'day_of_week': day_of_week,
            'location_change': location_change,
            'txn_frequency': txn_frequency,
            'balance_ratio': balance_ratio,
            'pattern_alert': pattern_alert
        })
        
    df_transactions = pd.DataFrame(transactions).sort_values('timestamp').reset_index(drop=True)
    
    # Generate Customer Care Tickets
    tickets = []
    issues = [
        "Card stuck in ATM", "Forgot UPI PIN", "Locker fee deduction query", 
        "Suspicious transaction alert received", "FD liquidation failed", 
        "Address update request", "App crashing on login"
    ]
    for _ in range(50):
        cust = random.choice(customers)
        tickets.append({
            'ticket_id': f"TCK{random.randint(1000, 9999)}",
            'customer_id': cust['customer_id'],
            'issue': random.choice(issues),
            'status': random.choice(['Open', 'In Progress', 'Resolved']),
            'priority': random.choice(['High', 'Medium', 'Low'])
        })
    df_tickets = pd.DataFrame(tickets)
    
    return df_customers, df_products, df_transactions, df_tickets

def generate_live_transaction(df_customers, df_transactions):
    cust = df_customers.sample(1).iloc[0]
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']
    
    tx_time = datetime.now()
    amount = round(random.uniform(10, 500), 2)
    location_city = cust['city'] if random.random() > 0.15 else random.choice(cities)
    txn_frequency = random.randint(1, 4)
    
    category = random.choices(
        ['Fund Transfer', 'FD Operation', 'Locker Access', 'Loan EMI', 'RD Deposit'], 
        weights=[50, 15, 15, 10, 10]
    )[0]
    
    is_fraud = 0
    pattern_alert = "None"
    
    if category == 'Fund Transfer':
        tx_mode = random.choice(['ATM', 'Online', 'UPI', 'POS'])
        tx_type = random.choice(['Credit', 'Debit'])
        if random.random() < 0.15:
            is_fraud = 1
            fraud_type = random.choice(['high_amount', 'odd_hour', 'location_mismatch', 'high_freq'])
            if fraud_type == 'high_amount':
                amount = round(random.uniform(2000, 10000), 2)
                pattern_alert = f"Unusually high {tx_mode} transfer"
            elif fraud_type == 'odd_hour':
                tx_time = tx_time.replace(hour=random.randint(1, 4))
                pattern_alert = "Activity during unusual late hours"
            elif fraud_type == 'location_mismatch':
                location_city = random.choice([c for c in cities if c != cust['city']])
                pattern_alert = f"Sudden location jump to {location_city}"
            elif fraud_type == 'high_freq':
                txn_frequency = random.randint(10, 30)
                pattern_alert = "Multiple rapid transactions in 5 mins"
                
    elif category == 'FD Operation':
        tx_mode = 'Online'
        tx_type = random.choice(['FD Creation', 'FD Premature Liquidation'])
        amount = round(random.uniform(1000, 20000), 2)
        if tx_type == 'FD Premature Liquidation' and random.random() < 0.4:
            is_fraud = 1
            pattern_alert = "Suspicious massive FD liquidation to unverified payee"
            
    elif category == 'Locker Access':
        tx_mode = 'Locker Vault'
        tx_type = 'Physical Access'
        amount = 0
        if random.random() < 0.4:
            is_fraud = 1
            tx_time = tx_time.replace(hour=random.choice([22, 23, 0, 1, 2]))
            pattern_alert = "Vault access attempted outside banking hours"
            
    elif category == 'Loan EMI':
        tx_mode = 'Auto-Debit'
        tx_type = 'Debit'
        amount = round(random.uniform(100, 500), 2)
        if random.random() < 0.1:
            is_fraud = 1
            pattern_alert = "Multiple failed EMI bounce attempts detected"
            
    elif category == 'RD Deposit':
        tx_mode = 'Auto-Debit'
        tx_type = 'Debit'
        amount = round(random.uniform(50, 200), 2)
        
    hour = tx_time.hour
    day_of_week = tx_time.strftime('%A')
    location_change = 1 if location_city != cust['city'] else 0
    balance_ratio = round(amount / (cust['balance'] + 1), 4)
    
    exact_location = get_granular_location(location_city, tx_mode)
    
    new_txn = {
        'transaction_id': f"TXN_{datetime.now().strftime('%H%M%S%f')}_{random.randint(100,999)}",
        'customer_id': cust['customer_id'],
        'category': category,
        'amount': amount,
        'type': tx_type,
        'mode': tx_mode,
        'timestamp': tx_time,
        'location': exact_location,
        'is_fraud': is_fraud, 
        'hour': hour,
        'day_of_week': day_of_week,
        'location_change': location_change,
        'txn_frequency': txn_frequency,
        'balance_ratio': balance_ratio,
        'pattern_alert': pattern_alert
    }
    return new_txn
