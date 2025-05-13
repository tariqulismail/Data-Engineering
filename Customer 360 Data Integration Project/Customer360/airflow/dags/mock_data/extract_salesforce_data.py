# /mock_data/extract_salesforce_data.py
from simple_salesforce import Salesforce
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def connect_to_salesforce():
    sf = Salesforce(
        username='nasimbd80-mkkm@force.com',
        password='commando_00',
        security_token='RdqzcXtDUu7NFdDQbVQ8fGYS'
    )
    return sf

def extract_salesforce_contacts():
    sf = connect_to_salesforce()
    
    # Query Salesforce for Contact data
    query = """
    SELECT Id, FirstName, LastName, Email, Phone, Account.Name, 
           CreatedDate, LastModifiedDate
    FROM Contact
    LIMIT 1000
    """
    
    results = sf.query_all(query)
    records = results['records']
    
    # Transform Salesforce records into pandas DataFrame
    contacts = []
    for record in records:
        contact = {
            'SalesforceID': record['Id'],
            'FirstName': record['FirstName'],
            'LastName': record['LastName'],
            'Email': record['Email'],
            'Phone': record['Phone'],
            'AccountName': record['Account']['Name'],
            'CreatedDate': record['CreatedDate'],
            'LastModifiedDate': record['LastModifiedDate']
        }
        contacts.append(contact)
    
    return pd.DataFrame(contacts)

if __name__ == "__main__":
    contacts_df = extract_salesforce_contacts()
    contacts_df.to_csv('salesforce_contacts.csv', index=False)