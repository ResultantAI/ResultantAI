#!/usr/bin/env python3
"""
MCA (Merchant Cash Advance) Qualification System
AI-powered business loan qualification with compliance logging
"""

import json
import sys
import os
import argparse
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "claude-sonnet-4-5-20250929")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))

# Qualification thresholds
MIN_REVENUE = 100000  # $100K annual revenue
MIN_CREDIT_SCORE = 500
MIN_BUSINESS_AGE_MONTHS = 6


def log_progress(message: str):
    """Log progress to stderr"""
    print(f"[MCA] {message}", file=sys.stderr)


def validate_inputs(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate required inputs and ranges"""
    required_fields = ["company_name", "annual_revenue", "credit_score", "business_age_months"]

    # Check required fields
    for field in required_fields:
        if field not in data or data[field] is None:
            return False, f"Missing required field: {field}"

    # Validate revenue
    try:
        revenue = float(data["annual_revenue"])
        if revenue <= 0:
            return False, "Annual revenue must be greater than 0"
        if revenue > 100000000:  # $100M sanity check
            return False, "Annual revenue exceeds maximum threshold"
    except (ValueError, TypeError):
        return False, "Invalid annual revenue format (must be a number)"

    # Validate credit score
    try:
        credit = int(data["credit_score"])
        if credit < 300 or credit > 850:
            return False, "Credit score must be between 300 and 850"
    except (ValueError, TypeError):
        return False, "Invalid credit score format (must be an integer)"

    # Validate business age
    try:
        age = int(data["business_age_months"])
        if age < 0:
            return False, "Business age cannot be negative"
        if age > 600:  # 50 years sanity check
            return False, "Business age exceeds reasonable maximum"
    except (ValueError, TypeError):
        return False, "Invalid business age format (must be an integer)"

    return True, None


def qualify_mca(
    company_name: str,
    annual_revenue: float,
    credit_score: int,
    business_age_months: int,
    industry: str = "General Business",
    monthly_revenue: Optional[float] = None,
    existing_debt: Optional[float] = None,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Qualify a business for Merchant Cash Advance

    Returns structured qualification decision with AI-powered analysis
    """

    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not found in environment")

    log_progress(f"Qualifying: {company_name}")
    log_progress(f"Revenue: ${annual_revenue:,.0f} | Credit: {credit_score} | Age: {business_age_months}mo")

    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Calculate derived metrics
    monthly_avg = monthly_revenue if monthly_revenue else annual_revenue / 12
    debt_ratio = (existing_debt / annual_revenue * 100) if existing_debt else 0

    # Build qualification prompt
    qualification_prompt = f"""You are an MCA (Merchant Cash Advance) underwriter. Analyze this business application and provide a qualification decision.

APPLICANT INFORMATION:
- Company Name: {company_name}
- Industry: {industry}
- Annual Revenue: ${annual_revenue:,.2f}
- Monthly Revenue (avg): ${monthly_avg:,.2f}
- Credit Score: {credit_score}
- Business Age: {business_age_months} months ({business_age_months/12:.1f} years)
- Existing Debt: ${existing_debt:,.2f if existing_debt else 0}
- Debt-to-Revenue Ratio: {debt_ratio:.1f}%
{f"- Additional Notes: {notes}" if notes else ""}

QUALIFICATION CRITERIA:
- Minimum Revenue: ${MIN_REVENUE:,}/year
- Minimum Credit Score: {MIN_CREDIT_SCORE}
- Minimum Business Age: {MIN_BUSINESS_AGE_MONTHS} months
- Maximum Debt Ratio: 50%

TASK:
Provide a comprehensive qualification analysis in the following JSON format:

{{
  "decision": "APPROVED" or "REJECTED",
  "risk_level": "low" or "medium" or "high",
  "recommended_advance_amount": {{
    "min": 0,
    "max": 0,
    "recommended": 0
  }},
  "factor_payback_rate": 1.20,
  "estimated_payback_months": 12,
  "decision_factors": {{
    "revenue_assessment": "Brief assessment of revenue strength",
    "credit_assessment": "Brief assessment of credit profile",
    "business_stability": "Brief assessment of business age/stability",
    "industry_risk": "Brief industry-specific risk assessment",
    "debt_burden": "Brief assessment of existing debt burden"
  }},
  "approval_conditions": ["Condition 1", "Condition 2"],
  "red_flags": ["Any concerns or warnings"],
  "underwriter_notes": "Additional context for decision"
}}

GUIDELINES:
- Advance amount should be 10-50% of annual revenue for qualified applicants
- Factor rates typically 1.15-1.35 based on risk
- Payback typically 6-18 months
- Be conservative but fair
- Reject if below minimum thresholds
- Consider industry-specific risks
- Flag any concerning debt levels or credit issues

Provide ONLY the JSON output, no other text."""

    log_progress("Analyzing qualification with AI...")

    # Call Claude API
    try:
        message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            messages=[{
                "role": "user",
                "content": qualification_prompt
            }]
        )

        # Extract and parse response
        response_text = message.content[0].text.strip()

        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        qualification_data = json.loads(response_text.strip())

    except json.JSONDecodeError as e:
        log_progress(f"Failed to parse AI response: {e}")
        raise
    except Exception as e:
        log_progress(f"API call failed: {e}")
        raise

    # Build complete output
    output = {
        "qualification_metadata": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "company_name": company_name,
            "industry": industry,
            "model_used": MODEL_NAME
        },
        "application_data": {
            "annual_revenue": annual_revenue,
            "monthly_revenue_avg": monthly_avg,
            "credit_score": credit_score,
            "business_age_months": business_age_months,
            "existing_debt": existing_debt or 0,
            "debt_to_revenue_ratio": round(debt_ratio, 2)
        },
        "qualification_result": qualification_data,
        "compliance_log": {
            "minimum_thresholds_met": {
                "revenue": annual_revenue >= MIN_REVENUE,
                "credit_score": credit_score >= MIN_CREDIT_SCORE,
                "business_age": business_age_months >= MIN_BUSINESS_AGE_MONTHS
            },
            "decision_timestamp": datetime.utcnow().isoformat() + "Z",
            "model_version": MODEL_NAME
        }
    }

    log_progress(f"Decision: {qualification_data['decision']} | Risk: {qualification_data['risk_level']}")

    return output


def main():
    """Main entry point - supports both CLI args and JSON stdin"""

    # Check if stdin has data (Make.com mode)
    if not sys.stdin.isatty():
        try:
            input_data = json.load(sys.stdin)

            # Validate inputs
            is_valid, error_msg = validate_inputs(input_data)
            if not is_valid:
                error_output = {
                    "error": error_msg,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
                print(json.dumps(error_output, indent=2))
                sys.exit(1)

            # Run qualification
            result = qualify_mca(
                company_name=input_data["company_name"],
                annual_revenue=float(input_data["annual_revenue"]),
                credit_score=int(input_data["credit_score"]),
                business_age_months=int(input_data["business_age_months"]),
                industry=input_data.get("industry", "General Business"),
                monthly_revenue=input_data.get("monthly_revenue"),
                existing_debt=input_data.get("existing_debt"),
                notes=input_data.get("notes")
            )

            # Output JSON to stdout
            print(json.dumps(result, indent=2))

        except json.JSONDecodeError:
            error_output = {
                "error": "Invalid JSON input",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            print(json.dumps(error_output, indent=2))
            sys.exit(1)
        except Exception as e:
            error_output = {
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            print(json.dumps(error_output, indent=2))
            sys.exit(1)

    else:
        # CLI mode with argparse
        parser = argparse.ArgumentParser(
            description="MCA Qualification System - AI-powered business loan qualification"
        )
        parser.add_argument("--company", required=True, help="Company name")
        parser.add_argument("--revenue", type=float, required=True, help="Annual revenue in USD")
        parser.add_argument("--credit", type=int, required=True, help="Credit score (300-850)")
        parser.add_argument("--age", type=int, required=True, help="Business age in months")
        parser.add_argument("--industry", default="General Business", help="Industry")
        parser.add_argument("--monthly-revenue", type=float, help="Monthly revenue (optional)")
        parser.add_argument("--debt", type=float, help="Existing debt amount (optional)")
        parser.add_argument("--notes", help="Additional notes (optional)")

        args = parser.parse_args()

        # Validate inputs
        input_data = {
            "company_name": args.company,
            "annual_revenue": args.revenue,
            "credit_score": args.credit,
            "business_age_months": args.age
        }

        is_valid, error_msg = validate_inputs(input_data)
        if not is_valid:
            print(f"ERROR: {error_msg}", file=sys.stderr)
            sys.exit(1)

        try:
            result = qualify_mca(
                company_name=args.company,
                annual_revenue=args.revenue,
                credit_score=args.credit,
                business_age_months=args.age,
                industry=args.industry,
                monthly_revenue=args.monthly_revenue,
                existing_debt=args.debt,
                notes=args.notes
            )

            print(json.dumps(result, indent=2))

        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
