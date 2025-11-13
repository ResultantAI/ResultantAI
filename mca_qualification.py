#!/usr/bin/env python3
"""
MCA (Merchant Cash Advance) Qualification System
=================================================
An automated underwriting tool that evaluates business eligibility for merchant cash advances.

Usage:
    # Command line mode
    python mca_qualification.py --revenue 500000 --time-in-business 24 --credit-score 650 --industry "Restaurant"

    # Make.com webhook mode (reads JSON from stdin)
    echo '{"monthly_revenue": 50000, "time_in_business_months": 24, "credit_score": 650, "industry": "Restaurant"}' | python mca_qualification.py
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# ============================================================================
# CONFIGURATION
# ============================================================================

MCA_CONFIG_PATH = os.getenv('MCA_CONFIG_PATH', 'mca_criteria.json')


# ============================================================================
# MCA CRITERIA LOADING
# ============================================================================

def load_mca_criteria(config_path: str = MCA_CONFIG_PATH) -> Dict[str, Any]:
    """
    Load MCA qualification criteria from JSON file.

    Args:
        config_path: Path to MCA criteria configuration file

    Returns:
        Dictionary containing MCA lending criteria
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Warning: MCA config file not found at {config_path}, using defaults", file=sys.stderr)
        return get_default_mca_criteria()
    except json.JSONDecodeError as e:
        print(f"Warning: Invalid JSON in MCA config: {e}, using defaults", file=sys.stderr)
        return get_default_mca_criteria()


def get_default_mca_criteria() -> Dict[str, Any]:
    """
    Return default MCA qualification criteria.

    Returns:
        Default MCA criteria dictionary
    """
    return {
        "minimum_requirements": {
            "monthly_revenue": 10000,
            "time_in_business_months": 6,
            "credit_score": 500,
            "description": "Absolute minimum thresholds for consideration"
        },
        "revenue_tiers": {
            "tier_1": {"min": 100000, "max_advance_percentage": 250, "description": "High revenue ($100k+/month)"},
            "tier_2": {"min": 50000, "max_advance_percentage": 200, "description": "Strong revenue ($50k-100k/month)"},
            "tier_3": {"min": 25000, "max_advance_percentage": 150, "description": "Good revenue ($25k-50k/month)"},
            "tier_4": {"min": 10000, "max_advance_percentage": 100, "description": "Minimum revenue ($10k-25k/month)"}
        },
        "credit_score_tiers": {
            "excellent": {"min": 720, "factor_rate_adjustment": -0.05, "description": "Excellent credit"},
            "good": {"min": 680, "factor_rate_adjustment": 0.0, "description": "Good credit"},
            "fair": {"min": 620, "factor_rate_adjustment": 0.03, "description": "Fair credit"},
            "poor": {"min": 550, "factor_rate_adjustment": 0.08, "description": "Poor credit"},
            "very_poor": {"min": 500, "factor_rate_adjustment": 0.15, "description": "Very poor credit"}
        },
        "time_in_business_multipliers": {
            "established": {"min_months": 36, "multiplier": 1.2, "description": "3+ years in business"},
            "mature": {"min_months": 24, "multiplier": 1.1, "description": "2-3 years in business"},
            "growing": {"min_months": 12, "multiplier": 1.0, "description": "1-2 years in business"},
            "new": {"min_months": 6, "multiplier": 0.8, "description": "6-12 months in business"}
        },
        "industry_risk_factors": {
            "low_risk": {
                "industries": ["Healthcare", "Professional Services", "Technology", "Education"],
                "factor_rate_adjustment": -0.02,
                "description": "Stable, low-risk industries"
            },
            "medium_risk": {
                "industries": ["Retail", "E-commerce", "Construction", "Manufacturing"],
                "factor_rate_adjustment": 0.0,
                "description": "Moderate-risk industries"
            },
            "high_risk": {
                "industries": ["Restaurant", "Hospitality", "Auto Repair", "Salon/Spa"],
                "factor_rate_adjustment": 0.05,
                "description": "Higher-risk industries with volatility"
            }
        },
        "base_factor_rates": {
            "premium": {"min_score": 85, "factor_rate": 1.15, "description": "Premium terms"},
            "standard": {"min_score": 70, "factor_rate": 1.25, "description": "Standard terms"},
            "subprime": {"min_score": 50, "factor_rate": 1.35, "description": "Subprime terms"},
            "high_risk": {"min_score": 0, "factor_rate": 1.45, "description": "High-risk terms"}
        },
        "repayment_terms": {
            "short": {"months": 3, "multiplier": 0.95, "description": "3-month term"},
            "standard": {"months": 6, "multiplier": 1.0, "description": "6-month term"},
            "extended": {"months": 9, "multiplier": 1.05, "description": "9-month term"},
            "long": {"months": 12, "multiplier": 1.1, "description": "12-month term"}
        }
    }


# ============================================================================
# QUALIFICATION SCORING ENGINE
# ============================================================================

def calculate_qualification_score(business_data: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate overall qualification score based on business data.

    Args:
        business_data: Business information
        criteria: MCA criteria configuration

    Returns:
        Scoring results with breakdown
    """
    scores = {}
    total_score = 0
    max_score = 100

    # Score revenue (40 points)
    revenue_score = score_revenue(business_data['monthly_revenue'], criteria)
    scores['revenue'] = revenue_score
    total_score += revenue_score['score']

    # Score credit (25 points)
    credit_score = score_credit(business_data['credit_score'], criteria)
    scores['credit'] = credit_score
    total_score += credit_score['score']

    # Score time in business (20 points)
    time_score = score_time_in_business(business_data['time_in_business_months'], criteria)
    scores['time_in_business'] = time_score
    total_score += time_score['score']

    # Score industry (15 points)
    industry_score = score_industry(business_data['industry'], criteria)
    scores['industry'] = industry_score
    total_score += industry_score['score']

    return {
        'total_score': round(total_score, 1),
        'max_score': max_score,
        'score_breakdown': scores,
        'grade': get_score_grade(total_score)
    }


def score_revenue(monthly_revenue: float, criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Score based on monthly revenue."""
    tiers = criteria['revenue_tiers']
    max_points = 40

    if monthly_revenue >= tiers['tier_1']['min']:
        score = max_points
        tier = 'tier_1'
    elif monthly_revenue >= tiers['tier_2']['min']:
        score = max_points * 0.85
        tier = 'tier_2'
    elif monthly_revenue >= tiers['tier_3']['min']:
        score = max_points * 0.70
        tier = 'tier_3'
    elif monthly_revenue >= tiers['tier_4']['min']:
        score = max_points * 0.50
        tier = 'tier_4'
    else:
        score = 0
        tier = 'below_minimum'

    return {
        'score': round(score, 1),
        'max_points': max_points,
        'tier': tier,
        'value': monthly_revenue,
        'reasoning': f"Monthly revenue of ${monthly_revenue:,.0f} falls in {tier}"
    }


def score_credit(credit_score: int, criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Score based on credit score."""
    tiers = criteria['credit_score_tiers']
    max_points = 25

    if credit_score >= tiers['excellent']['min']:
        score = max_points
        tier = 'excellent'
    elif credit_score >= tiers['good']['min']:
        score = max_points * 0.90
        tier = 'good'
    elif credit_score >= tiers['fair']['min']:
        score = max_points * 0.75
        tier = 'fair'
    elif credit_score >= tiers['poor']['min']:
        score = max_points * 0.60
        tier = 'poor'
    elif credit_score >= tiers['very_poor']['min']:
        score = max_points * 0.40
        tier = 'very_poor'
    else:
        score = 0
        tier = 'below_minimum'

    return {
        'score': round(score, 1),
        'max_points': max_points,
        'tier': tier,
        'value': credit_score,
        'reasoning': f"Credit score of {credit_score} is {tier}"
    }


def score_time_in_business(months: int, criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Score based on time in business."""
    tiers = criteria['time_in_business_multipliers']
    max_points = 20

    if months >= tiers['established']['min_months']:
        score = max_points
        tier = 'established'
    elif months >= tiers['mature']['min_months']:
        score = max_points * 0.85
        tier = 'mature'
    elif months >= tiers['growing']['min_months']:
        score = max_points * 0.70
        tier = 'growing'
    elif months >= tiers['new']['min_months']:
        score = max_points * 0.50
        tier = 'new'
    else:
        score = 0
        tier = 'too_new'

    return {
        'score': round(score, 1),
        'max_points': max_points,
        'tier': tier,
        'value': months,
        'reasoning': f"{months} months in business ({tier})"
    }


def score_industry(industry: str, criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Score based on industry risk."""
    risk_factors = criteria['industry_risk_factors']
    max_points = 15

    industry_lower = industry.lower()

    for risk_level, risk_data in risk_factors.items():
        if any(ind.lower() in industry_lower or industry_lower in ind.lower()
               for ind in risk_data['industries']):
            if risk_level == 'low_risk':
                score = max_points
            elif risk_level == 'medium_risk':
                score = max_points * 0.80
            else:  # high_risk
                score = max_points * 0.60

            return {
                'score': round(score, 1),
                'max_points': max_points,
                'risk_level': risk_level,
                'value': industry,
                'reasoning': f"{industry} is {risk_data['description']}"
            }

    # Default to medium risk if industry not recognized
    return {
        'score': round(max_points * 0.75, 1),
        'max_points': max_points,
        'risk_level': 'unknown',
        'value': industry,
        'reasoning': f"{industry} - risk level unknown, treated as medium risk"
    }


def get_score_grade(score: float) -> str:
    """Convert score to letter grade."""
    if score >= 85:
        return 'A'
    elif score >= 70:
        return 'B'
    elif score >= 50:
        return 'C'
    elif score >= 30:
        return 'D'
    else:
        return 'F'


# ============================================================================
# ADVANCE CALCULATION ENGINE
# ============================================================================

def calculate_advance_offer(
    business_data: Dict[str, Any],
    qualification_score: Dict[str, Any],
    criteria: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculate MCA offer details including advance amount and factor rate.

    Args:
        business_data: Business information
        qualification_score: Qualification scoring results
        criteria: MCA criteria configuration

    Returns:
        Offer details dictionary
    """
    monthly_revenue = business_data['monthly_revenue']
    credit_score = business_data['credit_score']
    time_in_business = business_data['time_in_business_months']
    industry = business_data['industry']

    # Determine revenue tier and max advance percentage
    revenue_tier_data = get_revenue_tier(monthly_revenue, criteria)
    max_advance_pct = revenue_tier_data['max_advance_percentage']

    # Apply time in business multiplier
    time_multiplier = get_time_multiplier(time_in_business, criteria)

    # Calculate base advance amount (percentage of monthly revenue)
    base_advance = monthly_revenue * (max_advance_pct / 100)
    adjusted_advance = base_advance * time_multiplier

    # Calculate factor rate based on risk profile
    base_factor_rate = get_base_factor_rate(qualification_score['total_score'], criteria)
    credit_adjustment = get_credit_adjustment(credit_score, criteria)
    industry_adjustment = get_industry_adjustment(industry, criteria)

    final_factor_rate = base_factor_rate + credit_adjustment + industry_adjustment
    final_factor_rate = max(1.10, min(1.50, final_factor_rate))  # Cap between 1.10 and 1.50

    # Calculate repayment details
    total_repayment = adjusted_advance * final_factor_rate

    # Determine recommended term based on score
    recommended_term = get_recommended_term(qualification_score['total_score'])
    daily_repayment = total_repayment / (recommended_term * 22)  # 22 business days per month

    # Calculate effective APR for disclosure
    effective_apr = calculate_effective_apr(final_factor_rate, recommended_term)

    return {
        'advance_amount': round(adjusted_advance, 2),
        'factor_rate': round(final_factor_rate, 3),
        'total_repayment': round(total_repayment, 2),
        'recommended_term_months': recommended_term,
        'daily_payment': round(daily_repayment, 2),
        'effective_apr': round(effective_apr, 2),
        'calculation_details': {
            'base_advance_percentage': max_advance_pct,
            'time_in_business_multiplier': time_multiplier,
            'base_factor_rate': round(base_factor_rate, 3),
            'credit_adjustment': round(credit_adjustment, 3),
            'industry_adjustment': round(industry_adjustment, 3)
        }
    }


def get_revenue_tier(monthly_revenue: float, criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Get revenue tier data."""
    tiers = criteria['revenue_tiers']

    if monthly_revenue >= tiers['tier_1']['min']:
        return tiers['tier_1']
    elif monthly_revenue >= tiers['tier_2']['min']:
        return tiers['tier_2']
    elif monthly_revenue >= tiers['tier_3']['min']:
        return tiers['tier_3']
    else:
        return tiers['tier_4']


def get_time_multiplier(months: int, criteria: Dict[str, Any]) -> float:
    """Get time in business multiplier."""
    tiers = criteria['time_in_business_multipliers']

    if months >= tiers['established']['min_months']:
        return tiers['established']['multiplier']
    elif months >= tiers['mature']['min_months']:
        return tiers['mature']['multiplier']
    elif months >= tiers['growing']['min_months']:
        return tiers['growing']['multiplier']
    else:
        return tiers['new']['multiplier']


def get_base_factor_rate(score: float, criteria: Dict[str, Any]) -> float:
    """Get base factor rate from score."""
    rates = criteria['base_factor_rates']

    if score >= rates['premium']['min_score']:
        return rates['premium']['factor_rate']
    elif score >= rates['standard']['min_score']:
        return rates['standard']['factor_rate']
    elif score >= rates['subprime']['min_score']:
        return rates['subprime']['factor_rate']
    else:
        return rates['high_risk']['factor_rate']


def get_credit_adjustment(credit_score: int, criteria: Dict[str, Any]) -> float:
    """Get factor rate adjustment based on credit."""
    tiers = criteria['credit_score_tiers']

    if credit_score >= tiers['excellent']['min']:
        return tiers['excellent']['factor_rate_adjustment']
    elif credit_score >= tiers['good']['min']:
        return tiers['good']['factor_rate_adjustment']
    elif credit_score >= tiers['fair']['min']:
        return tiers['fair']['factor_rate_adjustment']
    elif credit_score >= tiers['poor']['min']:
        return tiers['poor']['factor_rate_adjustment']
    else:
        return tiers['very_poor']['factor_rate_adjustment']


def get_industry_adjustment(industry: str, criteria: Dict[str, Any]) -> float:
    """Get factor rate adjustment based on industry."""
    risk_factors = criteria['industry_risk_factors']
    industry_lower = industry.lower()

    for risk_level, risk_data in risk_factors.items():
        if any(ind.lower() in industry_lower or industry_lower in ind.lower()
               for ind in risk_data['industries']):
            return risk_data['factor_rate_adjustment']

    return 0.0  # Default neutral adjustment


def get_recommended_term(score: float) -> int:
    """Get recommended term in months based on score."""
    if score >= 85:
        return 6
    elif score >= 70:
        return 6
    elif score >= 50:
        return 9
    else:
        return 12


def calculate_effective_apr(factor_rate: float, term_months: int) -> float:
    """
    Calculate effective APR for disclosure purposes.

    Note: This is a simplified calculation for demonstration.
    Real MCA APR calculations are complex due to daily payments.
    """
    # Calculate cost as percentage
    cost_percentage = (factor_rate - 1.0) * 100

    # Annualize the cost
    if term_months > 0:
        annual_rate = (cost_percentage / term_months) * 12
    else:
        annual_rate = 0

    return annual_rate


# ============================================================================
# QUALIFICATION DECISION ENGINE
# ============================================================================

def make_qualification_decision(
    business_data: Dict[str, Any],
    qualification_score: Dict[str, Any],
    criteria: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Make final qualification decision with detailed reasoning.

    Args:
        business_data: Business information
        qualification_score: Qualification scoring results
        criteria: MCA criteria configuration

    Returns:
        Decision dictionary with approval status and reasoning
    """
    min_req = criteria['minimum_requirements']

    # Check absolute minimums
    rejections = []

    if business_data['monthly_revenue'] < min_req['monthly_revenue']:
        rejections.append(f"Monthly revenue ${business_data['monthly_revenue']:,.0f} below minimum ${min_req['monthly_revenue']:,.0f}")

    if business_data['time_in_business_months'] < min_req['time_in_business_months']:
        rejections.append(f"Time in business {business_data['time_in_business_months']} months below minimum {min_req['time_in_business_months']} months")

    if business_data['credit_score'] < min_req['credit_score']:
        rejections.append(f"Credit score {business_data['credit_score']} below minimum {min_req['credit_score']}")

    # If any minimums not met, reject
    if rejections:
        return {
            'status': 'REJECTED',
            'decision': 'declined',
            'primary_reason': 'Does not meet minimum requirements',
            'rejection_reasons': rejections,
            'recommendations': get_rejection_recommendations(rejections)
        }

    # Score-based decision
    score = qualification_score['total_score']
    grade = qualification_score['grade']

    if score >= 50:
        return {
            'status': 'APPROVED',
            'decision': 'approved',
            'approval_tier': get_approval_tier(score),
            'confidence_level': get_confidence_level(score),
            'approval_reasons': get_approval_reasons(qualification_score),
            'conditions': get_approval_conditions(score, business_data)
        }
    else:
        return {
            'status': 'REJECTED',
            'decision': 'declined',
            'primary_reason': f'Qualification score {score}/100 (Grade {grade}) below approval threshold',
            'rejection_reasons': get_low_score_reasons(qualification_score),
            'recommendations': get_improvement_recommendations(qualification_score)
        }


def get_approval_tier(score: float) -> str:
    """Get approval tier based on score."""
    if score >= 85:
        return 'Premium'
    elif score >= 70:
        return 'Standard'
    else:
        return 'Subprime'


def get_confidence_level(score: float) -> str:
    """Get underwriting confidence level."""
    if score >= 85:
        return 'High'
    elif score >= 70:
        return 'Medium-High'
    elif score >= 50:
        return 'Medium'
    else:
        return 'Low'


def get_approval_reasons(qualification_score: Dict[str, Any]) -> List[str]:
    """Get list of approval reasons."""
    reasons = []
    breakdown = qualification_score['score_breakdown']

    if breakdown['revenue']['score'] >= 30:
        reasons.append(f"Strong monthly revenue of ${breakdown['revenue']['value']:,.0f}")

    if breakdown['credit']['score'] >= 20:
        reasons.append(f"Good credit profile (score: {breakdown['credit']['value']})")

    if breakdown['time_in_business']['score'] >= 15:
        reasons.append(f"Established business ({breakdown['time_in_business']['value']} months)")

    if breakdown['industry']['score'] >= 12:
        reasons.append(f"Favorable industry profile ({breakdown['industry']['value']})")

    if not reasons:
        reasons.append("Meets all minimum qualification requirements")

    return reasons


def get_approval_conditions(score: float, business_data: Dict[str, Any]) -> List[str]:
    """Get any conditions on approval."""
    conditions = []

    if score < 70:
        conditions.append("Subject to bank statement review for final approval")

    if business_data['credit_score'] < 620:
        conditions.append("May require personal guarantee")

    if business_data['time_in_business_months'] < 12:
        conditions.append("Additional documentation required (tax returns, bank statements)")

    return conditions if conditions else ["Standard approval - no additional conditions"]


def get_rejection_recommendations(rejections: List[str]) -> List[str]:
    """Get recommendations for rejected applications."""
    recommendations = []

    for rejection in rejections:
        if 'revenue' in rejection.lower():
            recommendations.append("Focus on increasing monthly revenue through sales growth or additional revenue streams")
        if 'time in business' in rejection.lower():
            recommendations.append("Reapply after 6+ months in business with consistent revenue")
        if 'credit score' in rejection.lower():
            recommendations.append("Work on improving business credit score through timely payments and credit utilization")

    recommendations.append("Consider alternative financing options (business credit cards, SBA loans, equipment financing)")

    return recommendations


def get_low_score_reasons(qualification_score: Dict[str, Any]) -> List[str]:
    """Get reasons for low qualification score."""
    reasons = []
    breakdown = qualification_score['score_breakdown']

    if breakdown['revenue']['score'] < 20:
        reasons.append(f"Low monthly revenue: ${breakdown['revenue']['value']:,.0f}")

    if breakdown['credit']['score'] < 15:
        reasons.append(f"Below-average credit score: {breakdown['credit']['value']}")

    if breakdown['time_in_business']['score'] < 10:
        reasons.append(f"Limited operating history: {breakdown['time_in_business']['value']} months")

    if breakdown['industry']['score'] < 10:
        reasons.append(f"High-risk industry: {breakdown['industry']['value']}")

    return reasons


def get_improvement_recommendations(qualification_score: Dict[str, Any]) -> List[str]:
    """Get recommendations for improving qualification."""
    recommendations = []
    breakdown = qualification_score['score_breakdown']

    if breakdown['revenue']['score'] < 25:
        recommendations.append("Increase monthly revenue to $50,000+ for better terms")

    if breakdown['credit']['score'] < 18:
        recommendations.append("Improve credit score to 650+ through consistent payment history")

    if breakdown['time_in_business']['score'] < 14:
        recommendations.append("Build longer operating history (12+ months preferred)")

    recommendations.append("Reapply in 3-6 months with improved financials")

    return recommendations


# ============================================================================
# INPUT/OUTPUT HANDLING
# ============================================================================

def parse_arguments() -> Optional[Dict[str, Any]]:
    """
    Parse command line arguments.

    Returns:
        Dictionary with business data, or None if reading from stdin
    """
    parser = argparse.ArgumentParser(
        description='Evaluate MCA qualification and calculate advance terms'
    )
    parser.add_argument('--revenue', type=float, help='Monthly revenue in dollars')
    parser.add_argument('--time-in-business', type=int, help='Time in business (months)')
    parser.add_argument('--credit-score', type=int, help='Business credit score (300-850)')
    parser.add_argument('--industry', type=str, help='Business industry')

    args = parser.parse_args()

    # If all args provided, return them
    if args.revenue and args.time_in_business and args.credit_score and args.industry:
        return {
            'monthly_revenue': args.revenue,
            'time_in_business_months': args.time_in_business,
            'credit_score': args.credit_score,
            'industry': args.industry
        }

    # If no args, check stdin
    if not sys.stdin.isatty():
        return None

    # If partial args, show error
    if any([args.revenue, args.time_in_business, args.credit_score, args.industry]):
        parser.error('All arguments required: --revenue, --time-in-business, --credit-score, --industry')

    parser.print_help()
    sys.exit(1)


def read_stdin_json() -> Dict[str, Any]:
    """Read JSON input from stdin (Make.com mode)."""
    try:
        data = json.load(sys.stdin)

        required_fields = ['monthly_revenue', 'time_in_business_months', 'credit_score', 'industry']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"JSON must contain '{field}' field")

        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input: {str(e)}")


def format_output(
    business_data: Dict[str, Any],
    qualification_score: Dict[str, Any],
    decision: Dict[str, Any],
    offer: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """Format final output."""
    result = {
        'qualification_metadata': {
            'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'business_details': business_data
        },
        'qualification_score': qualification_score,
        'decision': decision
    }

    if offer:
        result['offer_details'] = offer

    return result


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    try:
        # Step 1: Get input
        params = parse_arguments()

        if params is None:
            params = read_stdin_json()

        business_data = params

        # Step 2: Load MCA criteria
        print(f"Loading MCA qualification criteria...", file=sys.stderr)
        criteria = load_mca_criteria()

        # Step 3: Calculate qualification score
        print(f"Calculating qualification score...", file=sys.stderr)
        qualification_score = calculate_qualification_score(business_data, criteria)

        # Step 4: Make decision
        print(f"Evaluating qualification...", file=sys.stderr)
        decision = make_qualification_decision(business_data, qualification_score, criteria)

        # Step 5: Calculate offer if approved
        offer = None
        if decision['decision'] == 'approved':
            print(f"Calculating advance offer...", file=sys.stderr)
            offer = calculate_advance_offer(business_data, qualification_score, criteria)

        # Step 6: Format and output
        output = format_output(business_data, qualification_score, decision, offer)
        print(json.dumps(output, indent=2))

        # Summary to stderr
        status = decision['status']
        score = qualification_score['total_score']
        print(f"\n✓ Qualification completed!", file=sys.stderr)
        print(f"  Status: {status}", file=sys.stderr)
        print(f"  Score: {score}/100 (Grade {qualification_score['grade']})", file=sys.stderr)

        if offer:
            print(f"  Advance: ${offer['advance_amount']:,.2f}", file=sys.stderr)
            print(f"  Factor Rate: {offer['factor_rate']}", file=sys.stderr)

    except KeyboardInterrupt:
        print("\n\nQualification cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
