"""
Push CPA alerts to Notion Execution_OS as Metrics blocks.
"""

import os
import requests
from datetime import datetime

NOTION_API_KEY = os.getenv('NOTION_API_KEY', 'YOUR_KEY_HERE')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID', 'YOUR_DB_ID_HERE')

def push_to_notion(alert_data):
    """
    Args:
        alert_data: List of dicts from calculate_cpa() with 'alert' == 'OVER'
    """
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }

    for row in alert_data:
        if row['alert'] != 'OVER':
            continue  # Only push over-threshold alerts

        # Parse date for Week/Quarter/Year
        date_obj = datetime.strptime(row['date'], '%Y-%m-%d')
        week = date_obj.isocalendar()[1]
        quarter = (date_obj.month - 1) // 3 + 1
        year = date_obj.year

        payload = {
            'parent': {'database_id': NOTION_DATABASE_ID},
            'properties': {
                'Date': {'date': {'start': row['date']}},
                'Block Type': {'select': {'name': 'Metrics'}},
                'Project / Client': {
                    'title': [{'text': {'content': f"Ad Spend Guardrail — {row['channel']}"}}]
                },
                'Top Priority / Goal': {
                    'rich_text': [{'text': {'content': f"Reduce CPA below ${row['threshold']}"}}]
                },
                'Deliverables / Output': {
                    'rich_text': [{
                        'text': {'content': f"Channel {row['channel']} — Spend ${row['spend']}, Leads {row['leads']}, CPA ${row['cpa']} (threshold ${row['threshold']})"}
                    }]
                },
                'Week': {'number': week},
                'Quarter': {'number': quarter},
                'Year': {'number': year},
                'Tags': {'multi_select': [{'name': 'guardrail'}, {'name': row['channel']}]},
                'Status': {'select': {'name': 'Done'}}
            }
        }

        response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=payload)

        if response.status_code == 200:
            print(f"✅ Pushed {row['channel']} alert to Notion")
        else:
            print(f"❌ Failed to push {row['channel']}: {response.text}")

if __name__ == '__main__':
    from fetch_spend_data import fetch_spend_data
    from calculate_cpa import calculate_cpa

    data = fetch_spend_data()
    thresholds = {'Google': 60, 'Reddit': 45, 'Upwork': 30}
    results = calculate_cpa(data, thresholds)

    # Push only OVER alerts
    push_to_notion(results)
