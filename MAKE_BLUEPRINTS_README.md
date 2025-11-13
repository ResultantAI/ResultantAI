# Make.com Blueprints - Production Ready

Three production-ready Make.com blueprints for automated marketing audits, lead enrichment, and MCA qualification with comprehensive error handling, data validation, and smart routing.

## 📦 What's Included

### 1. Marketing Audit Blueprint (`make-blueprint-marketing-audit.json`)
**Automates comprehensive marketing audits using AI**

**Features:**
- ✅ Webhook trigger with URL validation
- ✅ Error handling with Slack notifications to #errors
- ✅ Retry logic (3 attempts, 5-second delays)
- ✅ Rich Slack formatting with emojis and color-coded scores
- ✅ Conditional HubSpot update (only if company_id exists)
- ✅ Email notification to requester with report summary
- ✅ Aggregate tracking (total audits completed)
- ✅ Google Sheets logging with separate error sheet
- ✅ "View Full Report" button in Slack messages

**Required Configuration:**
- GOOGLE_SHEET_ID (with tabs: "Marketing Audits", "Errors", "Stats")
- SLACK_WEBHOOK_URL (#marketing-audits channel)
- SLACK_ERROR_WEBHOOK (#errors channel)
- HUBSPOT_API_KEY (optional)

**Test Payload:**
```json
{
  "url": "https://stripe.com",
  "industry": "FinTech",
  "company_id": "12345",
  "requester_email": "analyst@company.com"
}
```

---

### 2. Lead Enrichment Blueprint (`make-blueprint-lead-enrichment.json`)
**AI-powered lead enrichment with ICP scoring and smart routing**

**Features:**
- ✅ Smart caching: Skips re-enrichment if done in last 30 days
- ✅ Conditional routing by lead score:
  - **Hot leads (80+)** → #hot-leads with calendar booking button 📅
  - **Warm leads (60-79)** → #warm-leads
  - **Cold leads (40-59)** → #cold-leads
- ✅ Error handling with Slack notifications
- ✅ Retry logic (3 attempts, 5-second delays)
- ✅ Rich Slack formatting per category
- ✅ Google Sheets logging
- ✅ Configurable enrichment cache period

**Required Configuration:**
- GOOGLE_SHEET_ID (with tabs: "Enriched Leads", "Errors")
- SLACK_HOT_WEBHOOK (#hot-leads channel)
- SLACK_WARM_WEBHOOK (#warm-leads channel)
- SLACK_COLD_WEBHOOK (#cold-leads channel)
- SLACK_ERROR_WEBHOOK (#errors channel)
- CALENDAR_BOOKING_LINK (Calendly/booking URL for hot leads)
- ENRICHMENT_CACHE_DAYS (default: 30)

**Test Payload:**
```json
{
  "domain": "stripe.com",
  "company": "Stripe",
  "lead_id": "LEAD-12345"
}
```

---

### 3. MCA Qualification Blueprint (`make-blueprint-mca-qualification.json`)
**AI-powered business loan qualification with compliance logging**

**Features:**
- ✅ Comprehensive data validation:
  - Revenue range ($0 - $100M)
  - Credit score (300-850)
  - Required fields check
- ✅ Conditional routing by decision:
  - **APPROVED** → #underwriter-queue
  - **REJECTED** → #rejections-log
- ✅ Email templates for both outcomes:
  - Approval: Terms, amounts, next steps
  - Rejection: Constructive feedback, reapplication guidance
- ✅ Compliance logging: Separate sheet with detailed decision factors
- ✅ Error handling with Slack notifications
- ✅ Retry logic (3 attempts, 5-second delays)
- ✅ Rich Slack formatting with risk levels

**Required Configuration:**
- GOOGLE_SHEET_ID (with tabs: "MCA Applications", "Compliance Log", "Errors")
- SLACK_APPROVED_WEBHOOK (#underwriter-queue channel)
- SLACK_REJECTED_WEBHOOK (#rejections-log channel)
- SLACK_ERROR_WEBHOOK (#errors channel)
- EMAIL_FROM (notification sender address)
- MIN_REVENUE (default: $100,000)
- MIN_CREDIT_SCORE (default: 500)
- MIN_BUSINESS_AGE (default: 6 months)

**Test Payloads:**

*Approved Application:*
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

*Rejected Application:*
```json
{
  "company_name": "New Biz",
  "annual_revenue": 50000,
  "credit_score": 450,
  "business_age_months": 3,
  "industry": "Retail",
  "applicant_email": "owner@newbiz.com",
  "application_id": "MCA-2025-002"
}
```

---

## 🚀 Quick Start Guide

### Step 1: Import Blueprints

1. Log into [Make.com](https://make.com)
2. Go to **Scenarios** → **Create a new scenario**
3. Click **...** (three dots) → **Import Blueprint**
4. Upload one of the JSON files
5. Repeat for each blueprint

### Step 2: Configure Variables

Each blueprint has a **"Set Variables"** module (Module #3) with TODO comments. Replace these values:

**Example:**
```
GOOGLE_SHEET_ID: "1AbC123..." (your actual Google Sheet ID)
SLACK_WEBHOOK_URL: "https://hooks.slack.com/services/..." (your webhook URL)
```

### Step 3: Set Up Google Sheets

Create a Google Sheet with the required tabs:

**Marketing Audit Sheet Tabs:**
- **Marketing Audits** - Main audit results
- **Errors** - Error log
- **Stats** - Aggregate metrics (cell A1 = total count)

**Lead Enrichment Sheet Tabs:**
- **Enriched Leads** - Enriched lead data (include "Enrichment Date" column)
- **Errors** - Error log

**MCA Qualification Sheet Tabs:**
- **MCA Applications** - Application results
- **Compliance Log** - Detailed decision factors
- **Errors** - Error log

**See each blueprint's notes for column structures.**

### Step 4: Configure Slack Webhooks

1. Go to your Slack workspace settings
2. Create Incoming Webhooks for each channel:
   - Marketing Audit: #marketing-audits, #errors
   - Lead Enrichment: #hot-leads, #warm-leads, #cold-leads, #errors
   - MCA Qualification: #underwriter-queue, #rejections-log, #errors
3. Copy webhook URLs to blueprint variables

### Step 5: Test with Sample Payloads

Each blueprint's Module #1 (Webhook) has test payloads in the notes. Use these to test your setup.

1. Copy the webhook URL from Module #1
2. Send a test request:
```bash
curl -X POST "YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://stripe.com", "industry": "FinTech"}'
```

### Step 6: Activate Scenarios

1. Save each scenario
2. Click **Turn on** (toggle in top-right)
3. Monitor the first few runs for any issues

---

## 🛠️ Configuration Reference

### All Blueprints Include:

**Error Handling:**
- Automatic retry logic (3 attempts)
- 5-second delays between retries
- Slack notifications on failure
- Error logging to Google Sheets

**Data Validation:**
- Required field checks
- Format validation
- Range validation (where applicable)
- Clear error messages

**Response Formatting:**
- Rich Slack messages with emojis
- Visual indicators (🔥 hot, ⭐ warm, ❄️ cold)
- Color-coded scores (🟢 🟡 🔴)
- Action buttons ("View Report", "Book Meeting")

**Logging:**
- Timestamp for all records
- Complete input data captured
- Decision factors documented
- Error details with retry information

---

## 📊 Google Sheet Column Structures

### Marketing Audits Sheet
```
Timestamp | URL | Industry | Overall Score | SEO Score | Content Score |
Social Score | Paid Ads Score | Top Quick Win | Strengths | Weaknesses |
HubSpot ID | Requester Email
```

### Enriched Leads Sheet
```
Enrichment Date | Domain | Company Name | Industry | Lead Score | Category |
Employees | Size Category | Funding Stage | Tech Stack | Is Hiring |
Brand Maturity | Lead ID
```

### MCA Applications Sheet
```
Timestamp | Application ID | Company Name | Industry | Decision | Risk Level |
Annual Revenue | Credit Score | Business Age | Existing Debt |
Recommended Advance | Factor Rate | Payback Months | Applicant Email
```

### Compliance Log Sheet
```
Timestamp | Application ID | Company Name | Decision | Risk Level |
Revenue Assessment | Credit Assessment | Business Stability | Industry Risk |
Debt Burden | Red Flags | Approval Conditions | Underwriter Notes |
Revenue Threshold Met | Credit Threshold Met | Age Threshold Met | AI Model Version
```

### Errors Sheet (all blueprints)
```
Timestamp | System | Company/Domain | Additional Info | Error Message | Retry Info
```

---

## 🔐 Security Considerations

1. **Webhook URLs:** Keep webhook URLs private - they provide direct access to your scenarios
2. **API Keys:** Store in Make.com variables, never hardcode in external systems
3. **Google Sheets:** Set appropriate sharing permissions (not public)
4. **Email Notifications:** Use professional email addresses, not personal
5. **MCA Blueprint:** Marked as CONFIDENTIAL due to financial data sensitivity

---

## 🎯 Best Practices

### For Marketing Audits:
- Run during business hours for faster response
- Use HubSpot integration to enrich CRM data
- Review aggregate stats weekly (Stats sheet)
- Follow up on high-value audits within 24 hours

### For Lead Enrichment:
- Set ENRICHMENT_CACHE_DAYS based on lead velocity (30 days default)
- Monitor hot leads channel closely - respond within 24 hours
- Use calendar booking link for hot leads to convert faster
- Review warm leads weekly for nurture campaigns

### For MCA Qualification:
- Review compliance log monthly for audit trails
- Update minimum thresholds seasonally based on performance
- Respond to approved applications within 24 hours
- Use rejection emails as educational touchpoints
- Track rejection reasons to identify process improvements

---

## 🐛 Troubleshooting

### "Webhook not receiving data"
- Check that webhook URL is correct
- Verify JSON payload format matches expected structure
- Look for firewall/security blocking webhook calls

### "Script execution failed"
- Verify Python script path in variables is correct
- Check that .env file has ANTHROPIC_API_KEY
- Ensure script has execute permissions (chmod +x)
- Review error logs in Google Sheets for details

### "Slack messages not sending"
- Verify webhook URLs are active and correct
- Check that Slack app has permission to post to channels
- Test webhook URLs with curl before using in Make.com

### "Google Sheets not updating"
- Verify Make.com has Google Sheets connection authorized
- Check that sheet ID is correct
- Ensure sheet tab names match exactly (case-sensitive)
- Verify column count matches array length

### "Email not sending"
- Check email service is connected in Make.com
- Verify FROM address is authorized
- Test email delivery with simple message first

### "Validation errors"
- Review Module #4-6 filter conditions
- Check that input data types match expected formats
- Use test payloads from notes to verify setup

---

## 🔄 Updating Blueprints

To modify existing scenarios:

1. **Don't break existing flows:** Test changes in a cloned scenario first
2. **Version control:** Export blueprints before major changes
3. **Update documentation:** Keep notes in modules current
4. **Test thoroughly:** Use test payloads before activating changes
5. **Monitor first runs:** Watch logs for issues after updates

---

## 📈 Monitoring & Analytics

### Key Metrics to Track:

**Marketing Audits:**
- Total audits completed (Stats sheet, A1)
- Average overall score
- Most common weaknesses
- HubSpot update success rate

**Lead Enrichment:**
- Hot/warm/cold lead distribution
- Enrichment cache hit rate (avoided API calls)
- Average lead scores by industry
- Conversion rate from hot leads

**MCA Qualification:**
- Approval rate
- Average approved advance amount
- Most common rejection reasons
- Risk level distribution

**All Systems:**
- Error rate
- Average execution time
- Retry frequency
- API cost per run

---

## 💡 Advanced Customizations

### Add Custom Scoring:
Modify ICP scoring criteria in `icp_config.json` to match your target customer profile.

### Integrate with CRM:
Add modules to push data to Salesforce, HubSpot, or Pipedrive after enrichment/qualification.

### Build Dashboards:
Connect Google Sheets to Data Studio, Tableau, or Looker for visual reporting.

### Add Webhooks:
Trigger external systems (CRMs, marketing automation) based on outcomes.

### Create Nurture Sequences:
Route warm/cold leads to email sequences in ActiveCampaign or Mailchimp.

---

## 🆘 Support

### Included in Each Blueprint:
- Detailed module notes
- Configuration checklists
- Test payloads
- Expected outputs
- Error handling flows

### External Resources:
- [Make.com Documentation](https://www.make.com/en/help/home)
- [Anthropic API Docs](https://docs.anthropic.com/)
- Python script READMEs in this repository

### Getting Help:
1. Check module notes for specific configuration
2. Review error logs in Google Sheets
3. Test individual modules in Make.com debugger
4. Verify all prerequisites are met
5. Use test payloads to isolate issues

---

## 📄 License

These blueprints are provided as-is for commercial and personal use. Modify as needed for your organization.

---

**Built with Make.com + Claude AI** | **Production-Ready** | **Enterprise-Grade Error Handling**

*Last Updated: 2025-11-13*
