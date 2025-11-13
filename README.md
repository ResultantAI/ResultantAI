# 🚀 ResultantAI - Production-Ready AI Automation Tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Make.com Compatible](https://img.shields.io/badge/Make.com-Compatible-purple.svg)](https://www.make.com/)
[![Powered by Claude](https://img.shields.io/badge/Powered%20by-Claude%20AI-orange.svg)](https://www.anthropic.com/)

**Open-source AI automation tools for lead intelligence, marketing analysis, and business qualification.** Built for developers, automation engineers, and growth teams who need production-ready solutions with zero black boxes.

---

## 🎯 What's Inside

This repository contains **three production-ready automation systems** powered by Anthropic's Claude AI:

| Tool | Description | Use Case |
|------|-------------|----------|
| **[Lead Enrichment & Scoring](LEAD_ENRICHMENT_README.md)** | AI-powered lead qualification with ICP scoring | Sales automation, CRM enrichment, lead routing |
| **[Marketing Audit System](MARKETING_AUDIT_README.md)** | Comprehensive marketing analysis engine | Agency audits, SEO analysis, content strategy |
| **[MCA Qualification](MCA_QUALIFICATION_README.md)** | Business financing qualification assessment | FinTech, lending automation, risk assessment |

Each tool includes:
- ✅ **CLI & API modes** (works standalone or in automation workflows)
- ✅ **Make.com blueprints** (pre-built automation scenarios)
- ✅ **Structured JSON output** (easy integration with any system)
- ✅ **Production-ready code** (error handling, logging, modular design)
- ✅ **Detailed documentation** (setup guides, examples, troubleshooting)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/settings/keys))
- Make.com account (optional, for no-code automation)

### Installation

```bash
# Clone the repository
git clone https://github.com/ResultantAI/ResultantAI.git
cd ResultantAI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Quick Examples

**Lead Enrichment:**
```bash
python lead_enrichment.py --domain stripe.com
# Returns comprehensive company data + ICP score (0-100)
```

**Marketing Audit:**
```bash
python marketing_audit.py --url https://example.com --industry "SaaS"
# Returns SEO, content, social media, and paid advertising analysis
```

**MCA Qualification:**
```bash
echo '{"business_name": "Acme Corp", "monthly_revenue": 50000}' | python mca_qualification.py
# Returns financing qualification assessment and recommendations
```

For detailed usage, see each tool's dedicated README.

---

## 🧰 Tool Documentation

### 1. [Lead Enrichment & Scoring System](LEAD_ENRICHMENT_README.md)

**Extract comprehensive company intelligence and score leads against your ICP.**

- Clearbit-style data enrichment (company size, tech stack, funding, growth signals)
- Customizable ICP scoring (6 weighted criteria, configurable thresholds)
- Lead categorization (Hot/Warm/Cold/Poor Fit) with actionable recommendations
- Perfect for: Sales automation, CRM enrichment, lead routing, ABM

**Output includes:**
- Company profile (name, industry, business model, HQ location)
- Tech stack analysis (React, AWS, Stripe, sophistication level)
- Funding & growth signals (stage, hiring activity, expansion indicators)
- Market presence assessment (SEO, social activity, content marketing)
- ICP score (0-100) with detailed breakdown by criteria

[→ Full Documentation](LEAD_ENRICHMENT_README.md) | [→ Make.com Blueprint](make-blueprint-lead-enrichment.json)

---

### 2. [Marketing Audit System](MARKETING_AUDIT_README.md)

**Generate comprehensive marketing audits with AI-powered analysis.**

- SEO analysis (title tags, meta descriptions, headers, performance)
- Content strategy assessment (messaging, blog quality, CTAs)
- Social media presence evaluation (platform coverage, engagement)
- Paid advertising opportunities (Google Ads, social ads, keywords)
- Top 3 Quick Wins (prioritized by impact vs. effort)

**Perfect for:**
- Agency client audits
- Competitive analysis
- Marketing health checks
- Lead generation (offer free audits)

[→ Full Documentation](MARKETING_AUDIT_README.md) | [→ Make.com Blueprint](make-blueprint-marketing-audit.json)

---

### 3. [MCA Qualification System](MCA_QUALIFICATION_README.md)

**Automate business financing qualification and risk assessment.**

- Business qualification scoring
- Revenue and cash flow analysis
- Industry risk assessment
- Credit readiness evaluation
- Financing recommendations

**Perfect for:**
- FinTech platforms
- Lending automation
- Business loan pre-qualification
- Risk assessment workflows

[→ Full Documentation](MCA_QUALIFICATION_README.md) | [→ Make.com Blueprint](make-blueprint-mca-qualification.json)

---

## 🔧 Technical Architecture

### Tech Stack

- **AI Engine:** Anthropic Claude (Sonnet 4.5)
- **Language:** Python 3.8+
- **Web Scraping:** BeautifulSoup4, Requests
- **Config Management:** python-dotenv, JSON
- **Automation:** Make.com compatible (stdin/stdout JSON)

### Design Principles

1. **Modular & Extensible:** Each tool is self-contained but shares common patterns
2. **Production-Ready:** Robust error handling, logging, and timeout management
3. **Automation-First:** Works standalone (CLI) or in workflows (Make.com, Zapier, n8n)
4. **Transparent & Auditable:** Structured JSON output with detailed reasoning
5. **Zero Black Boxes:** All logic is visible, configurable, and customizable

### Integration Patterns

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Webhook   │─────>│ Python Tool  │─────>│   CRM/DB    │
│  (Make.com) │      │  (CLI/API)   │      │  (Airtable) │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            v
                    ┌──────────────┐
                    │  Claude API  │
                    │  (Analysis)  │
                    └──────────────┘
```

---

## 📦 Make.com Blueprints

Pre-built automation scenarios for instant deployment:

1. **[Lead Enrichment Blueprint](make-blueprint-lead-enrichment.json)**
   - Trigger: New lead in CRM
   - Action: Enrich with company data + ICP score
   - Route: Hot leads → Sales, Warm → Nurture, Cold → Archive

2. **[Marketing Audit Blueprint](make-blueprint-marketing-audit.json)**
   - Trigger: Form submission or webhook
   - Action: Generate comprehensive audit
   - Output: Email report + save to Google Sheets

3. **[MCA Qualification Blueprint](make-blueprint-mca-qualification.json)**
   - Trigger: Loan application received
   - Action: Assess qualification and risk
   - Route: Qualified → Sales team, Not qualified → Auto-decline

**Import Instructions:**
1. Open Make.com → Create New Scenario
2. Import JSON blueprint from this repository
3. Configure API keys and webhooks
4. Activate and test

---

## 🛠️ Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
# Required: Anthropic API Key
ANTHROPIC_API_KEY=your_api_key_here

# Optional: Model Configuration
MODEL_NAME=claude-sonnet-4-5-20250929
MAX_TOKENS=4096
REQUEST_TIMEOUT=30
```

### ICP Scoring Configuration

Customize lead scoring criteria in `icp_config.json`:

```json
{
  "icp_criteria": {
    "company_size": {
      "weight": 20,
      "ideal_range": [50, 500]
    },
    "industry": {
      "weight": 15,
      "ideal_industries": ["SaaS", "FinTech", "E-commerce"]
    }
  },
  "scoring_thresholds": {
    "hot_lead": 80,
    "warm_lead": 60,
    "cold_lead": 40
  }
}
```

See [Lead Enrichment README](LEAD_ENRICHMENT_README.md) for full configuration options.

---

## 💡 Use Cases

### For Agencies
- **Client Acquisition:** Offer free marketing audits to generate leads
- **Onboarding:** Automate initial client assessments
- **Lead Qualification:** Score and route inbound leads automatically
- **Reporting:** Generate audit reports at scale

### For Sales Teams
- **Lead Enrichment:** Enhance CRM data with AI-powered intelligence
- **Lead Scoring:** Prioritize outreach based on ICP fit (0-100 score)
- **Account Research:** Get comprehensive company profiles instantly
- **ABM Targeting:** Identify and prioritize high-value accounts

### For FinTech/Lending
- **Pre-Qualification:** Automate initial loan eligibility checks
- **Risk Assessment:** Evaluate business health and creditworthiness
- **Lead Routing:** Direct qualified leads to appropriate loan products
- **Compliance:** Maintain audit trails of qualification decisions

### For Developers
- **Build Automation:** Integrate tools into existing workflows
- **Extend & Customize:** Fork and adapt to specific business needs
- **API Integration:** Connect to CRMs, databases, and marketing tools
- **Learn AI Automation:** Study production-ready AI implementation patterns

---

## 🗺️ Roadmap

| Status | Feature | Description |
|--------|---------|-------------|
| ✅ | **Lead Enrichment v1.0** | Production-ready with ICP scoring |
| ✅ | **Marketing Audit v1.0** | Comprehensive marketing analysis |
| ✅ | **MCA Qualification v1.0** | Business financing assessment |
| ✅ | **Make.com Blueprints** | Pre-built automation scenarios |
| 🚧 | **Web Dashboard** | UI for reviewing and managing results |
| 🚧 | **Batch Processing** | Process multiple leads/audits in parallel |
| 🔜 | **CRM Integrations** | Native HubSpot, Salesforce, Pipedrive connectors |
| 🔜 | **Historical Tracking** | Track score/data changes over time |
| 🔜 | **LinkedIn Integration** | Enrich with employee and company data |
| 🔜 | **Custom AI Prompts** | User-defined analysis templates |

**Legend:** ✅ Live | 🚧 In Progress | 🔜 Planned

Want to influence the roadmap? [Open an issue](../../issues) or contribute!

---

## 📚 Documentation

- **[Lead Enrichment Guide](LEAD_ENRICHMENT_README.md)** - Full setup, usage, and configuration
- **[Marketing Audit Guide](MARKETING_AUDIT_README.md)** - Installation and examples
- **[MCA Qualification Guide](MCA_QUALIFICATION_README.md)** - Business assessment docs
- **[Make.com Blueprints](MAKE_BLUEPRINTS_README.md)** - Automation scenario guides

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Quick Contributions
- 🐛 **Report bugs:** [Open an issue](../../issues)
- 💡 **Suggest features:** Share your ideas in issues
- 📖 **Improve docs:** Submit PRs for typos or clarity
- ⭐ **Star the repo:** Help others discover these tools

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/your-feature`
3. **Make your changes** (follow existing code style)
4. **Test thoroughly** (include examples in PR description)
5. **Submit a pull request** with clear description

### Contribution Ideas
- Add new data enrichment sources
- Build integrations (Zapier, n8n, custom APIs)
- Create additional Make.com blueprints
- Add multilingual support
- Improve AI prompts and analysis quality
- Build a web dashboard (React/Next.js)

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 🧠 Our Approach: AI Risk-First

Every tool in this repository follows our **transparent, auditable AI** philosophy:

- ✅ **No Black Boxes:** All logic is visible and configurable
- ✅ **Structured Output:** JSON with detailed reasoning and confidence scores
- ✅ **Error Handling:** Graceful failures with actionable error messages
- ✅ **Audit Trails:** Track all API calls and decisions
- ✅ **Human-in-the-Loop:** Tools assist, not replace, human judgment
- ✅ **Continuous Improvement:** Built for iteration and refinement

We believe AI automation should be **trustworthy, explainable, and outcome-focused.**

---

## 💬 Community & Support

### Get Help
- 📖 **Read the Docs:** Check tool-specific READMEs first
- 🐛 **Report Issues:** [GitHub Issues](../../issues)
- 💡 **Feature Requests:** [Open a discussion](../../discussions)
- 📧 **Email:** [Contact us directly](mailto:support@resultantai.com)

### Testimonials

> "The lead enrichment tool replaced three paid services for our agency. The ICP scoring is incredibly accurate." — SaaS Agency Owner

> "Finally, marketing audit automation that actually works. Saves us 5+ hours per client." — Digital Marketing Consultant

> "Production-ready code with excellent documentation. Integrated into our CRM in under an hour." — DevOps Engineer

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**TL;DR:** You can use, modify, and distribute this code for any purpose (commercial or personal), with attribution.

---

## 🏢 About ResultantAI

ResultantAI builds **transparent, production-ready AI automation** for founders, operators, and growth teams.

**Our Principles:**
- 🎯 **Outcome-Focused:** Build for business results, not just technical demos
- 🔍 **Transparency First:** No black boxes, clear reasoning, full auditability
- 🚀 **Production-Ready:** Enterprise-grade code, not prototypes
- 🤝 **Open Source:** Share knowledge, build together, lift the industry

**What We Specialize In:**
- AI agent workflows for sales, ops, and client delivery
- No-code/low-code automation (Make.com, Zapier, Airtable, Notion)
- Explainable AI systems with audit trails and risk dashboards
- Productized automation libraries for repeatable, scalable results

---

## ⭐ Star History

If you find these tools useful, please star the repository! It helps others discover these resources.

[![Star History Chart](https://api.star-history.com/svg?repos=ResultantAI/ResultantAI&type=Date)](https://star-history.com/#ResultantAI/ResultantAI&Date)

---

## 🔗 Links & Resources

- **Website:** [ResultantAI.com](https://resultantai.com) (coming soon)
- **Documentation:** [GitHub Wiki](../../wiki)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **Security:** [SECURITY.md](SECURITY.md)

---

**Built with ❤️ by ResultantAI** | **Powered by Claude AI** | **MIT Licensed**

*Making AI automation transparent, trustworthy, and production-ready.*
