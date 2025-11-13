# Lead Enrichment & Scoring System

An AI-powered lead qualification tool that enriches company data and scores leads against your Ideal Customer Profile (ICP) criteria. Perfect for sales teams, marketing automation, and lead routing workflows.

## Features

- **AI-Powered Enrichment**: Uses Claude to extract comprehensive company intelligence
- **ICP Scoring**: Automatically scores leads 1-100 based on customizable criteria
- **Clearbit-Style Data**: Company info, tech stack, employee count, funding, growth signals
- **Configurable Criteria**: JSON-based ICP configuration for easy customization
- **Make.com Ready**: Reads JSON from stdin for automation workflows
- **Actionable Output**: Lead categories (Hot/Warm/Cold/Poor Fit) with recommendations

## What Gets Enriched

### Company Profile
- Official company name and industry
- Business model (B2B/B2C/Marketplace)
- Company description and value proposition
- Headquarters location (when detectable)
- Website quality assessment

### Company Size
- Estimated employee count
- Size category (Enterprise/Mid-market/Small/Startup)
- Confidence level and reasoning

### Funding & Growth
- Funding stage (Bootstrap to Public)
- Growth indicators and expansion signals
- Hiring activity detection
- Revenue model analysis

### Technology Stack
- Confirmed technologies (React, AWS, Stripe, etc.)
- Technical sophistication level
- Infrastructure type (Cloud/Hybrid/On-premise)
- Technology compatibility score

### Market Presence
- Brand maturity level
- Content marketing activity
- SEO quality assessment
- Social media presence and activity
- Thought leadership indicators

### Business Intelligence
- Target customer profile
- Competitive positioning
- Revenue model
- Sales readiness indicators

## ICP Scoring Criteria

The system scores leads across 6 weighted dimensions (customizable in `icp_config.json`):

| Criteria | Default Weight | What It Measures |
|----------|---------------|------------------|
| **Company Size** | 20% | Employee count fit with ideal range |
| **Industry** | 15% | Match with target industries |
| **Funding Stage** | 15% | Funding maturity and budget availability |
| **Tech Stack** | 20% | Technology sophistication and compatibility |
| **Growth Signals** | 15% | Active growth indicators (hiring, expansion) |
| **Market Presence** | 15% | Brand maturity and marketing investment |

### Score Categories

- **Hot Lead (80-100)**: Priority prospects, immediate outreach
- **Warm Lead (60-79)**: Qualified fit, nurture sequence
- **Cold Lead (40-59)**: Moderate fit, long-term nurture
- **Poor Fit (0-39)**: Low priority, exclude from active outreach

## Installation

### Prerequisites
- Python 3.8 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/settings/keys))
- Virtual environment (recommended)

### Setup Steps

1. **Ensure dependencies are installed** (should already be done from marketing audit setup)
   ```bash
   source venv/bin/activate  # Activate existing venv
   # Dependencies are shared with marketing_audit.py
   ```

2. **Configure ICP criteria** (optional - defaults provided)
   ```bash
   # Edit icp_config.json to customize scoring criteria
   nano icp_config.json
   ```

3. **Ensure .env has API key** (should already exist)
   ```bash
   # .env should contain ANTHROPIC_API_KEY
   cat .env
   ```

## Usage

### Command Line Mode

Basic enrichment:
```bash
python lead_enrichment.py --domain stripe.com
```

With company name:
```bash
python lead_enrichment.py --domain example.com --company "Example Corp"
```

Save to file:
```bash
python lead_enrichment.py --domain shopify.com > shopify_lead.json
```

### Make.com Webhook Mode

Perfect for automation workflows:

```bash
echo '{"domain": "stripe.com"}' | python lead_enrichment.py > output.json
```

With company name:
```bash
echo '{"domain": "example.com", "company": "Example Corp"}' | python lead_enrichment.py
```

### Make.com Integration

**Scenario Setup:**
1. HTTP Webhook trigger to receive lead data
2. Execute Command module running `lead_enrichment.py`
3. JSON Parser to extract enrichment data and score
4. Router with filters based on `lead_category`:
   - Hot leads → Send to sales CRM + Slack notification
   - Warm leads → Add to nurture sequence
   - Cold leads → Add to long-term drip campaign
   - Poor fit → Archive or exclude

**Sample Webhook Payload:**
```json
{
  "domain": "stripe.com",
  "company": "Stripe"
}
```

## Output Format

```json
{
  "enrichment_metadata": {
    "timestamp": "2025-11-13T12:00:00Z",
    "domain": "stripe.com",
    "company_name": "Stripe",
    "model_used": "claude-sonnet-4-5-20250929"
  },
  "lead_score": 87.5,
  "lead_category": "hot_lead",
  "recommendation": "PRIORITY: High-value prospect (score: 87.5/100). Immediate outreach recommended...",
  "scoring_details": {
    "score_breakdown": {
      "company_size": {
        "raw_score": 90,
        "weighted_score": 18,
        "weight": 20,
        "value": 350,
        "reasoning": "Company size: 350"
      },
      "industry": {
        "raw_score": 100,
        "weighted_score": 15,
        "weight": 15,
        "value": "FinTech",
        "reasoning": "Industry: FinTech"
      },
      "funding_stage": {
        "raw_score": 100,
        "weighted_score": 15,
        "weight": 15,
        "value": "Series C",
        "reasoning": "Funding: Series C"
      },
      "tech_stack": {
        "raw_score": 100,
        "weighted_score": 20,
        "weight": 20,
        "value": ["React", "AWS", "Stripe"],
        "reasoning": "Tech matches: 3, Sophistication: high"
      },
      "growth_signals": {
        "raw_score": 80,
        "weighted_score": 12,
        "weight": 15,
        "value": {"is_hiring": true, "signals": 3},
        "reasoning": "Growth signals detected: 3"
      },
      "market_presence": {
        "raw_score": 85,
        "weighted_score": 12.75,
        "weight": 15,
        "value": {
          "brand_maturity": "established",
          "content_marketing": true,
          "seo_quality": "excellent",
          "social_activity": "active"
        },
        "reasoning": "Brand: established, SEO: excellent, Social: active"
      }
    },
    "category_thresholds": {
      "hot_lead": 80,
      "warm_lead": 60,
      "cold_lead": 40,
      "poor_fit": 0
    }
  },
  "enrichment_data": {
    "company_profile": { },
    "company_size": { },
    "funding_and_growth": { },
    "technology_stack": { },
    "market_presence": { },
    "business_intelligence": { },
    "contact_indicators": { }
  }
}
```

## Customizing ICP Criteria

Edit `icp_config.json` to match your ideal customer profile:

### Adjust Scoring Weights
```json
{
  "icp_criteria": {
    "company_size": {
      "weight": 30,  // Increase if size is critical
      "ideal_range": [100, 1000]  // Adjust target range
    }
  }
}
```

### Change Target Industries
```json
{
  "industry": {
    "weight": 15,
    "ideal_industries": [
      "Healthcare",
      "Education",
      "Government"
    ]
  }
}
```

### Modify Score Thresholds
```json
{
  "scoring_thresholds": {
    "hot_lead": 85,   // More selective
    "warm_lead": 70,
    "cold_lead": 50,
    "poor_fit": 0
  }
}
```

## Example Use Cases

### 1. Sales Lead Qualification
```bash
# Enrich inbound lead
python lead_enrichment.py --domain newlead.com > lead_data.json

# Parse score and route
SCORE=$(cat lead_data.json | python -c "import json, sys; print(json.load(sys.stdin)['lead_score'])")
if [ $SCORE -gt 80 ]; then
  echo "Hot lead - assign to senior rep"
fi
```

### 2. Batch Lead Scoring
```bash
# Score multiple leads from CSV
while IFS=, read -r domain company; do
  python lead_enrichment.py --domain "$domain" --company "$company" > "leads/${domain}.json"
done < leads.csv
```

### 3. CRM Integration
```bash
# Enrich and push to CRM
LEAD_DATA=$(python lead_enrichment.py --domain example.com)
curl -X POST https://crm.example.com/api/leads \
  -H "Content-Type: application/json" \
  -d "$LEAD_DATA"
```

## Demo Examples

### Example 1: FinTech Company
```bash
python lead_enrichment.py --domain stripe.com
# Expected: Hot Lead (85-95 score)
```

### Example 2: E-commerce Platform
```bash
python lead_enrichment.py --domain shopify.com
# Expected: Hot Lead (80-90 score)
```

### Example 3: Startup
```bash
python lead_enrichment.py --domain earlystartup.com
# Expected: Warm/Cold Lead (50-70 score)
```

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
Ensure `.env` file exists with your API key (shared with marketing audit system).

### "ICP config file not found"
The system will use default ICP criteria. To customize, ensure `icp_config.json` exists.

### Low scores for good leads
Adjust ICP criteria weights and ideal values in `icp_config.json` to match your actual ICP.

### Failed to fetch website
Some websites block automated requests. The system will continue with limited data when possible.

## Advanced Configuration

### Custom ICP Config Path
Set environment variable:
```bash
export ICP_CONFIG_PATH=/path/to/custom_icp.json
python lead_enrichment.py --domain example.com
```

### Adjusting API Timeout
Edit `.env`:
```
REQUEST_TIMEOUT=60  # Increase for slow websites
```

## Integration Ideas

- **CRM Auto-Enrichment**: Trigger on new lead creation
- **Marketing Automation**: Score leads before adding to campaigns
- **Sales Intelligence**: Enrich prospect lists before outreach
- **Lead Routing**: Auto-assign based on score and category
- **Account-Based Marketing**: Prioritize target accounts
- **Competitor Analysis**: Batch enrich competitor customer lists

## Performance Tips

1. **Batch Processing**: Process leads in parallel for large lists
2. **Caching**: Cache enrichment data to avoid re-enriching same companies
3. **Webhooks**: Use Make.com or Zapier for real-time enrichment
4. **Scheduling**: Run batch enrichment during off-peak hours

## Roadmap

- [ ] Company logo extraction
- [ ] LinkedIn integration for employee data
- [ ] Historical data tracking (score changes over time)
- [ ] Custom scoring formulas
- [ ] Integration with popular CRMs (Salesforce, HubSpot)
- [ ] Batch processing mode
- [ ] Web dashboard for lead review

## Support

For issues or questions:
1. Check this README
2. Review `icp_config.json` for scoring criteria
3. Verify `.env` has valid API key
4. Check error messages (they're descriptive!)

---

**Built with Claude AI** | **Make.com Compatible** | **Production-Ready**
