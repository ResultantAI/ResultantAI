#!/usr/bin/env python3
"""
Marketing Audit System
======================
A production-ready tool that generates comprehensive marketing audits using Claude AI.

Usage:
    # Command line mode
    python marketing_audit.py --url https://example.com --industry "SaaS"

    # Make.com webhook mode (reads JSON from stdin)
    echo '{"url": "https://example.com", "industry": "SaaS"}' | python marketing_audit.py
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import anthropic
from bs4 import BeautifulSoup
import time

# Load environment variables
load_dotenv()


# ============================================================================
# CONFIGURATION
# ============================================================================

API_KEY = os.getenv('ANTHROPIC_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME', 'claude-sonnet-4-5-20250929')
MAX_TOKENS = int(os.getenv('MAX_TOKENS', '4096'))
TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))


# ============================================================================
# WEBSITE FETCHING & ANALYSIS
# ============================================================================

def fetch_website_content(url: str) -> Dict[str, Any]:
    """
    Fetch website content and extract key SEO elements.

    Args:
        url: The website URL to analyze

    Returns:
        Dictionary containing page content, title, meta description, etc.
    """
    try:
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract SEO elements
        title = soup.find('title')
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')

        # Get text content (limited for API efficiency)
        text_content = soup.get_text(separator=' ', strip=True)[:8000]

        # Extract links for structure analysis
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        return {
            'url': url,
            'title': title.string if title else None,
            'meta_description': meta_desc.get('content') if meta_desc else None,
            'h1_count': len(h1_tags),
            'h1_tags': [h1.get_text(strip=True) for h1 in h1_tags[:5]],
            'h2_count': len(h2_tags),
            'text_content': text_content,
            'internal_links_count': len([l for l in links if l.startswith('/')]),
            'status_code': response.status_code,
            'load_time_seconds': response.elapsed.total_seconds()
        }

    except requests.RequestException as e:
        return {
            'url': url,
            'error': f'Failed to fetch website: {str(e)}',
            'title': None,
            'meta_description': None,
            'text_content': ''
        }


# ============================================================================
# CLAUDE API INTEGRATION
# ============================================================================

def generate_marketing_audit(website_data: Dict[str, Any], industry: str) -> Dict[str, Any]:
    """
    Use Claude to generate a comprehensive marketing audit.

    Args:
        website_data: Data extracted from the website
        industry: The company's industry/sector

    Returns:
        Structured audit findings as a dictionary
    """
    if not API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

    client = anthropic.Anthropic(api_key=API_KEY)

    # Build the analysis prompt
    prompt = f"""You are a senior marketing consultant conducting a comprehensive marketing audit.

COMPANY INFORMATION:
- Website: {website_data['url']}
- Industry: {industry}

WEBSITE DATA COLLECTED:
- Page Title: {website_data.get('title', 'Not found')}
- Meta Description: {website_data.get('meta_description', 'Not found')}
- H1 Tags ({website_data.get('h1_count', 0)}): {website_data.get('h1_tags', [])}
- Page Load Time: {website_data.get('load_time_seconds', 'N/A')} seconds
- Website Content Sample: {website_data.get('text_content', '')[:4000]}

Please conduct a thorough marketing audit and provide your analysis in the following JSON structure:

{{
  "seo_analysis": {{
    "score": <1-10>,
    "findings": [
      "finding 1",
      "finding 2"
    ],
    "issues": [
      "issue 1",
      "issue 2"
    ]
  }},
  "content_strategy": {{
    "score": <1-10>,
    "messaging_clarity": "assessment",
    "blog_quality": "assessment",
    "cta_effectiveness": "assessment",
    "findings": [
      "finding 1",
      "finding 2"
    ]
  }},
  "social_media_presence": {{
    "score": <1-10>,
    "platforms_detected": [
      "platform 1",
      "platform 2"
    ],
    "engagement_quality": "assessment",
    "recommendations": [
      "recommendation 1",
      "recommendation 2"
    ]
  }},
  "paid_advertising": {{
    "google_ads_potential": {{
      "score": <1-10>,
      "rationale": "explanation",
      "recommended_keywords": ["keyword1", "keyword2"]
    }},
    "social_ads_potential": {{
      "score": <1-10>,
      "platforms": ["Facebook", "LinkedIn"],
      "rationale": "explanation"
    }}
  }},
  "quick_wins": [
    {{
      "title": "Quick Win 1",
      "impact": "high|medium|low",
      "effort": "high|medium|low",
      "description": "detailed description",
      "expected_outcome": "what this will achieve"
    }},
    {{
      "title": "Quick Win 2",
      "impact": "high|medium|low",
      "effort": "high|medium|low",
      "description": "detailed description",
      "expected_outcome": "what this will achieve"
    }},
    {{
      "title": "Quick Win 3",
      "impact": "high|medium|low",
      "effort": "high|medium|low",
      "description": "detailed description",
      "expected_outcome": "what this will achieve"
    }}
  ],
  "overall_assessment": {{
    "overall_score": <1-10>,
    "strengths": ["strength 1", "strength 2"],
    "weaknesses": ["weakness 1", "weakness 2"],
    "priority_actions": ["action 1", "action 2", "action 3"]
  }}
}}

Provide ONLY the JSON output, no additional text. Be specific and actionable in your recommendations."""

    try:
        # Call Claude API
        message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract response text
        response_text = message.content[0].text

        # Parse JSON from response
        # Claude might wrap it in markdown code blocks, so clean that up
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()

        audit_data = json.loads(response_text)
        return audit_data

    except anthropic.APIError as e:
        raise Exception(f"Anthropic API error: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse Claude's response as JSON: {str(e)}\nResponse: {response_text}")


# ============================================================================
# INPUT/OUTPUT HANDLING
# ============================================================================

def parse_arguments() -> Optional[Dict[str, str]]:
    """
    Parse command line arguments.

    Returns:
        Dictionary with 'url' and 'industry', or None if reading from stdin
    """
    parser = argparse.ArgumentParser(
        description='Generate a comprehensive marketing audit using Claude AI'
    )
    parser.add_argument(
        '--url',
        type=str,
        help='Company website URL to audit'
    )
    parser.add_argument(
        '--industry',
        type=str,
        help='Company industry/sector (e.g., "SaaS", "E-commerce", "Healthcare")'
    )

    args = parser.parse_args()

    # If both args provided, return them
    if args.url and args.industry:
        return {'url': args.url, 'industry': args.industry}

    # If no args, check stdin (for Make.com webhook mode)
    if not sys.stdin.isatty():
        return None  # Signal to read from stdin

    # If partial args, show error
    if args.url or args.industry:
        parser.error('Both --url and --industry are required')

    parser.print_help()
    sys.exit(1)


def read_stdin_json() -> Dict[str, str]:
    """
    Read JSON input from stdin (for Make.com webhook integration).

    Returns:
        Dictionary with 'url' and 'industry'
    """
    try:
        data = json.load(sys.stdin)

        if 'url' not in data or 'industry' not in data:
            raise ValueError("JSON must contain 'url' and 'industry' fields")

        return {
            'url': data['url'],
            'industry': data['industry']
        }
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input: {str(e)}")


def format_output(audit_results: Dict[str, Any], url: str, industry: str) -> Dict[str, Any]:
    """
    Format the final output with metadata.

    Args:
        audit_results: The audit findings from Claude
        url: Original URL
        industry: Company industry

    Returns:
        Complete audit report with metadata
    """
    return {
        'audit_metadata': {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'company_url': url,
            'industry': industry,
            'model_used': MODEL_NAME
        },
        'findings': audit_results
    }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function - orchestrates the entire audit process.
    """
    try:
        # Step 1: Get input (CLI args or stdin)
        params = parse_arguments()

        if params is None:
            # Read from stdin (Make.com mode)
            params = read_stdin_json()

        url = params['url']
        industry = params['industry']

        # Step 2: Fetch website content
        print(f"Fetching website content from {url}...", file=sys.stderr)
        website_data = fetch_website_content(url)

        if 'error' in website_data:
            print(f"Warning: {website_data['error']}", file=sys.stderr)
            print("Continuing with limited data...", file=sys.stderr)

        # Step 3: Generate audit using Claude
        print(f"Generating marketing audit for {industry} industry...", file=sys.stderr)
        audit_results = generate_marketing_audit(website_data, industry)

        # Step 4: Format output
        final_output = format_output(audit_results, url, industry)

        # Step 5: Output JSON to stdout
        print(json.dumps(final_output, indent=2))

        print("\n✓ Audit completed successfully!", file=sys.stderr)

    except KeyboardInterrupt:
        print("\n\nAudit cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
