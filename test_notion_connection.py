#!/usr/bin/env python3
"""
Notion API Connection Test Script
Tests Notion integration setup, validates credentials, and tests database operations.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import requests
import json

# ANSI color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header(text):
    """Print a formatted header."""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{text}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    """Print a success message."""
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    """Print an error message."""
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    """Print a warning message."""
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_info(text):
    """Print an info message."""
    print(f"{BLUE}ℹ {text}{RESET}")

def load_credentials():
    """Load and validate credentials from .env file."""
    print_header("STEP 1: Loading Credentials")

    # Load .env file
    if not os.path.exists('.env'):
        print_error(".env file not found!")
        print_info("Create a .env file with NOTION_API_KEY and NOTION_DATABASE_ID")
        return None, None

    print_success(".env file found")
    load_dotenv()

    # Get credentials
    api_key = os.getenv('NOTION_API_KEY')
    database_id = os.getenv('NOTION_DATABASE_ID')

    if not api_key:
        print_error("NOTION_API_KEY not found in .env file")
        return None, None

    if not database_id:
        print_error("NOTION_DATABASE_ID not found in .env file")
        return None, None

    print_success(f"API Key loaded: {api_key[:20]}...{api_key[-4:]}")
    print_success(f"Database ID loaded: {database_id}")

    return api_key, database_id

def test_database_retrieval(api_key, database_id):
    """Test retrieving database schema (GET request)."""
    print_header("STEP 2: Testing Database Retrieval (GET)")

    url = f"https://api.notion.com/v1/databases/{database_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    print_info(f"Testing GET request to: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            print_success("Database retrieved successfully!")
            data = response.json()

            # Display database info
            print(f"\n{BOLD}Database Information:{RESET}")
            print(f"  Title: {data.get('title', [{}])[0].get('plain_text', 'Untitled')}")
            print(f"  Created: {data.get('created_time', 'Unknown')}")
            print(f"  Last Edited: {data.get('last_edited_time', 'Unknown')}")

            # Display properties (schema)
            print(f"\n{BOLD}Database Properties (Schema):{RESET}")
            properties = data.get('properties', {})
            for prop_name, prop_data in properties.items():
                prop_type = prop_data.get('type', 'unknown')
                print(f"  • {prop_name}: {prop_type}")

                # Show options for select/multi-select
                if prop_type in ['select', 'multi_select']:
                    options = prop_data.get(prop_type, {}).get('options', [])
                    if options:
                        option_names = [opt.get('name') for opt in options]
                        print(f"    Options: {', '.join(option_names)}")

            return True, properties

        elif response.status_code == 401:
            print_error("Authentication failed (401)")
            print_info("Issue: Invalid API key")
            print_info("Fix: Check that your NOTION_API_KEY is correct")
            print_info("Get your API key from: https://www.notion.so/my-integrations")
            return False, None

        elif response.status_code == 403:
            print_error("Access forbidden (403)")
            print_info("Issue: The integration doesn't have access to this database")
            print_info("Fix: Add your integration to the database:")
            print_info("  1. Open your Notion database in browser")
            print_info("  2. Click '...' menu in top right")
            print_info("  3. Select 'Connections' or '+ Add connections'")
            print_info("  4. Find and add your integration")
            return False, None

        elif response.status_code == 404:
            print_error("Database not found (404)")
            print_info("Issue: Invalid database ID")
            print_info("Fix: Check that your NOTION_DATABASE_ID is correct")
            print_info("Get the database ID from the database URL:")
            print_info("  https://www.notion.so/{workspace}/{DATABASE_ID}?v=...")
            return False, None

        else:
            print_error(f"Unexpected error (HTTP {response.status_code})")
            print_info(f"Response: {response.text}")
            return False, None

    except requests.exceptions.Timeout:
        print_error("Request timed out")
        print_info("Check your internet connection")
        return False, None

    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {str(e)}")
        return False, None

def test_page_creation(api_key, database_id, properties_schema):
    """Test creating a test page (POST request)."""
    print_header("STEP 3: Testing Page Creation (POST)")

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")

    # Build properties based on schema
    page_properties = {}

    # Check what properties exist in the schema
    schema_props = {name.lower(): (name, data) for name, data in properties_schema.items()}

    print_info("Building page properties based on database schema...")

    # Project / Client (title)
    title_candidates = ['project / client', 'project/client', 'project', 'client', 'name', 'title']
    title_prop = None
    for candidate in title_candidates:
        if candidate in schema_props:
            title_prop = schema_props[candidate][0]
            break

    # Find the title property from schema
    if not title_prop:
        for name, data in properties_schema.items():
            if data.get('type') == 'title':
                title_prop = name
                break

    if title_prop:
        page_properties[title_prop] = {
            "title": [
                {
                    "text": {
                        "content": "API Connection Test"
                    }
                }
            ]
        }
        print_success(f"Added title property: {title_prop}")
    else:
        print_warning("No title property found in schema")

    # Date
    date_candidates = ['date', 'created date', 'start date']
    for candidate in date_candidates:
        if candidate in schema_props:
            date_prop = schema_props[candidate][0]
            page_properties[date_prop] = {
                "date": {
                    "start": today
                }
            }
            print_success(f"Added date property: {date_prop} = {today}")
            break

    # Block Type (select)
    block_type_candidates = ['block type', 'blocktype', 'type']
    for candidate in block_type_candidates:
        if candidate in schema_props:
            block_type_prop = schema_props[candidate][0]
            page_properties[block_type_prop] = {
                "select": {
                    "name": "Metrics"
                }
            }
            print_success(f"Added select property: {block_type_prop} = Metrics")
            break

    # Status (select)
    if 'status' in schema_props:
        status_prop = schema_props['status'][0]
        # Check if it's a status type or select type
        prop_type = schema_props['status'][1].get('type')
        if prop_type == 'status':
            page_properties[status_prop] = {
                "status": {
                    "name": "Done"
                }
            }
        else:
            page_properties[status_prop] = {
                "select": {
                    "name": "Done"
                }
            }
        print_success(f"Added status property: {status_prop} = Done")

    # Tags (multi-select)
    tags_candidates = ['tags', 'tag', 'labels']
    for candidate in tags_candidates:
        if candidate in schema_props:
            tags_prop = schema_props[candidate][0]
            page_properties[tags_prop] = {
                "multi_select": [
                    {"name": "test"}
                ]
            }
            print_success(f"Added multi-select property: {tags_prop} = [test]")
            break

    # Build the payload
    payload = {
        "parent": {
            "database_id": database_id
        },
        "properties": page_properties
    }

    print_info(f"\nPayload preview:")
    print(json.dumps(payload, indent=2))
    print_info(f"\nSending POST request to: {url}")

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code == 200:
            print_success("Test page created successfully!")
            data = response.json()
            page_url = data.get('url', 'Unknown')
            page_id = data.get('id', 'Unknown')
            print(f"\n{BOLD}Page Details:{RESET}")
            print(f"  Page ID: {page_id}")
            print(f"  Page URL: {page_url}")
            print(f"  Created: {data.get('created_time', 'Unknown')}")
            return True

        elif response.status_code == 400:
            print_error("Bad request (400)")
            error_data = response.json()
            error_code = error_data.get('code', 'unknown')
            error_msg = error_data.get('message', 'Unknown error')

            print_info(f"Error Code: {error_code}")
            print_info(f"Error Message: {error_msg}")

            if 'validation_error' in error_code:
                print_info("\nIssue: Property validation error")
                print_info("Fix: Check that property names and types match your database:")
                print_info("  - Property names are case-sensitive")
                print_info("  - Select options must exist in the database")
                print_info("  - Property types (title, date, select, etc.) must match")

                # Show specific property errors
                if 'properties' in error_msg.lower():
                    print_info("\nDouble-check these properties in your database:")
                    print_info("  • Project / Client (should be title type)")
                    print_info("  • Date (should be date type)")
                    print_info("  • Block Type (should be select type with 'Metrics' option)")
                    print_info("  • Status (should be select/status type with 'Done' option)")
                    print_info("  • Tags (should be multi-select type)")

            return False

        elif response.status_code == 401:
            print_error("Authentication failed (401)")
            print_info("Issue: Invalid API key")
            print_info("Fix: Check that your NOTION_API_KEY is correct")
            return False

        elif response.status_code == 403:
            print_error("Access forbidden (403)")
            print_info("Issue: The integration doesn't have access to this database")
            print_info("Fix: Add your integration to the database (see STEP 2 instructions)")
            return False

        else:
            print_error(f"Unexpected error (HTTP {response.status_code})")
            print_info(f"Response: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print_error("Request timed out")
        print_info("Check your internet connection")
        return False

    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {str(e)}")
        return False

def main():
    """Main test execution."""
    print(f"\n{BOLD}{'='*60}")
    print(f"  NOTION API CONNECTION TEST")
    print(f"{'='*60}{RESET}\n")

    # Step 1: Load credentials
    api_key, database_id = load_credentials()
    if not api_key or not database_id:
        print_error("\n❌ TEST FAILED: Missing credentials")
        sys.exit(1)

    # Step 2: Test database retrieval
    db_success, properties = test_database_retrieval(api_key, database_id)
    if not db_success:
        print_error("\n❌ TEST FAILED: Could not retrieve database")
        sys.exit(1)

    # Step 3: Test page creation
    page_success = test_page_creation(api_key, database_id, properties)

    # Final results
    print_header("TEST RESULTS")

    if db_success and page_success:
        print_success("✅ ALL TESTS PASSED!")
        print_info("Your Notion integration is working correctly.")
        print_info("A test page has been created in your database.")
    elif db_success:
        print_warning("⚠️  PARTIAL SUCCESS")
        print_success("✓ Database retrieval works")
        print_error("✗ Page creation failed")
        print_info("\nYour API key and integration connection are correct,")
        print_info("but there's a mismatch with the database properties.")
        print_info("Review the error messages above for specific fixes.")
    else:
        print_error("❌ TEST FAILED")
        print_info("Review the error messages above for specific fixes.")

    print()

if __name__ == "__main__":
    main()
