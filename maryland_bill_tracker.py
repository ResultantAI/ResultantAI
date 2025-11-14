#!/usr/bin/env python3
"""
Maryland Bill Tracker - AI-Powered Legislative Monitoring
Track Maryland state bills, analyze content, and monitor status changes.

Usage:
    CLI Mode:
        python maryland_bill_tracker.py --bill-number HB123
        python maryland_bill_tracker.py --keyword "education funding" --session 2025
        python maryland_bill_tracker.py --subject healthcare --status introduced

    Automation Mode (stdin):
        echo '{"bill_number": "HB123"}' | python maryland_bill_tracker.py
        echo '{"keyword": "education", "session": "2025"}' | python maryland_bill_tracker.py
"""

import anthropic
import argparse
import json
import os
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "claude-sonnet-4-5-20250929")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 4096))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))

# Maryland General Assembly API/Website
MGA_BASE_URL = "https://mgaleg.maryland.gov"
MGA_API_BASE = f"{MGA_BASE_URL}/mgawebsite/Legislation"


class MarylandBillTracker:
    """Track and analyze Maryland state legislation."""

    def __init__(self):
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def search_bills(self,
                    bill_number: Optional[str] = None,
                    keyword: Optional[str] = None,
                    subject: Optional[str] = None,
                    session: Optional[str] = None,
                    status: Optional[str] = None) -> Dict:
        """
        Search for Maryland bills using various criteria.

        Args:
            bill_number: Specific bill number (e.g., "HB123", "SB456")
            keyword: Search by keyword in title/synopsis
            subject: Subject area (e.g., "healthcare", "education", "taxation")
            session: Legislative session year (e.g., "2025", "2024")
            status: Bill status (e.g., "introduced", "passed", "enacted")

        Returns:
            Dict containing bill information and analysis
        """

        # If session not provided, use current year
        if not session:
            session = str(datetime.now().year)

        # Build search parameters
        search_params = {
            "session": session,
            "bill_number": bill_number,
            "keyword": keyword,
            "subject": subject,
            "status": status
        }

        # Fetch bill data (simulation for demo - in production, use actual MGA API)
        bill_data = self._fetch_bill_data(search_params)

        # Analyze bill with Claude AI
        analysis = self._analyze_bill_with_ai(bill_data, search_params)

        return {
            "search_criteria": search_params,
            "bills_found": bill_data.get("count", 0),
            "bills": bill_data.get("bills", []),
            "ai_analysis": analysis,
            "timestamp": datetime.now().isoformat(),
            "session": session
        }

    def _fetch_bill_data(self, params: Dict) -> Dict:
        """
        Fetch bill data from Maryland General Assembly.

        Note: This is a demo implementation. In production, integrate with
        Maryland's actual LeGIS API or scrape from their website.
        """

        # Demo data for demonstration purposes
        # In production, replace with actual API calls to MGA
        demo_bills = []

        # Simulate bill data based on search criteria
        if params.get("bill_number"):
            demo_bills.append({
                "bill_number": params["bill_number"],
                "title": "Maryland Education Funding and Innovation Act",
                "sponsors": ["Del. John Smith", "Del. Jane Doe"],
                "status": "In Committee - Education and Economic Development",
                "introduced_date": "2025-01-15",
                "synopsis": "Establishes new funding mechanisms for public schools and creates innovation grants for educational technology initiatives. Appropriates $50M for FY2026.",
                "fiscal_note": "Estimated cost: $50M annually",
                "committee": "Education and Economic Development Committee",
                "latest_action": "Referred to committee on 2025-01-15",
                "url": f"{MGA_BASE_URL}/mgawebsite/Legislation/Details/{params['bill_number']}?ys={params['session']}"
            })
        elif params.get("keyword"):
            keyword = params["keyword"].lower()
            if "education" in keyword or "school" in keyword:
                demo_bills.extend([
                    {
                        "bill_number": "HB101",
                        "title": f"Public School {params['keyword'].title()} Enhancement Act",
                        "sponsors": ["Del. Sarah Johnson"],
                        "status": "Passed House, In Senate",
                        "introduced_date": "2025-01-10",
                        "synopsis": f"Legislation addressing {params['keyword']} in Maryland public schools.",
                        "committee": "Senate Education Committee",
                        "latest_action": "Passed House 98-42 on 2025-02-20"
                    },
                    {
                        "bill_number": "SB55",
                        "title": f"Maryland {params['keyword'].title()} Modernization",
                        "sponsors": ["Sen. Michael Brown"],
                        "status": "In Committee",
                        "introduced_date": "2025-01-08",
                        "synopsis": f"Modernizes Maryland's approach to {params['keyword']}.",
                        "committee": "Education Committee"
                    }
                ])
            elif "healthcare" in keyword or "health" in keyword:
                demo_bills.append({
                    "bill_number": "HB205",
                    "title": "Maryland Healthcare Access Expansion",
                    "sponsors": ["Del. Emily Wilson"],
                    "status": "Enacted",
                    "introduced_date": "2025-01-05",
                    "synopsis": "Expands healthcare access for underserved communities.",
                    "enacted_date": "2025-03-15"
                })

        if not demo_bills:
            demo_bills.append({
                "message": "No bills found matching criteria. This is demo data - integrate with actual MGA API for real results.",
                "note": "Maryland General Assembly API/web scraping integration needed for production use."
            })

        return {
            "count": len(demo_bills),
            "bills": demo_bills,
            "source": "Maryland General Assembly (Demo Data)",
            "session": params.get("session", str(datetime.now().year))
        }

    def _analyze_bill_with_ai(self, bill_data: Dict, search_params: Dict) -> Dict:
        """Use Claude AI to analyze bill impact and significance."""

        if not bill_data.get("bills") or bill_data["count"] == 0:
            return {
                "summary": "No bills found to analyze",
                "impact_assessment": None
            }

        # Prepare bill information for AI analysis
        bills_text = json.dumps(bill_data["bills"], indent=2)

        prompt = f"""You are analyzing Maryland state legislation. Provide a comprehensive analysis of the following bill(s):

SEARCH CRITERIA:
{json.dumps(search_params, indent=2)}

BILL DATA:
{bills_text}

Please provide:

1. EXECUTIVE SUMMARY: Brief overview of the bill(s) and their purpose

2. KEY PROVISIONS: Main components and what the legislation does

3. IMPACT ASSESSMENT:
   - Who is affected (citizens, businesses, government)
   - Potential benefits
   - Potential concerns or challenges
   - Fiscal impact if available

4. STATUS & TIMELINE: Current legislative status and likely path forward

5. STAKEHOLDER ANALYSIS: Who supports/opposes and why

6. PRIORITY RATING: Rate importance as High/Medium/Low with justification

7. MONITORING RECOMMENDATIONS: What to watch for as the bill progresses

Provide analysis in structured JSON format."""

        try:
            message = self.client.messages.create(
                model=MODEL_NAME,
                max_tokens=MAX_TOKENS,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Extract AI response
            ai_response = message.content[0].text

            # Try to parse as JSON, fallback to text if not valid JSON
            try:
                analysis = json.loads(ai_response)
            except json.JSONDecodeError:
                analysis = {
                    "analysis": ai_response,
                    "format": "text"
                }

            return analysis

        except Exception as e:
            return {
                "error": f"AI analysis failed: {str(e)}",
                "raw_data": bill_data
            }

    def track_bill(self, bill_number: str, session: Optional[str] = None) -> Dict:
        """
        Track a specific bill and get detailed information.

        Args:
            bill_number: Bill number (e.g., "HB123")
            session: Legislative session year

        Returns:
            Detailed bill information with AI analysis
        """
        return self.search_bills(bill_number=bill_number, session=session)

    def monitor_keywords(self, keywords: List[str], session: Optional[str] = None) -> Dict:
        """
        Monitor multiple keywords and return matching bills.

        Args:
            keywords: List of keywords to monitor
            session: Legislative session year

        Returns:
            Combined results for all keywords
        """
        results = []

        for keyword in keywords:
            result = self.search_bills(keyword=keyword, session=session)
            results.append({
                "keyword": keyword,
                "result": result
            })

        return {
            "keywords_monitored": keywords,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }


def parse_stdin() -> Optional[Dict]:
    """Parse JSON input from stdin for automation workflows."""
    if not sys.stdin.isatty():
        try:
            stdin_data = sys.stdin.read().strip()
            if stdin_data:
                return json.loads(stdin_data)
        except json.JSONDecodeError as e:
            print(json.dumps({
                "error": "Invalid JSON input",
                "details": str(e)
            }), file=sys.stderr)
            sys.exit(1)
    return None


def main():
    """Main entry point for Maryland Bill Tracker."""

    # Check for stdin input first (automation mode)
    stdin_input = parse_stdin()

    if stdin_input:
        # Automation mode - process JSON input
        tracker = MarylandBillTracker()

        bill_number = stdin_input.get("bill_number")
        keyword = stdin_input.get("keyword")
        keywords = stdin_input.get("keywords")
        subject = stdin_input.get("subject")
        session = stdin_input.get("session")
        status = stdin_input.get("status")

        if keywords:
            # Monitor multiple keywords
            result = tracker.monitor_keywords(keywords, session)
        else:
            # Single search
            result = tracker.search_bills(
                bill_number=bill_number,
                keyword=keyword,
                subject=subject,
                session=session,
                status=status
            )

        # Output JSON result
        print(json.dumps(result, indent=2))
        return

    # CLI mode - parse arguments
    parser = argparse.ArgumentParser(
        description="Maryland Bill Tracker - AI-Powered Legislative Monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Track a specific bill:
    python maryland_bill_tracker.py --bill-number HB123

  Search by keyword:
    python maryland_bill_tracker.py --keyword "education funding"

  Search with filters:
    python maryland_bill_tracker.py --subject healthcare --status passed --session 2025

  Automation mode (JSON input):
    echo '{"bill_number": "HB123"}' | python maryland_bill_tracker.py
    echo '{"keywords": ["education", "healthcare"]}' | python maryland_bill_tracker.py
        """
    )

    parser.add_argument("--bill-number", help="Specific bill number (e.g., HB123, SB456)")
    parser.add_argument("--keyword", help="Search by keyword")
    parser.add_argument("--keywords", nargs="+", help="Monitor multiple keywords")
    parser.add_argument("--subject", help="Subject area (e.g., healthcare, education)")
    parser.add_argument("--session", help="Legislative session year (default: current year)")
    parser.add_argument("--status", help="Bill status filter")

    args = parser.parse_args()

    # Validate that at least one search criteria is provided
    if not any([args.bill_number, args.keyword, args.keywords, args.subject]):
        parser.print_help()
        sys.exit(1)

    # Initialize tracker
    tracker = MarylandBillTracker()

    # Execute search
    if args.keywords:
        result = tracker.monitor_keywords(args.keywords, args.session)
    else:
        result = tracker.search_bills(
            bill_number=args.bill_number,
            keyword=args.keyword,
            subject=args.subject,
            session=args.session,
            status=args.status
        )

    # Output result
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
