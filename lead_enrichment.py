#!/usr/bin/env python3
"""
Lead Enrichment & Scoring System
=================================
A production-ready tool that enriches company data and scores leads against ICP criteria.

Usage:
    # Command line mode
    python lead_enrichment.py --domain stripe.com

    # Make.com webhook mode (reads JSON from stdin)
    echo '{"domain": "stripe.com"}' | python lead_enrichment.py

    # With custom company name
    python lead_enrichment.py --domain example.com --company "Example Corp"
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
import anthropic
from bs4 import BeautifulSoup
import re

# Load environment variables
load_dotenv()


# ============================================================================
# CONFIGURATION
# ============================================================================

API_KEY = os.getenv('ANTHROPIC_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME', 'claude-sonnet-4-5-20250929')
MAX_TOKENS = int(os.getenv('MAX_TOKENS', '4096'))
TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))
ICP_CONFIG_PATH = os.getenv('ICP_CONFIG_PATH', 'icp_config.json')


# ============================================================================
# ICP CONFIGURATION LOADING
# ============================================================================

def load_icp_config(config_path: str = ICP_CONFIG_PATH) -> Dict[str, Any]:
    """
    Load ICP (Ideal Customer Profile) configuration from JSON file.

    Args:
        config_path: Path to ICP configuration file

    Returns:
        Dictionary containing ICP criteria and scoring weights
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Warning: ICP config file not found at {config_path}, using defaults", file=sys.stderr)
        return get_default_icp_config()
    except json.JSONDecodeError as e:
        print(f"Warning: Invalid JSON in ICP config: {e}, using defaults", file=sys.stderr)
        return get_default_icp_config()


def get_default_icp_config() -> Dict[str, Any]:
    """
    Return default ICP configuration if config file is not found.

    Returns:
        Default ICP configuration dictionary
    """
    return {
        "icp_criteria": {
            "company_size": {
                "weight": 20,
                "ideal_range": [50, 500],
                "description": "Employee count between 50-500 (mid-market focus)"
            },
            "industry": {
                "weight": 15,
                "ideal_industries": ["SaaS", "FinTech", "E-commerce", "Technology", "Software"],
                "description": "Target industries with high digital maturity"
            },
            "funding_stage": {
                "weight": 15,
                "ideal_stages": ["Series A", "Series B", "Series C", "Growth"],
                "description": "Funded companies with growth trajectory"
            },
            "tech_stack": {
                "weight": 20,
                "ideal_technologies": ["React", "AWS", "Stripe", "Salesforce", "HubSpot", "Node.js", "Python"],
                "description": "Modern tech stack indicating technical sophistication"
            },
            "growth_signals": {
                "weight": 15,
                "indicators": ["hiring", "expanding", "recent_funding", "press_coverage"],
                "description": "Active growth signals"
            },
            "market_presence": {
                "weight": 15,
                "indicators": ["strong_website", "social_presence", "content_marketing", "seo_optimized"],
                "description": "Professional market presence and brand maturity"
            }
        },
        "scoring_thresholds": {
            "hot_lead": 80,
            "warm_lead": 60,
            "cold_lead": 40,
            "poor_fit": 0
        }
    }


# ============================================================================
# COMPANY DATA EXTRACTION
# ============================================================================

def fetch_company_data(domain: str, company_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch company website and extract basic information.

    Args:
        domain: Company domain (e.g., 'stripe.com')
        company_name: Optional company name if known

    Returns:
        Dictionary containing scraped company data
    """
    try:
        # Ensure domain has protocol
        if not domain.startswith(('http://', 'https://')):
            url = 'https://' + domain
        else:
            url = domain
            # Extract domain from URL for cleaner data
            domain = url.split('://')[1].split('/')[0]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract basic SEO and content data
        title = soup.find('title')
        meta_desc = soup.find('meta', attrs={'name': 'description'})

        # Get page text for analysis
        text_content = soup.get_text(separator=' ', strip=True)[:10000]

        # Try to detect technologies from page source
        page_source = str(soup)[:20000]
        detected_tech = detect_technologies(page_source)

        # Look for social links
        social_links = extract_social_links(soup)

        # Extract company name from title if not provided
        if not company_name and title:
            company_name = extract_company_name(title.string)

        return {
            'domain': domain,
            'company_name': company_name,
            'url': url,
            'title': title.string if title else None,
            'meta_description': meta_desc.get('content') if meta_desc else None,
            'text_content': text_content,
            'detected_technologies': detected_tech,
            'social_links': social_links,
            'status_code': response.status_code,
            'has_https': url.startswith('https://'),
            'fetch_timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }

    except requests.RequestException as e:
        return {
            'domain': domain,
            'company_name': company_name,
            'error': f'Failed to fetch website: {str(e)}',
            'text_content': ''
        }


def detect_technologies(page_source: str) -> List[str]:
    """
    Detect technologies used based on page source analysis.

    Args:
        page_source: HTML source code

    Returns:
        List of detected technologies
    """
    tech_patterns = {
        'React': r'react',
        'Vue.js': r'vue',
        'Angular': r'angular',
        'WordPress': r'wp-content|wordpress',
        'Shopify': r'shopify',
        'Stripe': r'stripe',
        'Google Analytics': r'google-analytics|gtag',
        'HubSpot': r'hubspot',
        'Salesforce': r'salesforce',
        'Intercom': r'intercom',
        'AWS': r'amazonaws',
        'Cloudflare': r'cloudflare',
        'Node.js': r'node\.js',
        'Next.js': r'next\.js|__next'
    }

    detected = []
    page_lower = page_source.lower()

    for tech, pattern in tech_patterns.items():
        if re.search(pattern, page_lower, re.IGNORECASE):
            detected.append(tech)

    return detected


def extract_social_links(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Extract social media links from page.

    Args:
        soup: BeautifulSoup parsed HTML

    Returns:
        Dictionary of social platform: URL
    """
    social_links = {}
    social_patterns = {
        'linkedin': r'linkedin\.com',
        'twitter': r'twitter\.com|x\.com',
        'facebook': r'facebook\.com',
        'instagram': r'instagram\.com',
        'youtube': r'youtube\.com',
        'github': r'github\.com'
    }

    links = soup.find_all('a', href=True)
    for link in links:
        href = link.get('href', '')
        for platform, pattern in social_patterns.items():
            if re.search(pattern, href, re.IGNORECASE) and platform not in social_links:
                social_links[platform] = href

    return social_links


def extract_company_name(title: str) -> str:
    """
    Extract company name from page title.

    Args:
        title: Page title string

    Returns:
        Extracted company name
    """
    # Remove common suffixes
    name = re.split(r'\s*[\|\-–:]\s*', title)[0].strip()
    # Remove common words
    name = re.sub(r'\s+(home|welcome|official|website)$', '', name, flags=re.IGNORECASE)
    return name.strip()


# ============================================================================
# AI-POWERED ENRICHMENT
# ============================================================================

def enrich_company_data(company_data: Dict[str, Any], icp_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Use Claude to enrich company data with additional insights.

    Args:
        company_data: Basic company data from web scraping
        icp_config: ICP configuration for context

    Returns:
        Enriched company data dictionary
    """
    if not API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

    client = anthropic.Anthropic(api_key=API_KEY)

    # Build enrichment prompt
    prompt = f"""You are a B2B sales intelligence analyst enriching company data for lead qualification.

COMPANY INFORMATION:
- Domain: {company_data.get('domain', 'Unknown')}
- Company Name: {company_data.get('company_name', 'Unknown')}
- Website Title: {company_data.get('title', 'Not found')}
- Meta Description: {company_data.get('meta_description', 'Not found')}
- Detected Technologies: {company_data.get('detected_technologies', [])}
- Social Presence: {list(company_data.get('social_links', {}).keys())}
- Website Content Sample: {company_data.get('text_content', '')[:5000]}

Based on the available information, provide a comprehensive company enrichment analysis in the following JSON structure:

{{
  "company_profile": {{
    "name": "official company name",
    "industry": "primary industry (e.g., SaaS, FinTech, E-commerce)",
    "business_model": "B2B/B2C/Marketplace/etc",
    "description": "2-3 sentence company description",
    "headquarters_location": "city, country (if detectable from content)",
    "website_quality": "excellent|good|average|poor"
  }},
  "company_size": {{
    "estimated_employees": <number or null>,
    "size_category": "enterprise|mid-market|small|startup",
    "confidence": "high|medium|low",
    "reasoning": "brief explanation of estimate"
  }},
  "funding_and_growth": {{
    "funding_stage": "Bootstrap|Seed|Series A|Series B|Series C|Growth|Public|Unknown",
    "growth_indicators": ["indicator1", "indicator2"],
    "is_hiring": true/false,
    "expansion_signals": ["signal1", "signal2"]
  }},
  "technology_stack": {{
    "confirmed_technologies": ["tech1", "tech2"],
    "likely_technologies": ["tech3", "tech4"],
    "technical_sophistication": "high|medium|low",
    "infrastructure": "cloud|hybrid|on-premise|unknown"
  }},
  "market_presence": {{
    "brand_maturity": "established|growing|emerging|unknown",
    "content_marketing": true/false,
    "seo_quality": "excellent|good|average|poor",
    "social_media_activity": "active|moderate|minimal|none",
    "thought_leadership": true/false
  }},
  "business_intelligence": {{
    "target_customers": "description of their customers",
    "value_proposition": "their core value prop",
    "competitive_positioning": "assessment",
    "revenue_model": "subscription|transaction|advertising|service|product|mixed|unknown"
  }},
  "contact_indicators": {{
    "has_contact_page": true/false,
    "has_demo_cta": true/false,
    "has_pricing_page": true/false,
    "sales_readiness": "high|medium|low"
  }}
}}

Provide ONLY the JSON output, no additional text. Be specific and realistic in your assessments. If information is not available, use "unknown" or null rather than guessing."""

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
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()

        enrichment_data = json.loads(response_text)
        return enrichment_data

    except anthropic.APIError as e:
        raise Exception(f"Anthropic API error: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse Claude's response as JSON: {str(e)}")


# ============================================================================
# LEAD SCORING ENGINE
# ============================================================================

def score_lead(enriched_data: Dict[str, Any], icp_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Score lead based on ICP fit criteria.

    Args:
        enriched_data: Enriched company data
        icp_config: ICP configuration with criteria and weights

    Returns:
        Scoring results with breakdown
    """
    criteria = icp_config['icp_criteria']
    thresholds = icp_config['scoring_thresholds']

    scores = {}
    total_score = 0
    max_possible = 100

    # Score company size
    size_score = score_company_size(enriched_data, criteria['company_size'])
    scores['company_size'] = size_score
    total_score += size_score['weighted_score']

    # Score industry
    industry_score = score_industry(enriched_data, criteria['industry'])
    scores['industry'] = industry_score
    total_score += industry_score['weighted_score']

    # Score funding stage
    funding_score = score_funding(enriched_data, criteria['funding_stage'])
    scores['funding_stage'] = funding_score
    total_score += funding_score['weighted_score']

    # Score tech stack
    tech_score = score_tech_stack(enriched_data, criteria['tech_stack'])
    scores['tech_stack'] = tech_score
    total_score += tech_score['weighted_score']

    # Score growth signals
    growth_score = score_growth_signals(enriched_data, criteria['growth_signals'])
    scores['growth_signals'] = growth_score
    total_score += growth_score['weighted_score']

    # Score market presence
    market_score = score_market_presence(enriched_data, criteria['market_presence'])
    scores['market_presence'] = market_score
    total_score += market_score['weighted_score']

    # Determine lead category
    if total_score >= thresholds['hot_lead']:
        category = 'hot_lead'
    elif total_score >= thresholds['warm_lead']:
        category = 'warm_lead'
    elif total_score >= thresholds['cold_lead']:
        category = 'cold_lead'
    else:
        category = 'poor_fit'

    return {
        'total_score': round(total_score, 1),
        'max_score': max_possible,
        'category': category,
        'category_thresholds': thresholds,
        'score_breakdown': scores,
        'recommendation': get_recommendation(category, total_score)
    }


def score_company_size(data: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Score based on company size criteria."""
    weight = criteria['weight']
    ideal_range = criteria['ideal_range']

    size_data = data.get('company_size', {})
    estimated_employees = size_data.get('estimated_employees')

    if estimated_employees is None:
        # Fallback to size category
        size_category = size_data.get('size_category', 'unknown')
        if size_category == 'mid-market':
            raw_score = 90
        elif size_category == 'small':
            raw_score = 70
        elif size_category == 'enterprise':
            raw_score = 60
        elif size_category == 'startup':
            raw_score = 50
        else:
            raw_score = 40
    else:
        # Score based on employee count
        if ideal_range[0] <= estimated_employees <= ideal_range[1]:
            raw_score = 100
        elif estimated_employees < ideal_range[0]:
            raw_score = max(40, 100 - (ideal_range[0] - estimated_employees) * 2)
        else:
            raw_score = max(40, 100 - (estimated_employees - ideal_range[1]) * 0.2)

    return {
        'raw_score': round(raw_score, 1),
        'weighted_score': round((raw_score * weight) / 100, 1),
        'weight': weight,
        'value': estimated_employees or size_data.get('size_category', 'unknown'),
        'reasoning': f"Company size: {estimated_employees or size_data.get('size_category', 'unknown')}"
    }


def score_industry(data: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Score based on industry match."""
    weight = criteria['weight']
    ideal_industries = [ind.lower() for ind in criteria['ideal_industries']]

    industry = data.get('company_profile', {}).get('industry', 'unknown').lower()

    if any(ideal in industry for ideal in ideal_industries):
        raw_score = 100
    elif 'tech' in industry or 'software' in industry or 'digital' in industry:
        raw_score = 70
    else:
        raw_score = 40

    return {
        'raw_score': round(raw_score, 1),
        'weighted_score': round((raw_score * weight) / 100, 1),
        'weight': weight,
        'value': data.get('company_profile', {}).get('industry', 'unknown'),
        'reasoning': f"Industry: {data.get('company_profile', {}).get('industry', 'unknown')}"
    }


def score_funding(data: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Score based on funding stage."""
    weight = criteria['weight']
    ideal_stages = [stage.lower() for stage in criteria['ideal_stages']]

    funding_stage = data.get('funding_and_growth', {}).get('funding_stage', 'unknown').lower()

    if any(stage in funding_stage for stage in ideal_stages):
        raw_score = 100
    elif 'bootstrap' in funding_stage or 'seed' in funding_stage:
        raw_score = 60
    elif 'public' in funding_stage:
        raw_score = 70
    else:
        raw_score = 50

    return {
        'raw_score': round(raw_score, 1),
        'weighted_score': round((raw_score * weight) / 100, 1),
        'weight': weight,
        'value': data.get('funding_and_growth', {}).get('funding_stage', 'unknown'),
        'reasoning': f"Funding: {data.get('funding_and_growth', {}).get('funding_stage', 'unknown')}"
    }


def score_tech_stack(data: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Score based on technology stack match."""
    weight = criteria['weight']
    ideal_tech = [tech.lower() for tech in criteria['ideal_technologies']]

    confirmed = data.get('technology_stack', {}).get('confirmed_technologies', [])
    likely = data.get('technology_stack', {}).get('likely_technologies', [])
    all_tech = [t.lower() for t in (confirmed + likely)]

    matches = sum(1 for tech in ideal_tech if any(t in tech_item for tech_item in all_tech for t in [tech]))
    tech_sophistication = data.get('technology_stack', {}).get('technical_sophistication', 'low')

    if matches >= 3:
        raw_score = 100
    elif matches == 2:
        raw_score = 80
    elif matches == 1:
        raw_score = 60
    elif tech_sophistication == 'high':
        raw_score = 70
    elif tech_sophistication == 'medium':
        raw_score = 50
    else:
        raw_score = 30

    return {
        'raw_score': round(raw_score, 1),
        'weighted_score': round((raw_score * weight) / 100, 1),
        'weight': weight,
        'value': confirmed + likely,
        'reasoning': f"Tech matches: {matches}, Sophistication: {tech_sophistication}"
    }


def score_growth_signals(data: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Score based on growth indicators."""
    weight = criteria['weight']

    growth_data = data.get('funding_and_growth', {})
    is_hiring = growth_data.get('is_hiring', False)
    growth_indicators = growth_data.get('growth_indicators', [])
    expansion_signals = growth_data.get('expansion_signals', [])

    signal_count = len(growth_indicators) + len(expansion_signals)
    if is_hiring:
        signal_count += 1

    if signal_count >= 4:
        raw_score = 100
    elif signal_count == 3:
        raw_score = 80
    elif signal_count == 2:
        raw_score = 60
    elif signal_count == 1:
        raw_score = 40
    else:
        raw_score = 20

    return {
        'raw_score': round(raw_score, 1),
        'weighted_score': round((raw_score * weight) / 100, 1),
        'weight': weight,
        'value': {'is_hiring': is_hiring, 'signals': signal_count},
        'reasoning': f"Growth signals detected: {signal_count}"
    }


def score_market_presence(data: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Score based on market presence and brand maturity."""
    weight = criteria['weight']

    presence = data.get('market_presence', {})
    brand_maturity = presence.get('brand_maturity', 'unknown')
    content_marketing = presence.get('content_marketing', False)
    seo_quality = presence.get('seo_quality', 'poor')
    social_activity = presence.get('social_media_activity', 'none')

    score = 0
    if brand_maturity == 'established':
        score += 30
    elif brand_maturity == 'growing':
        score += 20

    if content_marketing:
        score += 20

    if seo_quality in ['excellent', 'good']:
        score += 25
    elif seo_quality == 'average':
        score += 15

    if social_activity in ['active', 'moderate']:
        score += 25
    elif social_activity == 'minimal':
        score += 10

    raw_score = min(100, score)

    return {
        'raw_score': round(raw_score, 1),
        'weighted_score': round((raw_score * weight) / 100, 1),
        'weight': weight,
        'value': {
            'brand_maturity': brand_maturity,
            'content_marketing': content_marketing,
            'seo_quality': seo_quality,
            'social_activity': social_activity
        },
        'reasoning': f"Brand: {brand_maturity}, SEO: {seo_quality}, Social: {social_activity}"
    }


def get_recommendation(category: str, score: float) -> str:
    """Get action recommendation based on lead category."""
    recommendations = {
        'hot_lead': f"PRIORITY: High-value prospect (score: {score}/100). Immediate outreach recommended. Assign to senior sales rep for personalized engagement.",
        'warm_lead': f"QUALIFIED: Good fit (score: {score}/100). Add to nurture sequence. Schedule demo or discovery call within 1 week.",
        'cold_lead': f"MODERATE FIT: Below ideal (score: {score}/100). Add to long-term nurture campaign. Monitor for growth signals before direct outreach.",
        'poor_fit': f"LOW PRIORITY: Poor ICP match (score: {score}/100). Consider excluding from active outreach unless specific high-value indicator emerges."
    }
    return recommendations.get(category, "No recommendation available")


# ============================================================================
# INPUT/OUTPUT HANDLING
# ============================================================================

def parse_arguments() -> Optional[Dict[str, str]]:
    """
    Parse command line arguments.

    Returns:
        Dictionary with 'domain' and optional 'company', or None if reading from stdin
    """
    parser = argparse.ArgumentParser(
        description='Enrich company data and score leads against ICP criteria'
    )
    parser.add_argument(
        '--domain',
        type=str,
        help='Company domain to enrich (e.g., stripe.com)'
    )
    parser.add_argument(
        '--company',
        type=str,
        help='Company name (optional, will be detected if not provided)'
    )

    args = parser.parse_args()

    # If domain provided, return it
    if args.domain:
        result = {'domain': args.domain}
        if args.company:
            result['company'] = args.company
        return result

    # If no args, check stdin (for Make.com webhook mode)
    if not sys.stdin.isatty():
        return None  # Signal to read from stdin

    parser.print_help()
    sys.exit(1)


def read_stdin_json() -> Dict[str, str]:
    """
    Read JSON input from stdin (for Make.com webhook integration).

    Returns:
        Dictionary with 'domain' and optional 'company'
    """
    try:
        data = json.load(sys.stdin)

        if 'domain' not in data:
            raise ValueError("JSON must contain 'domain' field")

        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input: {str(e)}")


def format_output(
    enriched_data: Dict[str, Any],
    scoring_results: Dict[str, Any],
    domain: str,
    company_name: Optional[str]
) -> Dict[str, Any]:
    """
    Format the final output with metadata.

    Args:
        enriched_data: Enriched company data
        scoring_results: Lead scoring results
        domain: Company domain
        company_name: Company name

    Returns:
        Complete enrichment report with scoring
    """
    return {
        'enrichment_metadata': {
            'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'domain': domain,
            'company_name': company_name or enriched_data.get('company_profile', {}).get('name', 'Unknown'),
            'model_used': MODEL_NAME
        },
        'lead_score': scoring_results['total_score'],
        'lead_category': scoring_results['category'],
        'recommendation': scoring_results['recommendation'],
        'scoring_details': {
            'score_breakdown': scoring_results['score_breakdown'],
            'category_thresholds': scoring_results['category_thresholds']
        },
        'enrichment_data': enriched_data
    }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function - orchestrates the entire enrichment process.
    """
    try:
        # Step 1: Get input (CLI args or stdin)
        params = parse_arguments()

        if params is None:
            # Read from stdin (Make.com mode)
            params = read_stdin_json()

        domain = params['domain']
        company_name = params.get('company')

        # Step 2: Load ICP configuration
        print(f"Loading ICP configuration...", file=sys.stderr)
        icp_config = load_icp_config()

        # Step 3: Fetch company data
        print(f"Fetching company data from {domain}...", file=sys.stderr)
        company_data = fetch_company_data(domain, company_name)

        if 'error' in company_data:
            print(f"Warning: {company_data['error']}", file=sys.stderr)
            print("Continuing with limited data...", file=sys.stderr)

        # Step 4: Enrich data using Claude
        print(f"Enriching company data with AI...", file=sys.stderr)
        enriched_data = enrich_company_data(company_data, icp_config)

        # Step 5: Score lead against ICP
        print(f"Scoring lead against ICP criteria...", file=sys.stderr)
        scoring_results = score_lead(enriched_data, icp_config)

        # Step 6: Format output
        final_output = format_output(
            enriched_data,
            scoring_results,
            domain,
            company_name
        )

        # Step 7: Output JSON to stdout
        print(json.dumps(final_output, indent=2))

        # Show summary to stderr
        score = scoring_results['total_score']
        category = scoring_results['category'].replace('_', ' ').title()
        print(f"\n✓ Enrichment completed!", file=sys.stderr)
        print(f"  Lead Score: {score}/100 ({category})", file=sys.stderr)

    except KeyboardInterrupt:
        print("\n\nEnrichment cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
