# MCA Qualification & Underwriting System

An automated underwriting tool that evaluates business eligibility for Merchant Cash Advances (MCA). Provides instant qualification decisions, calculates advance amounts, determines factor rates, and generates detailed approval/rejection reasoning.

## Features

- **Automated Underwriting**: Instant qualification decisions based on configurable criteria
- **Smart Pricing**: Dynamic factor rate calculation based on risk profile
- **Advance Calculation**: Determines appropriate advance amounts based on revenue and risk
- **Detailed Reasoning**: Transparent approval/rejection reasons with improvement recommendations
- **Make.com Ready**: JSON input/output for automation workflows
- **Compliance-Friendly**: Built-in scoring transparency and APR calculations

## What It Evaluates

### Business Inputs
- **Monthly Revenue**: Average monthly business revenue
- **Time in Business**: Months of operating history
- **Credit Score**: Business credit score (500-850)
- **Industry**: Business industry/vertical

### Qualification Criteria (100-point scoring system)

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| **Monthly Revenue** | 40 pts | Revenue strength and advance capacity |
| **Credit Score** | 25 pts | Creditworthiness and payment history |
| **Time in Business** | 20 pts | Business stability and longevity |
| **Industry** | 15 pts | Industry risk profile and default rates |

### Approval Tiers

- **Premium (Score 85+)**: Best terms, 1.15 factor rate
- **Standard (Score 70-84)**: Good terms, 1.25 factor rate
- **Subprime (Score 50-69)**: Higher cost, 1.35 factor rate
- **Declined (Score <50)**: Does not qualify

## Minimum Requirements

To qualify for any MCA:
- Monthly Revenue: $10,000+
- Time in Business: 6+ months
- Credit Score: 500+

Applications below these thresholds are automatically declined.

## How Factor Rates Work

Factor rates determine the total repayment amount:

```
Total Repayment = Advance Amount × Factor Rate
```

**Example:**
- Advance: $50,000
- Factor Rate: 1.25
- Total Repayment: $62,500
- Cost: $12,500 (25%)

## Installation

### Prerequisites
- Python 3.8+
- Existing virtual environment (from marketing audit/lead enrichment)

### Setup

```bash
# Activate existing virtual environment
source venv/bin/activate

# No additional dependencies needed
# (uses same stack as other demo tools)
```

## Usage

### Command Line Mode

Basic qualification:
```bash
python mca_qualification.py \
  --revenue 50000 \
  --time-in-business 24 \
  --credit-score 650 \
  --industry "Restaurant"
```

Save to file:
```bash
python mca_qualification.py \
  --revenue 100000 \
  --time-in-business 36 \
  --credit-score 720 \
  --industry "Technology" > approval.json
```

### Make.com Webhook Mode

Perfect for automated underwriting workflows:

```bash
echo '{
  "monthly_revenue": 50000,
  "time_in_business_months": 24,
  "credit_score": 650,
  "industry": "Restaurant"
}' | python mca_qualification.py > result.json
```

### Example JSON Input

```json
{
  "monthly_revenue": 75000,
  "time_in_business_months": 18,
  "credit_score": 680,
  "industry": "E-commerce"
}
```

## Output Format

### Approved Application

```json
{
  "qualification_metadata": {
    "timestamp": "2025-11-13T12:00:00Z",
    "business_details": {
      "monthly_revenue": 75000,
      "time_in_business_months": 18,
      "credit_score": 680,
      "industry": "E-commerce"
    }
  },
  "qualification_score": {
    "total_score": 77.6,
    "max_score": 100,
    "grade": "B",
    "score_breakdown": {
      "revenue": {
        "score": 34.0,
        "max_points": 40,
        "tier": "tier_2",
        "reasoning": "Monthly revenue of $75,000 falls in tier_2"
      },
      "credit": {
        "score": 22.5,
        "max_points": 25,
        "tier": "good",
        "reasoning": "Credit score of 680 is good"
      },
      "time_in_business": {
        "score": 14.0,
        "max_points": 20,
        "tier": "growing",
        "reasoning": "18 months in business (growing)"
      },
      "industry": {
        "score": 12.0,
        "max_points": 15,
        "risk_level": "medium_risk",
        "reasoning": "E-commerce is Moderate-risk industries"
      }
    }
  },
  "decision": {
    "status": "APPROVED",
    "decision": "approved",
    "approval_tier": "Standard",
    "confidence_level": "Medium-High",
    "approval_reasons": [
      "Strong monthly revenue of $75,000",
      "Good credit profile (score: 680)",
      "Established business (18 months)"
    ],
    "conditions": [
      "Standard approval - no additional conditions"
    ]
  },
  "offer_details": {
    "advance_amount": 150000.00,
    "factor_rate": 1.250,
    "total_repayment": 187500.00,
    "recommended_term_months": 6,
    "daily_payment": 1420.45,
    "effective_apr": 50.00,
    "calculation_details": {
      "base_advance_percentage": 200,
      "time_in_business_multiplier": 1.0,
      "base_factor_rate": 1.250,
      "credit_adjustment": 0.000,
      "industry_adjustment": 0.000
    }
  }
}
```

### Rejected Application

```json
{
  "qualification_metadata": { },
  "qualification_score": {
    "total_score": 32.6,
    "grade": "D"
  },
  "decision": {
    "status": "REJECTED",
    "decision": "declined",
    "primary_reason": "Qualification score 32.6/100 (Grade D) below approval threshold",
    "rejection_reasons": [
      "Low monthly revenue: $15,000",
      "Below-average credit score: 540",
      "Limited operating history: 8 months"
    ],
    "recommendations": [
      "Increase monthly revenue to $50,000+ for better terms",
      "Improve credit score to 650+ through consistent payment history",
      "Build longer operating history (12+ months preferred)",
      "Reapply in 3-6 months with improved financials"
    ]
  }
}
```

## Customizing Qualification Criteria

Edit `mca_criteria.json` to customize underwriting rules:

### Adjust Minimum Requirements

```json
{
  "minimum_requirements": {
    "monthly_revenue": 15000,     // Increase minimum
    "time_in_business_months": 12, // Require more history
    "credit_score": 550            // Adjust credit threshold
  }
}
```

### Modify Revenue Tiers

```json
{
  "revenue_tiers": {
    "tier_1": {
      "min": 150000,              // Higher threshold
      "max_advance_percentage": 300  // More aggressive advance
    }
  }
}
```

### Adjust Factor Rates

```json
{
  "base_factor_rates": {
    "premium": {
      "min_score": 85,
      "factor_rate": 1.12,  // More competitive pricing
      "description": "Premium terms"
    }
  }
}
```

### Industry-Specific Adjustments

```json
{
  "industry_risk_factors": {
    "low_risk": {
      "industries": ["Healthcare", "SaaS", "Legal Services"],
      "factor_rate_adjustment": -0.03  // Better rates
    }
  }
}
```

## Example Use Cases

### 1. Strong Approval (Technology Company)

**Input:**
```bash
python mca_qualification.py \
  --revenue 120000 \
  --time-in-business 48 \
  --credit-score 740 \
  --industry "Technology"
```

**Expected Result:**
- Status: APPROVED
- Score: 95/100 (Grade A)
- Tier: Premium
- Advance: ~$360,000
- Factor Rate: ~1.12

### 2. Standard Approval (Retail Business)

**Input:**
```bash
python mca_qualification.py \
  --revenue 60000 \
  --time-in-business 20 \
  --credit-score 670 \
  --industry "Retail"
```

**Expected Result:**
- Status: APPROVED
- Score: 73/100 (Grade B)
- Tier: Standard
- Advance: ~$132,000
- Factor Rate: ~1.25

### 3. Subprime Approval (Restaurant)

**Input:**
```bash
python mca_qualification.py \
  --revenue 30000 \
  --time-in-business 10 \
  --credit-score 580 \
  --industry "Restaurant"
```

**Expected Result:**
- Status: APPROVED
- Score: 52/100 (Grade C)
- Tier: Subprime
- Advance: ~$36,000
- Factor Rate: ~1.48

### 4. Rejection (Insufficient Revenue)

**Input:**
```bash
python mca_qualification.py \
  --revenue 8000 \
  --time-in-business 4 \
  --credit-score 520 \
  --industry "Salon"
```

**Expected Result:**
- Status: REJECTED
- Reason: Below minimum requirements
- Recommendations provided

## Make.com Integration

### Automated Underwriting Workflow

**Scenario Setup:**
1. **HTTP Webhook** → Receives application data
2. **JSON Parser** → Extracts business details
3. **Execute Command** → Runs `mca_qualification.py`
4. **Router** filters by decision status:
   - **APPROVED** → Route to:
     - Update CRM with offer details
     - Send approval email with terms
     - Generate contract for DocuSign
     - Notify underwriting team
   - **REJECTED** → Route to:
     - Update CRM with decline reason
     - Send rejection email with recommendations
     - Schedule follow-up task in 90 days

**Sample Webhook Payload:**
```json
{
  "application_id": "APP-12345",
  "monthly_revenue": 65000,
  "time_in_business_months": 22,
  "credit_score": 695,
  "industry": "E-commerce",
  "business_name": "Example LLC",
  "contact_email": "owner@example.com"
}
```

### Advanced Routing Logic

**Premium Approvals (Score 85+):**
- Auto-approve up to $250k
- Send contract immediately
- Assign to senior account manager

**Standard Approvals (Score 70-84):**
- Require bank statement review
- Send conditional approval
- Queue for underwriter review

**Subprime Approvals (Score 50-69):**
- Additional documentation required
- Manual underwriter approval
- Higher scrutiny process

## Compliance & Transparency

### APR Disclosure
The system calculates effective APR for transparency:
```python
effective_apr = ((factor_rate - 1.0) / term_months) * 12 * 100
```

### Reasoning Transparency
Every decision includes:
- Detailed score breakdown
- Specific approval/rejection reasons
- Improvement recommendations
- Clear calculation methodology

### Risk-Based Pricing
Factor rates adjust based on:
- Overall qualification score
- Credit score tier
- Industry risk level
- Time in business

## Performance Metrics

Track these KPIs for underwriting quality:

- **Approval Rate**: % of applications approved
- **Average Advance**: Mean advance amount
- **Average Factor Rate**: Mean pricing
- **Score Distribution**: Distribution across tiers
- **Industry Performance**: Approval rates by vertical

## Advanced Features

### Batch Processing

Process multiple applications:
```bash
while IFS=, read -r revenue months credit industry; do
  python mca_qualification.py \
    --revenue "$revenue" \
    --time-in-business "$months" \
    --credit-score "$credit" \
    --industry "$industry" > "results/${industry}_${credit}.json"
done < applications.csv
```

### Custom Risk Models

Extend the scoring with custom factors:
- Bank balance requirements
- Industry-specific metrics
- Seasonal adjustments
- Geographic risk factors

## Troubleshooting

### "Below minimum requirements"
Check that all inputs meet absolute minimums in `mca_criteria.json`

### Unexpected factor rates
Review `credit_adjustment` and `industry_adjustment` in output calculation details

### Low qualification scores
Check score breakdown to identify weak areas (revenue, credit, time, industry)

## Roadmap

- [ ] Bank statement analysis integration
- [ ] Historical default rate tracking
- [ ] A/B testing for approval criteria
- [ ] Integration with credit bureaus
- [ ] Automated funding workflow
- [ ] Portfolio performance analytics
- [ ] Seasonal adjustment factors

## Legal Disclaimer

**IMPORTANT**: This tool is for demonstration purposes only.

- Consult legal counsel before using for actual lending
- Ensure compliance with state and federal lending regulations
- Implement proper KYC/AML procedures
- Maintain proper licensing for MCA operations
- Follow Truth in Lending Act (TILA) disclosure requirements

## Support

For questions or customization:
1. Review `mca_criteria.json` for configuration options
2. Check score breakdown in output for qualification logic
3. Verify input data format matches requirements

---

**Demo Tool** | **Make.com Compatible** | **Configurable Underwriting Logic**
