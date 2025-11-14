"""
Calculate Cost Per Acquisition (CPA) from ad spend data and check against thresholds.
"""

from typing import List, Dict, Any


def calculate_cpa(data: List[Dict[str, Any]], thresholds: Dict[str, float]) -> List[Dict[str, Any]]:
    """
    Calculate CPA for each record and check against channel-specific thresholds.

    Args:
        data: List of dicts with keys: date, channel, spend, leads
        thresholds: Dict mapping channel name to CPA threshold (e.g., {'Google': 60, 'Reddit': 45})

    Returns:
        List of dicts with keys: date, channel, spend, leads, cpa, threshold, alert
        where alert is 'OVER' if CPA > threshold, 'UNDER' if CPA <= threshold
    """
    results = []

    for record in data:
        channel = record['channel']
        spend = float(record['spend'])
        leads = int(record['leads'])

        # Calculate CPA
        if leads > 0:
            cpa = spend / leads
        else:
            cpa = float('inf')  # Infinite CPA if no leads

        # Get threshold for this channel
        threshold = thresholds.get(channel, 0)

        # Determine alert status
        if cpa > threshold:
            alert = 'OVER'
        else:
            alert = 'UNDER'

        # Build result record
        result = {
            'date': record['date'],
            'channel': channel,
            'spend': spend,
            'leads': leads,
            'cpa': round(cpa, 2),
            'threshold': threshold,
            'alert': alert
        }

        results.append(result)

    return results


def get_default_thresholds() -> Dict[str, float]:
    """
    Return default CPA thresholds for each channel.

    Returns:
        Dict mapping channel name to CPA threshold
    """
    return {
        'Google': 60.0,
        'Reddit': 45.0,
        'Upwork': 30.0
    }


def print_cpa_report(results: List[Dict[str, Any]]):
    """
    Print a formatted CPA report showing alerts.

    Args:
        results: Output from calculate_cpa()
    """
    print("\n" + "="*100)
    print("CPA ANALYSIS REPORT")
    print("="*100)

    # Group by channel
    channels = {}
    for record in results:
        channel = record['channel']
        if channel not in channels:
            channels[channel] = []
        channels[channel].append(record)

    # Print each channel's results
    for channel, records in channels.items():
        print(f"\n{channel}:")
        print(f"{'Date':<12} {'Spend':<10} {'Leads':<8} {'CPA':<10} {'Threshold':<12} {'Alert':<8}")
        print("-" * 100)

        # Sort by date (newest first)
        sorted_records = sorted(records, key=lambda x: x['date'], reverse=True)

        for record in sorted_records:
            alert_symbol = "🔴" if record['alert'] == 'OVER' else "🟢"
            print(
                f"{record['date']:<12} "
                f"${record['spend']:<9.2f} "
                f"{record['leads']:<8} "
                f"${record['cpa']:<9.2f} "
                f"${record['threshold']:<11.2f} "
                f"{alert_symbol} {record['alert']:<8}"
            )

    # Summary statistics
    print("\n" + "="*100)
    print("SUMMARY")
    print("="*100)

    total_over = sum(1 for r in results if r['alert'] == 'OVER')
    total_under = sum(1 for r in results if r['alert'] == 'UNDER')

    print(f"Total records: {len(results)}")
    print(f"🔴 Over threshold: {total_over}")
    print(f"🟢 Under threshold: {total_under}")

    if total_over > 0:
        print(f"\n⚠️  {total_over} alert(s) require attention!")


if __name__ == '__main__':
    import sys
    import json
    from fetch_spend_data import fetch_spend_data

    # Fetch spend data
    data = fetch_spend_data()

    # Use default thresholds or load from environment/config
    thresholds = get_default_thresholds()

    print(f"\n📊 Using thresholds: {thresholds}")

    # Calculate CPA
    results = calculate_cpa(data, thresholds)

    # Print report
    print_cpa_report(results)

    # Output JSON for piping to other scripts
    print("\n" + "="*100)
    print("JSON OUTPUT")
    print("="*100)
    print(json.dumps(results, indent=2))
