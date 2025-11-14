#!/usr/bin/env python3
"""
Fetch daily ad spend data from Google Sheets (or mock CSV).
Returns: List of dicts with keys: date, channel, spend, clicks, leads, cpc
"""

import csv
import json
import sys
from datetime import datetime

def fetch_spend_data(source='mock'):
    """
    Mock data for tonight's build. Replace with Google Sheets API later.
    """
    if source == 'mock':
        return [
            {'date': '2025-11-13', 'channel': 'Google', 'spend': 120, 'clicks': 150, 'leads': 3, 'cpc': 0.80},
            {'date': '2025-11-13', 'channel': 'Reddit', 'spend': 80, 'clicks': 200, 'leads': 5, 'cpc': 0.40},
            {'date': '2025-11-13', 'channel': 'Upwork', 'spend': 45, 'clicks': 30, 'leads': 2, 'cpc': 1.50},
        ]
    # TODO: Add Google Sheets API integration here
    else:
        raise NotImplementedError("Google Sheets API not yet implemented")

def main():
    """
    Main entry point for API integration.
    Accepts JSON input via stdin and returns JSON output via stdout.
    """
    try:
        # Read input from stdin (for Make.com/API integration)
        stdin_input = sys.stdin.read().strip()
        input_data = json.loads(stdin_input) if stdin_input else {}

        # Get source from input (default to mock)
        source = input_data.get('source', 'mock')

        # Fetch spend data
        spend_data = fetch_spend_data(source=source)

        # Calculate totals
        total_spend = sum(row['spend'] for row in spend_data)
        total_clicks = sum(row['clicks'] for row in spend_data)
        total_leads = sum(row['leads'] for row in spend_data)
        avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0

        # Return structured JSON output
        result = {
            'success': True,
            'data': spend_data,
            'summary': {
                'total_spend': total_spend,
                'total_clicks': total_clicks,
                'total_leads': total_leads,
                'average_cpc': round(avg_cpc, 2),
                'cost_per_lead': round(total_spend / total_leads, 2) if total_leads > 0 else 0
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
