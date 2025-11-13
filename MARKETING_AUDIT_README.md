# Marketing Audit System

A production-ready Python tool that generates comprehensive marketing audits using Claude AI. Perfect for agencies, consultants, and businesses looking to automate marketing assessments.

## Features

- **Comprehensive Analysis**: Audits SEO, content strategy, social media, and paid advertising opportunities
- **AI-Powered**: Uses Anthropic's Claude for intelligent, context-aware recommendations
- **Dual Input Mode**: Works as CLI tool or with JSON input for Make.com/automation workflows
- **Production-Ready**: Robust error handling, modular design, clean JSON output
- **Quick Wins**: Automatically identifies top 3 actionable recommendations prioritized by impact/effort

## What It Analyzes

### 1. SEO Analysis
- Title tags and meta descriptions
- Header tag structure (H1, H2)
- Page load time and performance
- Technical SEO issues

### 2. Content Strategy
- Messaging clarity and effectiveness
- Blog quality and consistency
- Call-to-action (CTA) effectiveness
- Content gaps and opportunities

### 3. Social Media Presence
- Platform detection and coverage
- Engagement quality assessment
- Platform-specific recommendations

### 4. Paid Advertising Potential
- Google Ads opportunities and keywords
- Social media advertising potential (Facebook, LinkedIn, etc.)
- Budget allocation recommendations

### 5. Quick Wins
- Top 3 actionable recommendations
- Impact vs. effort analysis
- Expected outcomes for each action

## Installation

### Prerequisites
- Python 3.8 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/settings/keys))

### Setup Steps

1. **Clone or download this repository**
   ```bash
   cd ResultantAI
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

5. **Make the script executable** (optional, Linux/Mac)
   ```bash
   chmod +x marketing_audit.py
   ```

## Usage

### Command Line Mode

Basic usage:
```bash
python marketing_audit.py --url https://example.com --industry "SaaS"
```

The script will output JSON to stdout and progress messages to stderr.

To save the output to a file:
```bash
python marketing_audit.py --url https://example.com --industry "E-commerce" > audit_report.json
```

### Make.com Webhook Mode

The script can read JSON input from stdin, making it perfect for automation workflows:

```bash
echo '{"url": "https://example.com", "industry": "Healthcare"}' | python marketing_audit.py > output.json
```

In Make.com:
1. Use an HTTP module to trigger the scenario
2. Pass JSON with `url` and `industry` fields
3. Use an Execute Command module or webhook to run the script
4. Parse the JSON output for further processing

### Example JSON Input

```json
{
  "url": "https://example.com",
  "industry": "SaaS"
}
```

## Output Format

The script outputs structured JSON with the following format:

```json
{
  "audit_metadata": {
    "timestamp": "2025-01-15T10:30:00Z",
    "company_url": "https://example.com",
    "industry": "SaaS",
    "model_used": "claude-sonnet-4-5-20250929"
  },
  "findings": {
    "seo_analysis": {
      "score": 7,
      "findings": ["Finding 1", "Finding 2"],
      "issues": ["Issue 1", "Issue 2"]
    },
    "content_strategy": {
      "score": 6,
      "messaging_clarity": "Assessment text",
      "blog_quality": "Assessment text",
      "cta_effectiveness": "Assessment text",
      "findings": ["Finding 1", "Finding 2"]
    },
    "social_media_presence": {
      "score": 5,
      "platforms_detected": ["LinkedIn", "Twitter"],
      "engagement_quality": "Assessment text",
      "recommendations": ["Rec 1", "Rec 2"]
    },
    "paid_advertising": {
      "google_ads_potential": {
        "score": 8,
        "rationale": "Explanation",
        "recommended_keywords": ["keyword1", "keyword2"]
      },
      "social_ads_potential": {
        "score": 7,
        "platforms": ["Facebook", "LinkedIn"],
        "rationale": "Explanation"
      }
    },
    "quick_wins": [
      {
        "title": "Quick Win 1",
        "impact": "high",
        "effort": "low",
        "description": "Detailed description",
        "expected_outcome": "What this will achieve"
      }
    ],
    "overall_assessment": {
      "overall_score": 7,
      "strengths": ["Strength 1", "Strength 2"],
      "weaknesses": ["Weakness 1", "Weakness 2"],
      "priority_actions": ["Action 1", "Action 2", "Action 3"]
    }
  }
}
```

## Configuration

Edit `.env` to customize:

- `ANTHROPIC_API_KEY`: Your API key (required)
- `MODEL_NAME`: Claude model to use (default: claude-sonnet-4-5-20250929)
- `MAX_TOKENS`: Maximum response length (default: 4096)
- `REQUEST_TIMEOUT`: Website fetch timeout in seconds (default: 30)

## Error Handling

The script includes robust error handling for:
- Invalid URLs or unreachable websites
- API errors and rate limits
- Malformed input
- Network timeouts

Progress messages go to stderr, JSON output to stdout (making it easy to separate logs from data).

## Future Enhancements

The modular design makes it easy to add:
- PDF report generation
- Email delivery
- Multi-page website analysis
- Competitor comparison
- Historical audit tracking
- Custom scoring weights

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
Make sure you've created a `.env` file with your API key:
```bash
cp .env.example .env
# Edit .env and add your key
```

### "Failed to fetch website"
- Check that the URL is accessible
- Some websites block automated requests
- Try increasing `REQUEST_TIMEOUT` in .env

### Import errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Demo Script Examples

### Example 1: Tech Startup
```bash
python marketing_audit.py --url https://stripe.com --industry "FinTech"
```

### Example 2: E-commerce
```bash
python marketing_audit.py --url https://shopify.com --industry "E-commerce"
```

### Example 3: Healthcare SaaS
```bash
python marketing_audit.py --url https://zoom.us --industry "Healthcare SaaS"
```

## Support

For issues or questions:
1. Check this README
2. Review error messages (they're descriptive!)
3. Verify your API key is valid
4. Ensure dependencies are installed

## License

This tool is provided as-is for commercial and personal use.

---

**Built with Claude AI** | **Production-Ready** | **Make.com Compatible**
