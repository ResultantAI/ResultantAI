"""
Fetch ad spend data from various channels (Google Ads, Reddit Ads, Upwork).
Returns structured data for CPA calculation.
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

# API configuration from environment
GOOGLE_ADS_API_KEY = os.getenv('GOOGLE_ADS_API_KEY', '')
GOOGLE_ADS_CLIENT_ID = os.getenv('GOOGLE_ADS_CLIENT_ID', '')
GOOGLE_ADS_CUSTOMER_ID = os.getenv('GOOGLE_ADS_CUSTOMER_ID', '')

REDDIT_ADS_ACCESS_TOKEN = os.getenv('REDDIT_ADS_ACCESS_TOKEN', '')
REDDIT_ADS_ACCOUNT_ID = os.getenv('REDDIT_ADS_ACCOUNT_ID', '')

UPWORK_API_KEY = os.getenv('UPWORK_API_KEY', '')
UPWORK_API_SECRET = os.getenv('UPWORK_API_SECRET', '')

# Date range configuration
DAYS_BACK = int(os.getenv('FETCH_DAYS_BACK', '7'))


def fetch_google_ads_data() -> List[Dict[str, Any]]:
    """
    Fetch Google Ads spend and conversion data.

    Returns:
        List of dicts with: date, channel, spend, leads
    """
    # TODO: Implement actual Google Ads API integration
    # For now, return mock data for testing

    if not GOOGLE_ADS_API_KEY:
        print("⚠️  GOOGLE_ADS_API_KEY not configured, using mock data")

    # Mock data - replace with actual API calls
    end_date = datetime.now()
    data = []

    for i in range(DAYS_BACK):
        date = (end_date - timedelta(days=i)).strftime('%Y-%m-%d')
        data.append({
            'date': date,
            'channel': 'Google',
            'spend': 500 + (i * 50),  # Mock spend data
            'leads': 8 + i  # Mock leads data
        })

    return data


def fetch_reddit_ads_data() -> List[Dict[str, Any]]:
    """
    Fetch Reddit Ads spend and conversion data.

    Returns:
        List of dicts with: date, channel, spend, leads
    """
    # TODO: Implement actual Reddit Ads API integration

    if not REDDIT_ADS_ACCESS_TOKEN:
        print("⚠️  REDDIT_ADS_ACCESS_TOKEN not configured, using mock data")

    # Mock data - replace with actual API calls
    end_date = datetime.now()
    data = []

    for i in range(DAYS_BACK):
        date = (end_date - timedelta(days=i)).strftime('%Y-%m-%d')
        data.append({
            'date': date,
            'channel': 'Reddit',
            'spend': 300 + (i * 30),  # Mock spend data
            'leads': 7 + i  # Mock leads data
        })

    return data


def fetch_upwork_data() -> List[Dict[str, Any]]:
    """
    Fetch Upwork spend and conversion data (job posts leading to hires).

    Returns:
        List of dicts with: date, channel, spend, leads
    """
    # TODO: Implement actual Upwork API integration

    if not UPWORK_API_KEY:
        print("⚠️  UPWORK_API_KEY not configured, using mock data")

    # Mock data - replace with actual API calls
    end_date = datetime.now()
    data = []

    for i in range(DAYS_BACK):
        date = (end_date - timedelta(days=i)).strftime('%Y-%m-%d')
        data.append({
            'date': date,
            'channel': 'Upwork',
            'spend': 200 + (i * 20),  # Mock spend data
            'leads': 6 + i  # Mock leads data (hires)
        })

    return data


def fetch_spend_data() -> List[Dict[str, Any]]:
    """
    Fetch ad spend data from all configured channels.

    Returns:
        List of dicts with: date, channel, spend, leads
    """
    all_data = []

    print("📊 Fetching ad spend data...")

    # Fetch from each channel
    try:
        google_data = fetch_google_ads_data()
        all_data.extend(google_data)
        print(f"✅ Fetched {len(google_data)} records from Google Ads")
    except Exception as e:
        print(f"❌ Error fetching Google Ads data: {e}")

    try:
        reddit_data = fetch_reddit_ads_data()
        all_data.extend(reddit_data)
        print(f"✅ Fetched {len(reddit_data)} records from Reddit Ads")
    except Exception as e:
        print(f"❌ Error fetching Reddit Ads data: {e}")

    try:
        upwork_data = fetch_upwork_data()
        all_data.extend(upwork_data)
        print(f"✅ Fetched {len(upwork_data)} records from Upwork")
    except Exception as e:
        print(f"❌ Error fetching Upwork data: {e}")

    print(f"📈 Total records fetched: {len(all_data)}")

    return all_data


if __name__ == '__main__':
    # When run directly, fetch and display data
    data = fetch_spend_data()

    # Pretty print the results
    print("\n" + "="*80)
    print("AD SPEND DATA")
    print("="*80)

    # Group by channel for display
    channels = {}
    for record in data:
        channel = record['channel']
        if channel not in channels:
            channels[channel] = []
        channels[channel].append(record)

    for channel, records in channels.items():
        print(f"\n{channel}:")
        print(f"{'Date':<12} {'Spend':<10} {'Leads':<10}")
        print("-" * 32)
        for record in sorted(records, key=lambda x: x['date'], reverse=True):
            print(f"{record['date']:<12} ${record['spend']:<9.2f} {record['leads']:<10}")

    # Output JSON for piping to other scripts
    print("\n" + "="*80)
    print("JSON OUTPUT")
    print("="*80)
    print(json.dumps(data, indent=2))
