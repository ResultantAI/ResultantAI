# Make.com Automation Blueprints

Pre-built Make.com scenarios that integrate with the ResultantAI demo automation systems. Import these blueprints directly into Make.com for instant automation workflows.

## 📦 Available Blueprints

### 1. Marketing Audit Automation
**File:** `marketing-audit-automation.json`

Automatically audits company websites and delivers insights via Slack and Google Sheets.

**Workflow:**
1. Webhook receives company URL and industry
2. Executes `marketing_audit.py` script
3. Sends top 3 quick wins to Slack
4. Stores full report in Google Sheets
5. Tags company in HubSpot CRM as "audit completed"

**Use Cases:**
- Automated client onboarding audits
- Sales enablement (audit before first call)
- Lead magnet delivery
- Marketing health checks

---

### 2. Lead Enrichment Pipeline
**File:** `lead-enrichment-pipeline.json`

Enriches new HubSpot contacts with company intelligence and routes based on ICP fit.

**Workflow:**
1. Monitors HubSpot for new contacts (every 15 min)
2. Enriches contact with `lead_enrichment.py`
3. Scores against ICP criteria (0-100)
4. Routes based on score:
   - **Hot Leads (80+)**: Slack alert + high priority tag
   - **Warm Leads (60-79)**: Nurture sequence enrollment
   - **Cold Leads (<60)**: Long-term nurture campaign
5. Logs all enrichment data to Google Sheets

**Use Cases:**
- Automated lead qualification
- SDR enablement with pre-scored leads
- Pipeline prioritization
- CRM data enrichment

---

### 3. MCA Qualification Workflow
**File:** `mca-qualification-workflow.json`

Automated underwriting for Merchant Cash Advance applications with instant decisions.

**Workflow:**
1. Form submission webhook receives application
2. Executes `mca_qualification.py` for instant decision
3. Logs all applications to Google Sheets
4. Routes based on decision:
   - **APPROVED**: Sends offer email + notifies underwriters
   - **REJECTED**: Sends decline email with improvement tips
5. All decisions tracked for compliance

**Use Cases:**
- Instant pre-qualification for applicants
- Automated underwriting workflows
- Lead qualification for financial services
- Demo tool for lending automation

---

## 🚀 Quick Start

### Prerequisites

1. **Make.com Account** (Free or Pro plan)
2. **Server with Python Scripts** (ResultantAI automation scripts)
3. **API Connections:**
   - Slack (for notifications)
   - Google Sheets (for logging)
   - HubSpot (for CRM integration)
   - Email (SMTP or Gmail)

### Import Steps

#### 1. Download Blueprint
```bash
# Clone the repo or download individual blueprints
git clone https://github.com/ResultantAI/ResultantAI.git
cd ResultantAI/make-blueprints/
```

#### 2. Import to Make.com

1. Log into Make.com
2. Click **"Scenarios"** in left sidebar
3. Click **"+ Create a new scenario"**
4. Click the **three dots (⋮)** in top right
5. Select **"Import Blueprint"**
6. Upload the JSON file
7. Click **"Save"**

#### 3. Configure Connections

Replace these placeholders in the imported scenario:

**All Blueprints:**
- `YOUR_SERVER_URL` → Your Python script execution endpoint
- `YOUR_API_TOKEN` → Your authentication token

**Slack:**
- `YOUR_SLACK_CONNECTION_ID` → Create Slack connection
- `C0123456789` → Replace with your Slack channel IDs

**Google Sheets:**
- `YOUR_GOOGLE_SHEETS_CONNECTION_ID` → Create Google connection
- `YOUR_SPREADSHEET_ID` → Your Google Sheet ID

**HubSpot (Lead Enrichment):**
- `YOUR_HUBSPOT_CONNECTION_ID` → Create HubSpot connection
- `YOUR_PORTAL_ID` → Your HubSpot portal ID
- `YOUR_NURTURE_SEQUENCE_ID` → HubSpot sequence IDs

**Email (MCA Workflow):**
- `YOUR_EMAIL_CONNECTION_ID` → Create email connection

#### 4. Test the Scenario

Each blueprint includes test data in the notes section. Use "Run once" to test.

---

## 🔧 Server Configuration

### Option 1: Simple HTTP Wrapper (Recommended)

Create a simple Flask/Express endpoint that executes the Python scripts:

```python
# server.py
from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/execute-script', methods=['POST'])
def execute_script():
    data = request.json
    script = data['script']
    args = data['args']

    # Build command
    if script == 'marketing_audit.py':
        cmd = f"source venv/bin/activate && python3 marketing_audit.py --url {args['url']} --industry \"{args['industry']}\""
    elif script == 'lead_enrichment.py':
        cmd = f"source venv/bin/activate && python3 lead_enrichment.py --domain {args['domain']}"
    elif script == 'mca_qualification.py':
        cmd = f"source venv/bin/activate && python3 mca_qualification.py --revenue {args['monthly_revenue']} --time-in-business {args['time_in_business_months']} --credit-score {args['credit_score']} --industry \"{args['industry']}\""
    else:
        return jsonify({'error': 'Unknown script'}), 400

    # Execute
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        return jsonify(json.loads(result.stdout))
    else:
        return jsonify({'error': result.stderr}), 500

if __name__ == '__main__':
    app.run(port=5000)
```

### Option 2: Serverless (AWS Lambda, Google Cloud Functions)

Deploy each Python script as a serverless function and update URLs in blueprints.

### Option 3: Direct SSH Execution

Use Make.com's SSH module to execute scripts directly on your server.

---

## 📊 Google Sheets Setup

### Marketing Audit Sheet

Create a Google Sheet with these headers:

```
Timestamp | Company Name | Company URL | Industry | Overall Score | SEO Score | Content Score | Social Score | Quick Win 1 | Quick Win 2 | Quick Win 3 | Strengths | Weaknesses | Requester Email | Full Report JSON
```

### Lead Enrichment Sheet

Create sheet named "Lead Enrichment Log" with headers:

```
Timestamp | Contact ID | Company Name | Domain | ICP Score | Lead Category | Industry | Company Size | Funding Stage | Tech Stack | Revenue Score | Industry Score | Tech Score | Recommendation | HubSpot URL
```

### MCA Applications Sheet

Create sheet named "MCA Applications" with headers:

```
Timestamp | Application ID | Business Name | Contact Name | Contact Email | Phone | Monthly Revenue | Time in Business | Credit Score | Industry | Qualification Score | Grade | Decision | Approval Tier | Advance Amount | Factor Rate | Total Repayment | Term Months | Daily Payment | Effective APR | Primary Reason | Full Response
```

---

## 💬 Slack Channel Setup

### Marketing Audit Automation
- **#marketing-audits** (general audit notifications)

### Lead Enrichment Pipeline
- **#hot-leads** (score 80+)
- **#lead-enrichment-log** (optional: all enrichments)

### MCA Qualification Workflow
- **#underwriter-queue** (approved applications)
- **#rejections-log** (declined applications)

---

## 🔐 HubSpot Custom Properties

### For Lead Enrichment Pipeline

Create these custom properties in HubSpot:

| Property Name | Type | Description |
|--------------|------|-------------|
| `enrichment_status` | Single-line text | "completed" or empty |
| `enrichment_date` | Date | Date enriched |
| `icp_score` | Number | ICP fit score (0-100) |
| `lead_category` | Single-line text | hot_lead, warm_lead, cold_lead, poor_fit |
| `company_size` | Number | Estimated employees |
| `company_industry` | Single-line text | Detected industry |
| `funding_stage` | Single-line text | Bootstrap, Series A, etc. |
| `tech_stack` | Multi-line text | Detected technologies |
| `lead_status` | Dropdown | hot_lead, warm_lead, cold_lead, poor_fit |
| `lead_priority` | Dropdown | high, medium, low |
| `next_action` | Single-line text | Recommended next action |

### For Marketing Audit Automation

| Property Name | Type | Description |
|--------------|------|-------------|
| `marketing_audit_completed` | Checkbox | Audit status |
| `audit_date` | Date | Audit completion date |
| `audit_overall_score` | Number | Overall score (0-10) |
| `audit_seo_score` | Number | SEO score (0-10) |
| `marketing_audit_tag` | Single-line text | "audit_completed" |

---

## 🧪 Testing

### Test Data

**Marketing Audit:**
```json
{
  "url": "https://stripe.com",
  "industry": "FinTech",
  "company_name": "Stripe",
  "company_id": "123456",
  "requester_email": "test@example.com"
}
```

**Lead Enrichment:**
```json
{
  "website": "notion.so",
  "company": "Notion",
  "id": "123456"
}
```

**MCA Qualification:**
```json
{
  "monthly_revenue": 75000,
  "time_in_business_months": 18,
  "credit_score": 680,
  "industry": "E-commerce",
  "business_name": "Example LLC",
  "contact_email": "test@example.com",
  "contact_name": "John Doe",
  "phone": "555-123-4567",
  "application_id": "TEST-001"
}
```

### Testing Workflow

1. **Marketing Audit:**
   ```bash
   curl -X POST https://YOUR_WEBHOOK_URL \
     -H "Content-Type: application/json" \
     -d '{"url": "https://stripe.com", "industry": "FinTech", "company_name": "Stripe"}'
   ```

2. **Lead Enrichment:**
   - Create test contact in HubSpot with website field
   - Wait 15 minutes for trigger or "Run once" manually

3. **MCA Qualification:**
   ```bash
   curl -X POST https://YOUR_WEBHOOK_URL \
     -H "Content-Type: application/json" \
     -d @test-mca-application.json
   ```

---

## 🎨 Customization

### Modify Email Templates

Edit the HTML content in email modules to match your branding:
- Update colors, logos, fonts
- Customize contact information
- Adjust messaging tone

### Adjust Routing Logic

**Lead Enrichment:**
- Change score thresholds (default: 80+, 60-80, <60)
- Add more granular routing (A/B/C/D/F grades)
- Route by industry or other criteria

**MCA Qualification:**
- Add manual review step for subprime approvals
- Route premium approvals to different underwriters
- Add SMS notifications for high-value applications

### Add More Integrations

Extend blueprints with:
- **CRM**: Salesforce, Pipedrive, Close
- **Email**: SendGrid, Mailgun, Customer.io
- **SMS**: Twilio notifications
- **Calendar**: Auto-schedule calls for hot leads
- **DocuSign**: Send contracts for approved MCAs

---

## 🔍 Troubleshooting

### Blueprint Won't Import
- Ensure JSON is valid (use jsonlint.com)
- Check Make.com plan supports required modules
- Try importing to new scenario vs. existing

### Script Execution Fails
- Verify server URL is accessible from Make.com
- Check authentication token is correct
- Ensure Python environment is activated
- Review server logs for errors

### No Data in Google Sheets
- Verify Google Sheets connection is authorized
- Check spreadsheet ID is correct
- Ensure sheet name matches exactly
- Verify column headers exist

### HubSpot Updates Fail
- Check custom properties exist in HubSpot
- Verify API key has write permissions
- Ensure contact/company IDs are valid
- Check rate limits (Make.com may throttle)

### Email Not Sending
- Verify email connection is configured
- Check spam folders
- Ensure "from" email is authorized
- Review email service logs

---

## 📈 Performance Tips

1. **Batching**: Group operations when possible
2. **Scheduling**: Spread triggers throughout day to avoid rate limits
3. **Error Handling**: Add error handlers for critical steps
4. **Logging**: Log all operations to sheets for debugging
5. **Testing**: Always test with "Run once" before activating

---

## 🔒 Security Best Practices

1. **API Keys**: Store in Make.com connections (not hardcoded)
2. **Webhook URLs**: Keep private, rotate periodically
3. **Data Retention**: Set Google Sheets cleanup policies
4. **Access Control**: Limit Make.com scenario permissions
5. **Compliance**: Review data handling for GDPR/CCPA

---

## 📝 Blueprint Modification Log

Track customizations for easy updates:

```
Blueprint: marketing-audit-automation.json
Modified: 2025-11-13
Changes:
- Updated Slack channel to #client-audits
- Added email notification to sales team
- Customized scoring thresholds

Blueprint: lead-enrichment-pipeline.json
Modified: 2025-11-13
Changes:
- Adjusted hot lead threshold to 85
- Added Salesforce integration
- Modified nurture sequence IDs
```

---

## 🆘 Support

### Documentation
- **Make.com Docs**: https://www.make.com/en/help/
- **Python Scripts**: See individual README files in repo
- **API References**: Check connection provider docs

### Community
- Make.com Community Forum
- ResultantAI GitHub Issues
- Slack support channel

---

## 📄 License

These blueprints are provided as-is for demonstration purposes. Customize freely for your use cases.

---

**Updated:** 2025-11-13
**Version:** 1.0
**Compatibility:** Make.com (all plans)
