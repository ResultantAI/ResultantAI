# MCA Qualification System

An AI-powered Merchant Cash Advance (MCA) qualification tool that evaluates business loan applications using Claude AI. Provides instant APPROVED/REJECTED decisions with detailed risk assessment, recommended advance amounts, and compliance documentation.

## Features

- **AI-Powered Underwriting**: Uses Claude to analyze applications against qualification criteria
- **Instant Decisions**: APPROVED or REJECTED with detailed reasoning
- **Risk Assessment**: Low/Medium/High risk classification
- **Smart Advance Calculation**: Recommended amounts based on revenue and risk profile
- **Compliance Ready**: Detailed decision factors for audit trails
- **Data Validation**: Comprehensive input validation before processing
- **Make.com Compatible**: JSON stdin/stdout for automation workflows
- **CLI Interface**: Command-line mode for testing and manual qualification

## What Gets Evaluated

### Financial Metrics
- Annual revenue (minimum: $100,000)
- Monthly revenue patterns
- Credit score (minimum: 500)
- Existing debt burden
- Debt-to-revenue ratio

### Business Stability
- Business age (minimum: 6 months)
- Industry risk assessment
- Growth trajectory
- Revenue consistency

### Qualification Criteria
- **Minimum Revenue**: $100,000/year
- **Minimum Credit Score**: 500 (300-850 scale)
- **Minimum Business Age**: 6 months
- **Maximum Debt Ratio**: 50% (existing debt / annual revenue)

### Decision Factors
The AI analyzes and documents:
1. **Revenue Assessment**: Strength and sustainability of revenue
2. **Credit Assessment**: Credit profile and payment history indicators
3. **Business Stability**: Age, consistency, and operational maturity
4. **Industry Risk**: Industry-specific risks and opportunities
5. **Debt Burden**: Impact of existing debt on repayment capacity

## Installation

### Prerequisites
- Python 3.8 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/settings/keys))
- Virtual environment (recommended)

### Setup Steps

1. **Ensure dependencies are installed** (shared with other tools in this repo)
   ```bash
   source venv/bin/activate  # Activate existing venv
   # Dependencies are shared with marketing_audit.py and lead_enrichment.py
   ```

2. **Verify .env configuration** (should already exist)
   ```bash
   # .env should contain ANTHROPIC_API_KEY
   cat .env
   ```

3. **Make script executable** (optional, Linux/Mac)
   ```bash
   chmod +x mca_qualification.py
   ```

## Usage

### Command Line Mode

Basic qualification:
```bash
python mca_qualification.py \
  --company "Tech Startup Inc" \
  --revenue 500000 \
  --credit 680 \
  --age 24 \
  --industry "Technology"
```

With optional parameters:
```bash
python mca_qualification.py \
  --company "E-commerce Co" \
  --revenue 750000 \
  --credit 720 \
  --age 36 \
  --industry "E-commerce" \
  --monthly-revenue 65000 \
  --debt 100000 \
  --notes "Strong seasonal revenue pattern"
```

Save to file:
```bash
python mca_qualification.py \
  --company "Example Corp" \
  --revenue 300000 \
  --credit 650 \
  --age 18 > qualification_result.json
```

### Make.com Webhook Mode

Perfect for automation workflows:

```bash
echo '{
  "company_name": "Tech Startup Inc",
  "annual_revenue": 500000,
  "credit_score": 680,
  "business_age_months": 24,
  "industry": "Technology"
}' | python mca_qualification.py > output.json
```

With optional fields:
```bash
echo '{
  "company_name": "Example Corp",
  "annual_revenue": 300000,
  "credit_score": 650,
  "business_age_months": 18,
  "industry": "Retail",
  "monthly_revenue": 27000,
  "existing_debt": 50000,
  "notes": "Applying for expansion capital"
}' | python mca_qualification.py
```

### Make.com Integration

**Scenario Setup:**
1. HTTP Webhook trigger to receive application data
2. Execute Command module running `mca_qualification.py`
3. JSON Parser to extract decision and details
4. Router with filters based on `decision`:
   - APPROVED → Send to underwriter queue + applicant approval email
   - REJECTED → Log rejection + send constructive rejection email
5. Google Sheets logging for compliance

**Sample Webhook Payload:**
```json
{
  "company_name": "Tech Startup Inc",
  "annual_revenue": 500000,
  "credit_score": 680,
  "business_age_months": 24,
  "industry": "Technology",
  "existing_debt": 50000,
  "applicant_email": "owner@techstartup.com",
  "application_id": "MCA-2025-001"
}
```

## Output Format

### APPROVED Application Example

```json
{
  "qualification_metadata": {
    "timestamp": "2025-11-13T12:00:00Z",
    "company_name": "Tech Startup Inc",
    "industry": "Technology",
    "model_used": "claude-sonnet-4-5-20250929"
  },
  "application_data": {
    "annual_revenue": 500000,
    "monthly_revenue_avg": 41666.67,
    "credit_score": 680,
    "business_age_months": 24,
    "existing_debt": 50000,
    "debt_to_revenue_ratio": 10.0
  },
  "qualification_result": {
    "decision": "APPROVED",
    "risk_level": "medium",
    "recommended_advance_amount": {
      "min": 50000,
      "max": 125000,
      "recommended": 75000
    },
    "factor_payback_rate": 1.25,
    "estimated_payback_months": 12,
    "decision_factors": {
      "revenue_assessment": "Strong revenue base at $500K annually with consistent performance",
      "credit_assessment": "Good credit profile at 680, demonstrates responsible financial management",
      "business_stability": "Established 2-year track record shows operational maturity",
      "industry_risk": "Technology sector has moderate risk with strong growth potential",
      "debt_burden": "Low debt ratio at 10% provides comfortable repayment capacity"
    },
    "approval_conditions": [
      "Verify last 6 months of bank statements",
      "Confirm no recent payment defaults"
    ],
    "red_flags": [],
    "underwriter_notes": "Strong candidate with solid financials and manageable debt. Recommended advance at 15% of annual revenue to ensure comfortable repayment."
  },
  "compliance_log": {
    "minimum_thresholds_met": {
      "revenue": true,
      "credit_score": true,
      "business_age": true
    },
    "decision_timestamp": "2025-11-13T12:00:00Z",
    "model_version": "claude-sonnet-4-5-20250929"
  }
}
```

### REJECTED Application Example

```json
{
  "qualification_metadata": {
    "timestamp": "2025-11-13T12:00:00Z",
    "company_name": "New Business",
    "industry": "Retail",
    "model_used": "claude-sonnet-4-5-20250929"
  },
  "application_data": {
    "annual_revenue": 50000,
    "monthly_revenue_avg": 4166.67,
    "credit_score": 450,
    "business_age_months": 3,
    "existing_debt": 0,
    "debt_to_revenue_ratio": 0
  },
  "qualification_result": {
    "decision": "REJECTED",
    "risk_level": "high",
    "recommended_advance_amount": {
      "min": 0,
      "max": 0,
      "recommended": 0
    },
    "factor_payback_rate": 0,
    "estimated_payback_months": 0,
    "decision_factors": {
      "revenue_assessment": "Revenue of $50K is below minimum threshold of $100K annually",
      "credit_assessment": "Credit score of 450 is below minimum requirement of 500",
      "business_stability": "Only 3 months in operation, need minimum 6 months track record",
      "industry_risk": "Retail sector carries higher risk for new businesses",
      "debt_burden": "No existing debt burden (positive)"
    },
    "approval_conditions": [],
    "red_flags": [
      "Revenue significantly below minimum threshold",
      "Credit score below acceptable range",
      "Insufficient business operating history"
    ],
    "underwriter_notes": "Application does not meet minimum qualification criteria. Recommend reapplication after 6 months of operation with improved revenue and credit profile."
  },
  "compliance_log": {
    "minimum_thresholds_met": {
      "revenue": false,
      "credit_score": false,
      "business_age": false
    },
    "decision_timestamp": "2025-11-13T12:00:00Z",
    "model_version": "claude-sonnet-4-5-20250929"
  }
}
```

## Qualification Thresholds

### Configurable Minimums
Edit script constants or pass via environment variables:

```python
MIN_REVENUE = 100000        # $100K annual revenue
MIN_CREDIT_SCORE = 500      # FICO score
MIN_BUSINESS_AGE_MONTHS = 6 # 6 months operating history
```

### Advance Amount Guidelines
- **Conservative**: 10-20% of annual revenue
- **Moderate**: 20-35% of annual revenue
- **Aggressive**: 35-50% of annual revenue

Actual amounts determined by AI based on:
- Revenue strength and consistency
- Credit profile
- Business age and stability
- Industry risk factors
- Existing debt burden

### Factor Rates
- **Low Risk**: 1.15 - 1.20x
- **Medium Risk**: 1.20 - 1.30x
- **High Risk**: 1.30 - 1.35x

### Payback Periods
- **Short Term**: 6-9 months
- **Standard**: 9-15 months
- **Extended**: 15-18 months

## Example Use Cases

### 1. Manual Application Review
```bash
# Qualify a single application
python mca_qualification.py \
  --company "Restaurant LLC" \
  --revenue 400000 \
  --credit 600 \
  --age 36 \
  --industry "Food Service" \
  --debt 75000

# Review output and make decision
```

### 2. Batch Processing
```bash
# Qualify multiple applications from CSV
while IFS=, read -r company revenue credit age industry; do
  python mca_qualification.py \
    --company "$company" \
    --revenue "$revenue" \
    --credit "$credit" \
    --age "$age" \
    --industry "$industry" > "qualifications/${company// /_}.json"
done < applications.csv
```

### 3. Webhook Integration
```bash
# Receive application via webhook and qualify
curl -X POST https://your-webhook-endpoint.com/mca-qualify \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Tech Co",
    "annual_revenue": 600000,
    "credit_score": 700,
    "business_age_months": 30,
    "industry": "Technology"
  }'
```

## Demo Examples

### Example 1: Strong Approval
```bash
python mca_qualification.py \
  --company "Established Tech Co" \
  --revenue 1200000 \
  --credit 750 \
  --age 48 \
  --industry "Software"
# Expected: APPROVED, Low Risk, $180K-$300K advance
```

### Example 2: Borderline Approval
```bash
python mca_qualification.py \
  --company "Growing Retail" \
  --revenue 180000 \
  --credit 550 \
  --age 12 \
  --industry "Retail"
# Expected: APPROVED, Medium-High Risk, $27K-$54K advance
```

### Example 3: Rejection - Low Revenue
```bash
python mca_qualification.py \
  --company "New Startup" \
  --revenue 75000 \
  --credit 680 \
  --age 8 \
  --industry "Services"
# Expected: REJECTED, Revenue below minimum
```

### Example 4: Rejection - Low Credit
```bash
python mca_qualification.py \
  --company "Struggling Business" \
  --revenue 300000 \
  --credit 420 \
  --age 24 \
  --industry "Construction"
# Expected: REJECTED, Credit score below minimum
```

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
Ensure `.env` file exists with your API key (shared with other tools in this repo).

### "Invalid revenue format"
Revenue must be a positive number. Use digits only, no commas or dollar signs:
```bash
--revenue 500000  # Correct
--revenue $500,000  # Incorrect
```

### "Credit score must be between 300 and 850"
Provide a valid FICO credit score in the 300-850 range.

### "Business age cannot be negative"
Provide business age in months as a positive integer.

### Unexpected rejections
Check that your application meets minimum thresholds:
- Revenue ≥ $100,000
- Credit score ≥ 500
- Business age ≥ 6 months
- Debt ratio < 50%

## Advanced Configuration

### Custom Thresholds
Set environment variables to override defaults:
```bash
export MIN_REVENUE=150000
export MIN_CREDIT_SCORE=550
export MIN_BUSINESS_AGE_MONTHS=12

python mca_qualification.py --company "Test Co" --revenue 160000 --credit 560 --age 13
```

### Adjusting API Timeout
Edit `.env`:
```
REQUEST_TIMEOUT=90  # Increase for slower API responses
```

### Custom Model Selection
Edit `.env`:
```
MODEL_NAME=claude-sonnet-4-5-20250929  # Latest model
MAX_TOKENS=4096  # Response length
```

## Integration Ideas

- **Lending Platform**: Automate pre-qualification for applications
- **CRM Integration**: Qualify leads before sales outreach
- **Financial Dashboard**: Build approval/rejection analytics
- **Email Automation**: Send decision letters automatically
- **Compliance System**: Archive decisions for regulatory review
- **Risk Management**: Track approval rates and default correlation
- **Underwriter Queue**: Route approved applications to human reviewers

## Compliance & Regulations

### Fair Lending Practices
This tool provides objective, AI-based analysis of financial metrics. The AI:
- Does not discriminate based on protected characteristics
- Applies consistent criteria to all applications
- Documents all decision factors transparently
- Provides clear reasoning for decisions

### Audit Trail
The compliance_log section provides:
- Threshold verification (which criteria were met)
- Decision timestamp
- AI model version used
- Complete decision factor documentation

### Recommended Practices
1. **Human Review**: Use AI as a pre-qualification tool, not final authority
2. **Documentation**: Save all qualification outputs for audit trails
3. **Disclosure**: Inform applicants that AI assists in qualification
4. **Appeals Process**: Allow manual review of borderline cases
5. **Regular Audits**: Review approval/rejection patterns quarterly

## Performance Tips

1. **Batch Processing**: Qualify multiple applications in parallel
2. **Cache Results**: Store qualifications to avoid re-processing
3. **Webhooks**: Use event-driven architecture for real-time qualification
4. **Database Integration**: Store results in database for analytics

## Roadmap

- [ ] Multi-factor authentication for sensitive data
- [ ] Historical trend analysis (compare to previous applications)
- [ ] Industry benchmarking (compare to similar businesses)
- [ ] Seasonal adjustment factors
- [ ] Integration with credit bureaus (Experian, Equifax, TransUnion)
- [ ] Bank statement analysis integration
- [ ] Fraud detection capabilities
- [ ] White-label API for lending platforms

## Support

For issues or questions:
1. Check this README
2. Verify `.env` has valid API key
3. Ensure all required parameters are provided
4. Review error messages (they're descriptive!)
5. Test with demo examples to verify setup

---

**Built with Claude AI** | **Make.com Compatible** | **Compliance-Ready** | **Production-Grade**
