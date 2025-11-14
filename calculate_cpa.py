#!/usr/bin/env python3
"""
Calculate CPA per channel and flag over-threshold spend.
"""

import json
import sys
from datetime import datetime
from ad_spend_data import fetch_spend_data


def calculate_cpa(spend_data, thresholds):
    """
    Args:
        spend_data: List of dicts from fetch_spend_data()
        thresholds: Dict mapping channel -> max CPA (e.g., {'Google': 60, 'Reddit': 45})
    Returns:
        List of dicts with added 'cpa' and 'alert' keys
    """
    results = []
    for row in spend_data:
        cpa = row['spend'] / max(row['leads'], 1)  # Avoid division by zero
        channel = row['channel']
        threshold = thresholds.get(channel, 50)  # Default $50 if channel not in map

        row['cpa'] = round(cpa, 2)
        row['alert'] = 'OVER' if cpa >= threshold else 'UNDER'
        row['threshold'] = threshold
        results.append(row)

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

        # Get source and thresholds from input
        source = input_data.get('source', 'mock')
        thresholds = input_data.get('thresholds', {
            'Google': 60,
            'Reddit': 45,
            'Upwork': 30
        })

        # Fetch spend data
        spend_data = fetch_spend_data(source=source)

        # Calculate CPA with alerts
        results = calculate_cpa(spend_data, thresholds)

        # Identify channels with alerts
        over_threshold = [r for r in results if r['alert'] == 'OVER']
        under_threshold = [r for r in results if r['alert'] == 'UNDER']

        # Calculate summary stats
        total_spend = sum(r['spend'] for r in results)
        total_leads = sum(r['leads'] for r in results)
        overall_cpa = round(total_spend / max(total_leads, 1), 2)

        # Return structured JSON output
        result = {
            'success': True,
            'analysis': results,
            'alerts': {
                'over_threshold_count': len(over_threshold),
                'over_threshold_channels': [r['channel'] for r in over_threshold],
                'under_threshold_count': len(under_threshold),
                'under_threshold_channels': [r['channel'] for r in under_threshold]
            },
            'summary': {
                'total_spend': total_spend,
                'total_leads': total_leads,
                'overall_cpa': overall_cpa,
                'highest_cpa_channel': max(results, key=lambda x: x['cpa'])['channel'],
                'lowest_cpa_channel': min(results, key=lambda x: x['cpa'])['channel']
            },
            'thresholds_used': thresholds,
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
