# /mock_data/generate_transactions.py
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)  # For reproducibility

def generate_transactions(num_customers=1000, min_transactions=1, max_transactions=10):
    transactions = []
    
    for i in range(1, num_customers + 1):
        customer_id = f"CUST{i:06d}"
        
        # Generate 1-10 transactions per customer
        num_transactions = random.randint(min_transactions, max_transactions)
        
        for j in range(num_transactions):
            transaction_id = f"TXN{len(transactions) + 1:08d}"
            
            # Generate transaction dates within the last year
            start_date = datetime.now() - timedelta(days=365)
            transaction_date = fake.date_time_between(start_date=start_date, end_date='now')
            
            # Generate random product and amount
            product_id = f"PROD{random.randint(1, 100):04d}"
            amount = round(random.uniform(10, 500), 2)
            
            # Generate random store location
            store_id = f"STORE{random.randint(1, 20):03d}"
            payment_method = random.choice(['CREDIT', 'DEBIT', 'CASH', 'MOBILE'])
            
            transactions.append({
                'TransactionID': transaction_id,
                'CustomerID': customer_id,
                'TransactionDate': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
                'ProductID': product_id,
                'Amount': amount,
                'StoreID': store_id,
                'PaymentMethod': payment_method
            })
    
    return pd.DataFrame(transactions)

if __name__ == "__main__":
    df = generate_transactions()
    df.to_csv('offline_transactions.csv', index=False)