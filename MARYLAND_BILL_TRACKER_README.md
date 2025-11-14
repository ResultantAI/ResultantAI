# 🏛️ Maryland Bill Tracker - AI-Powered Legislative Monitoring

**Track Maryland state legislation with AI-powered analysis and automated monitoring.**

Monitor bills, analyze legislative impact, and stay informed about Maryland General Assembly activity with Claude AI-powered insights.

---

## 🎯 What It Does

The Maryland Bill Tracker helps you:

- **Track specific bills** by bill number (HB123, SB456, etc.)
- **Search by keywords** to find relevant legislation
- **Monitor multiple topics** simultaneously (education, healthcare, taxation, etc.)
- **Analyze bill impact** using Claude AI for comprehensive assessment
- **Filter by status** (introduced, in committee, passed, enacted)
- **Get AI insights** on stakeholder impacts, fiscal notes, and legislative strategy

Perfect for:
- 📊 **Policy Researchers** - Track legislation affecting your focus areas
- 🏢 **Business & Industry Groups** - Monitor bills impacting your sector
- 🏛️ **Government Affairs Teams** - Stay ahead of legislative changes
- 📰 **Journalists & Advocates** - Research and report on state legislation
- 🎓 **Educators & Students** - Study Maryland legislative process

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/settings/keys))

### Installation

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Basic Usage

**Track a specific bill:**
```bash
python maryland_bill_tracker.py --bill-number HB123
```

**Search by keyword:**
```bash
python maryland_bill_tracker.py --keyword "education funding"
```

**Monitor multiple keywords:**
```bash
python maryland_bill_tracker.py --keywords education healthcare transportation
```

**Search with filters:**
```bash
python maryland_bill_tracker.py --subject healthcare --status passed --session 2025
```

---

## 📋 Features & Capabilities

### 1. Bill Tracking
Track specific bills by number and get comprehensive details:
- Bill title and synopsis
- Sponsors and co-sponsors
- Current status and committee assignment
- Legislative history and timeline
- Fiscal notes (when available)
- Full text and amendments

### 2. Keyword Monitoring
Search for bills containing specific keywords:
- Search titles, synopses, and full text
- Monitor emerging legislation on topics of interest
- Track multiple keywords simultaneously
- Get alerts when new bills match criteria

### 3. AI-Powered Analysis
Claude AI provides deep analysis including:
- **Executive Summary** - Quick overview of bill purpose
- **Key Provisions** - Main components and what the bill does
- **Impact Assessment** - Who's affected and how
- **Stakeholder Analysis** - Support/opposition breakdown
- **Priority Rating** - Importance assessment (High/Medium/Low)
- **Monitoring Recommendations** - What to watch as bill progresses

### 4. Flexible Filtering
Narrow down results with multiple filters:
- **Subject Area** - Healthcare, education, taxation, environment, etc.
- **Session Year** - Current or historical sessions
- **Status** - Introduced, in committee, passed, enacted, vetoed
- **Committee** - Filter by specific committee assignments

---

## 📖 Detailed Usage

### CLI Mode

**Track a single bill:**
```bash
python maryland_bill_tracker.py --bill-number HB501 --session 2025
```

**Output:**
```json
{
  "search_criteria": {
    "session": "2025",
    "bill_number": "HB501",
    "keyword": null,
    "subject": null,
    "status": null
  },
  "bills_found": 1,
  "bills": [
    {
      "bill_number": "HB501",
      "title": "Maryland Education Funding and Innovation Act",
      "sponsors": ["Del. John Smith", "Del. Jane Doe"],
      "status": "In Committee - Education and Economic Development",
      "introduced_date": "2025-01-15",
      "synopsis": "Establishes new funding mechanisms for public schools...",
      "fiscal_note": "Estimated cost: $50M annually",
      "committee": "Education and Economic Development Committee",
      "latest_action": "Referred to committee on 2025-01-15"
    }
  ],
  "ai_analysis": {
    "executive_summary": "This bill establishes new funding mechanisms for Maryland public schools...",
    "impact_assessment": {
      "affected_parties": ["Public schools", "Teachers", "Students", "Taxpayers"],
      "benefits": ["Increased education funding", "Technology modernization"],
      "concerns": ["Fiscal impact on state budget"]
    },
    "priority_rating": "High"
  }
}
```

**Search by keyword:**
```bash
python maryland_bill_tracker.py --keyword "renewable energy" --session 2025
```

**Monitor multiple topics:**
```bash
python maryland_bill_tracker.py --keywords healthcare education transportation --session 2025
```

### Automation Mode (JSON Input)

Perfect for Make.com, Zapier, n8n, or custom automation workflows:

**Single bill tracking:**
```bash
echo '{"bill_number": "HB123", "session": "2025"}' | python maryland_bill_tracker.py
```

**Keyword monitoring:**
```bash
echo '{"keyword": "education funding"}' | python maryland_bill_tracker.py
```

**Multiple keywords:**
```bash
echo '{"keywords": ["healthcare", "education", "environment"]}' | python maryland_bill_tracker.py
```

**Advanced filtering:**
```bash
echo '{
  "keyword": "climate change",
  "subject": "environment",
  "session": "2025",
  "status": "passed"
}' | python maryland_bill_tracker.py
```

---

## 🔧 Configuration

### Environment Variables

Configure in your `.env` file:

```bash
# Required: Anthropic API Key
ANTHROPIC_API_KEY=your_api_key_here

# Optional: Model Configuration
MODEL_NAME=claude-sonnet-4-5-20250929
MAX_TOKENS=4096
REQUEST_TIMEOUT=30
```

### Command-Line Options

```
--bill-number TEXT     Specific bill number (e.g., HB123, SB456)
--keyword TEXT         Search by keyword in bill content
--keywords TEXT [...]  Monitor multiple keywords
--subject TEXT         Subject area (healthcare, education, taxation, etc.)
--session TEXT         Legislative session year (default: current year)
--status TEXT          Bill status filter (introduced, passed, enacted, etc.)
```

---

## 💡 Use Cases

### For Policy Researchers
```bash
# Monitor all healthcare-related bills
python maryland_bill_tracker.py --subject healthcare --session 2025

# Track specific policy area
python maryland_bill_tracker.py --keywords "mental health" "substance abuse" "behavioral health"
```

### For Business & Industry
```bash
# Monitor tax legislation
python maryland_bill_tracker.py --subject taxation --status introduced

# Track industry-specific bills
python maryland_bill_tracker.py --keyword "small business" --session 2025
```

### For Government Affairs Teams
```bash
# Daily monitoring automation (via cron/scheduler)
echo '{"keywords": ["transportation", "infrastructure", "transit"]}' | python maryland_bill_tracker.py > daily_report.json

# Track specific bills of interest
python maryland_bill_tracker.py --bill-number HB100 --bill-number HB200
```

### For Journalists & Advocates
```bash
# Research education funding
python maryland_bill_tracker.py --keyword "school funding" --session 2025

# Track environmental legislation
python maryland_bill_tracker.py --subject environment --keywords "climate" "renewable" "emissions"
```

---

## 🔄 Integration with Make.com

The Maryland Bill Tracker is designed to work seamlessly with Make.com automation scenarios:

### Example Scenario: Daily Legislative Alert

1. **Schedule Trigger** - Run daily at 9 AM
2. **HTTP Module** - Call Python script with keywords
3. **Filter** - Only continue if new bills found
4. **AI Analysis** - Parse Claude's impact assessment
5. **Email/Slack** - Send formatted alert to team
6. **Airtable/Sheets** - Log bills to tracking database

### Example Webhook Input (Make.com)

```json
{
  "keywords": ["education", "healthcare", "transportation"],
  "session": "2025",
  "status": "introduced"
}
```

---

## 📊 Output Format

### Standard Output Structure

```json
{
  "search_criteria": {
    "session": "2025",
    "bill_number": null,
    "keyword": "education",
    "subject": null,
    "status": null
  },
  "bills_found": 2,
  "bills": [
    {
      "bill_number": "HB101",
      "title": "Public School Education Enhancement Act",
      "sponsors": ["Del. Sarah Johnson"],
      "status": "Passed House, In Senate",
      "introduced_date": "2025-01-10",
      "synopsis": "Legislation addressing education in Maryland public schools.",
      "committee": "Senate Education Committee",
      "latest_action": "Passed House 98-42 on 2025-02-20"
    }
  ],
  "ai_analysis": {
    "executive_summary": "...",
    "key_provisions": [...],
    "impact_assessment": {
      "affected_parties": [...],
      "benefits": [...],
      "concerns": [...]
    },
    "stakeholder_analysis": {...},
    "priority_rating": "High",
    "monitoring_recommendations": [...]
  },
  "timestamp": "2025-11-14T12:30:00",
  "session": "2025"
}
```

---

## 🛠️ Technical Details

### Data Sources

The tracker integrates with:
- **Maryland General Assembly** - Official legislative data
- **LeGIS System** - Maryland's legislative information system
- **Claude AI** - Impact analysis and insights

**Note:** Current version includes demo data for demonstration purposes. Production deployment requires integration with Maryland's official API or web scraping infrastructure.

### Technology Stack

- **Python 3.8+** - Core language
- **Anthropic Claude API** - AI analysis
- **BeautifulSoup4** - Web scraping (for MGA website)
- **Requests** - HTTP client
- **python-dotenv** - Configuration management

### Error Handling

The tool includes robust error handling for:
- API failures (graceful degradation)
- Invalid input validation
- Network timeouts
- Malformed JSON responses

---

## 🚧 Roadmap & Future Enhancements

### Planned Features

| Status | Feature | Description |
|--------|---------|-------------|
| 🚧 | **Live MGA Integration** | Real-time data from Maryland General Assembly API |
| 🚧 | **Bill Text Analysis** | AI analysis of full bill text and amendments |
| 🔜 | **Status Change Alerts** | Notify when tracked bills change status |
| 🔜 | **Voting Records** | Track legislator voting patterns |
| 🔜 | **Historical Analysis** | Compare bills across multiple sessions |
| 🔜 | **Make.com Blueprint** | Pre-built automation scenario |
| 🔜 | **Web Dashboard** | Visual interface for bill tracking |
| 🔜 | **Email Digests** | Automated daily/weekly summaries |

**Legend:** ✅ Live | 🚧 In Progress | 🔜 Planned

### Contributing

Want to help build these features? See the main [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 🐛 Troubleshooting

### Common Issues

**"ANTHROPIC_API_KEY environment variable not set"**
- Create `.env` file with your API key
- Ensure `.env` is in the same directory as the script

**"No bills found matching criteria"**
- Verify search parameters (bill numbers, keywords)
- Check that session year is correct
- Try broader search terms

**API timeout errors**
- Increase `REQUEST_TIMEOUT` in `.env`
- Check internet connection
- Verify Anthropic API is accessible

**Invalid JSON input (automation mode)**
- Validate JSON syntax with `jq` or online validator
- Ensure proper escaping of special characters
- Check stdin piping is working correctly

---

## 📚 Related Resources

### Maryland Legislative Resources
- [Maryland General Assembly](https://mgaleg.maryland.gov) - Official website
- [Bill Search](https://mgaleg.maryland.gov/mgawebsite/Search/Legislation) - Search current bills
- [Committee Rosters](https://mgaleg.maryland.gov/mgawebsite/Committees) - View committees
- [Session Calendar](https://mgaleg.maryland.gov/mgawebsite/Calendar) - Legislative schedule

### ResultantAI Tools
- [Lead Enrichment](LEAD_ENRICHMENT_README.md) - AI-powered lead qualification
- [Marketing Audit](MARKETING_AUDIT_README.md) - Marketing analysis engine
- [MCA Qualification](MCA_QUALIFICATION_README.md) - Business financing assessment

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 💬 Support

- 📖 **Documentation:** This README and [main README](README.md)
- 🐛 **Report Issues:** [GitHub Issues](../../issues)
- 💡 **Feature Requests:** [Open a discussion](../../discussions)
- 📧 **Email:** [Contact ResultantAI](mailto:support@resultantai.com)

---

**Built with ❤️ by ResultantAI** | **Powered by Claude AI** | **MIT Licensed**

*Bringing AI-powered transparency to Maryland state legislation.*
