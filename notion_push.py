#!/usr/bin/env python3
"""
Push CPA alerts to Notion Execution_OS as Metrics blocks.
"""

import os
import json
import sys
import requests
from datetime import datetime
from ad_spend_data import fetch_spend_data
from calculate_cpa import calculate_cpa


NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')


def push_to_notion(alert_data):
    """
    Args:
        alert_data: List of dicts from calculate_cpa() with 'alert' == 'OVER'
    Returns:
        Dict with success status and results
    """
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }

    results = {
        'pushed': [],
        'skipped': [],
        'failed': []
    }

    for row in alert_data:
        if row['alert'] != 'OVER':
            results['skipped'].append({
                'channel': row['channel'],
                'reason': 'Under threshold',
                'cpa': row['cpa'],
                'threshold': row['threshold']
            })
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

        try:
            response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=payload)

            if response.status_code == 200:
                results['pushed'].append({
                    'channel': row['channel'],
                    'cpa': row['cpa'],
                    'threshold': row['threshold'],
                    'notion_page_id': response.json().get('id')
                })
            else:
                results['failed'].append({
                    'channel': row['channel'],
                    'error': response.text,
                    'status_code': response.status_code
                })
        except Exception as e:
            results['failed'].append({
                'channel': row['channel'],
                'error': str(e),
                'error_type': type(e).__name__
            })

    return results


def main():
    """
    Main entry point for API integration.
    Accepts JSON input via stdin and returns JSON output via stdout.
    """
    try:
        # Read input from stdin (for Make.com/API integration)
        stdin_input = sys.stdin.read().strip()
        input_data = json.loads(stdin_input) if stdin_input else {}

        # Get parameters from input
        source = input_data.get('source', 'mock')
        thresholds = input_data.get('thresholds', {
            'Google': 60,
            'Reddit': 45,
            'Upwork': 30
        })

        # Override Notion credentials if provided
        notion_api_key = input_data.get('notion_api_key', NOTION_API_KEY)
        notion_db_id = input_data.get('notion_database_id', NOTION_DATABASE_ID)

        # Temporarily set environment variables for this run
        if notion_api_key:
            os.environ['NOTION_API_KEY'] = notion_api_key
        if notion_db_id:
            os.environ['NOTION_DATABASE_ID'] = notion_db_id

        # Fetch spend data
        spend_data = fetch_spend_data(source=source)

        # Calculate CPA with alerts
        cpa_results = calculate_cpa(spend_data, thresholds)

        # Push to Notion
        notion_results = push_to_notion(cpa_results)

        # Return structured JSON output
        result = {
            'success': True,
            'notion_push': notion_results,
            'summary': {
                'total_channels': len(cpa_results),
                'alerts_pushed': len(notion_results['pushed']),
                'alerts_skipped': len(notion_results['skipped']),
                'alerts_failed': len(notion_results['failed'])
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }

        print(json.dumps(result, indent=2))
        return 0

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        print(json.dumps(error_result, indent=2))
        return 1


if __name__ == '__main__':
    sys.exit(main())
