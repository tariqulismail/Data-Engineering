# /mock_data/generate_crm_data.py
import os
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)  # For reproducibility

def generate_crm_data(num_records=1000):
    customers = []
    
    for i in range(1, num_records + 1):
        customer_id = f"CUST{i:06d}"
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone = fake.phone_number()
        
        # Generate signup dates within the last 3 years
        start_date = datetime.now() - timedelta(days=3*365)
        signup_date = fake.date_time_between(start_date=start_date, end_date='now')
        
        customers.append({
            'CustomerID': customer_id,
            'FirstName': first_name,
            'LastName': last_name,
            'Email': email,
            'Phone': phone,
            'SignupDate': signup_date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return pd.DataFrame(customers)

if __name__ == "__main__":
    df = generate_crm_data()
    output_path = f'/opt/airflow/crm_data.csv'
    df.to_csv(output_path, index=False)
   
    

# if __name__ == "__main__":
#     output_dir = './output_data'
#     os.makedirs(output_dir, exist_ok=True)  # ✅ Create the directory if it doesn't exist
#     output_file = os.path.join(output_dir, 'crm_data.csv')
#     df = generate_crm_data()
#     df.to_csv(output_file, index=False)
#     print(f"✅ File saved to {output_file}")


    # SQL script to load into MySQL
    with open('create_crm_table.sql', 'w') as f:
        f.write("""
CREATE TABLE IF NOT EXISTS crm_customers (
    CustomerID VARCHAR(10) PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    Phone VARCHAR(20),
    SignupDate DATETIME
);
        """)