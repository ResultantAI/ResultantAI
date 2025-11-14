"""
Test Notion API connection and database access.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

def test_connection():
    """Test if we can access the Notion database."""

    if not NOTION_API_KEY:
        print("❌ NOTION_API_KEY not found in environment")
        return False

    if not NOTION_DATABASE_ID:
        print("❌ NOTION_DATABASE_ID not found in environment")
        return False

    print(f"✓ API Key found (starts with: {NOTION_API_KEY[:10]}...)")
    print(f"✓ Database ID: {NOTION_DATABASE_ID}")

    # Test 1: Retrieve database
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

    print("\n🔍 Testing database access...")
    response = requests.get(
        f'https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}',
        headers=headers
    )

    if response.status_code == 200:
        db_data = response.json()
        print(f"✅ Database access successful!")
        print(f"   Title: {db_data.get('title', [{}])[0].get('plain_text', 'Untitled')}")
        print(f"\n📋 Properties found:")
        for prop_name, prop_data in db_data.get('properties', {}).items():
            print(f"   - {prop_name}: {prop_data['type']}")
        return True
    elif response.status_code == 403:
        print("❌ 403 Forbidden - Integration doesn't have access to database")
        print("\n🔧 Fix steps:")
        print("1. Go to your Notion database")
        print("2. Click '...' (three dots) → 'Add connections'")
        print("3. Add your 'ResultantAI Automation' integration")
        return False
    elif response.status_code == 401:
        print("❌ 401 Unauthorized - Invalid API key")
        print("\n🔧 Fix steps:")
        print("1. Go to https://www.notion.so/my-integrations")
        print("2. Copy the 'Internal Integration Token' (starts with 'secret_')")
        print("3. Update your .env file")
        return False
    else:
        print(f"❌ Unexpected error: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🧪 Notion Connection Test")
    print("=" * 60)
    success = test_connection()
    print("\n" + "=" * 60)
    if success:
        print("✅ All tests passed! Ready to push data to Notion.")
    else:
        print("❌ Tests failed. Please fix the issues above.")
    print("=" * 60)
