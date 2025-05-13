# /mock_data/extract_ga_data.py
from google.cloud import bigquery
import google.cloud  # (not sufficient on its own)
import pandas as pd
import os

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "personalfinancedata-33d6ed593671.json"

def extract_ga_data():
    client = bigquery.Client()
    
    # Query to get Google Analytics sample data
    query = """
    SELECT
      fullVisitorId,
      visitId,
      date,
      totals.pageviews,
      totals.timeOnSite,
      device.deviceCategory,
      geoNetwork.country,
      trafficSource.source,
      trafficSource.medium
    FROM
      `bigquery-public-data.google_analytics_sample.ga_sessions_*`
    WHERE
      _TABLE_SUFFIX BETWEEN '20170101' AND '20170131'
    LIMIT 5000
    """
    
    df = client.query(query).to_dataframe()
    
    # Generate a simple customer mapping (in a real scenario, you'd match with actual customer IDs)
    df['CustomerID'] = 'CUST' + df['fullVisitorId'].astype(str).str[-6:].str.zfill(6)
    
    return df

if __name__ == "__main__":
    ga_df = extract_ga_data()
    ga_df.to_csv('ga_sessions.csv', index=False)