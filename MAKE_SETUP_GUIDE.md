# Make.com Setup Guide: Marketing Audit Automation

**🎯 Goal:** Build a simple Make.com scenario that runs marketing audits when triggered via webhook.

**⏱️ Time:** 15-20 minutes
**💰 Cost:** Free Make.com tier works fine
**🔧 Skill Level:** Beginner-friendly

---

## 📋 What You'll Need

Before starting, gather these:

1. ✅ **Make.com account** (free tier OK) - [Sign up here](https://make.com)
2. ✅ **Anthropic API Key** - Get from [console.anthropic.com](https://console.anthropic.com)
3. ✅ **Slack Workspace** - Create a channel called `#marketing-audits`
4. ✅ **Google Sheet** - Create a blank sheet
5. ✅ **Server with Python 3.8+** - Where your `marketing_audit.py` script lives

---

## 🏗️ Architecture Overview

Here's what we're building:

```
Webhook → HTTP Request → JSON Parser → Slack + Google Sheets
   ↓           ↓              ↓              ↓
 Trigger    Runs Python   Parses results  Sends results
            script
```

**Flow:**
1. You send data to a webhook URL
2. Make.com calls your Python script on your server
3. Script returns JSON audit results
4. Results go to Slack + Google Sheets

---

## 🚀 Step-by-Step Setup

### MODULE 1: Webhook Setup (Trigger)

This is the entry point - it receives data and kicks off your automation.

#### Steps:

1. **Login to Make.com** → Click "Create a new scenario"

2. **Add Webhook Module:**
   - Click the big `+` button
   - Search for: `Webhooks`
   - Select: **"Webhooks" app** (icon looks like a plug)
   - Choose: **"Custom webhook"**

3. **Create Webhook:**
   - Click **"Add"** next to "Webhook" dropdown
   - Give it a name: `Marketing Audit Trigger`
   - Click **"Save"**
   - Copy the webhook URL (you'll test with this later)

4. **Define Data Structure:**
   - Click **"Show advanced settings"**
   - Under "Data structure", click **"Add"**
   - Name it: `Marketing Audit Input`
   - Click **"Generator"**
   - Paste this sample JSON:

   ```json
   {
     "url": "https://stripe.com",
     "industry": "FinTech"
   }
   ```

   - Click **"Save"**

5. **Save the module** (checkmark button)

#### What it should look like:
```
📌 Visual:
┌─────────────────────────┐
│  🔌 Custom Webhook      │
│                         │
│  Webhook: Marketing     │
│           Audit Trigger │
│                         │
│  Expects:               │
│  • url (string)         │
│  • industry (string)    │
└─────────────────────────┘
```

#### Common Errors:
- ❌ **"Webhook not working"** → Make sure you clicked "Save" and copied the full URL
- ❌ **"Data not received"** → Send a test POST request to verify webhook is listening
- ❌ **"JSON parsing error"** → Ensure your test payload is valid JSON

---

### MODULE 2: HTTP Request (Calls Python Script)

This module calls an HTTP endpoint that runs your Python script.

#### 🎯 Two Options:

**Option A: Direct Server Execution** (if you have SSH access)
**Option B: HTTP Endpoint** (recommended - what we'll use)

We'll use **Option B** because it's more reliable and doesn't require Make.com to SSH into your server.

#### Prerequisites:

You need to set up a simple HTTP endpoint that runs your Python script. Here's a quick Flask example:

**Create `api.py` on your server:**

```python
from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/run-audit', methods=['POST'])
def run_audit():
    data = request.json

    # Run Python script with JSON input
    result = subprocess.run(
        ['python3', '/home/user/ResultantAI/marketing_audit.py'],
        input=json.dumps(data),
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return jsonify(json.loads(result.stdout))
    else:
        return jsonify({'error': result.stderr}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Run it:**
```bash
pip install flask
python3 api.py
```

**Your endpoint URL:** `http://YOUR_SERVER_IP:5000/run-audit`

#### Steps in Make.com:

1. **Add HTTP Module:**
   - Click the `+` button after Webhook
   - Search for: `HTTP`
   - Select: **"HTTP" app**
   - Choose: **"Make a request"**

2. **Configure Request:**

   **URL:**
   ```
   http://YOUR_SERVER_IP:5000/run-audit
   ```
   *(Replace `YOUR_SERVER_IP` with your actual server IP or domain)*

   **Method:** `POST`

   **Headers:**
   - Click **"Add item"**
   - Name: `Content-Type`
   - Value: `application/json`

   **Body type:** `Raw`

   **Request content:**
   ```json
   {
     "url": "{{1.url}}",
     "industry": "{{1.industry}}"
   }
   ```

   ⚠️ **IMPORTANT:** The `{{1.url}}` and `{{1.industry}}` are variables from Module 1 (webhook). Make.com auto-suggests these when you start typing `{{`.

   **Timeout:** `120` (seconds - script needs time to run)

   **Parse response:** ✅ **YES**

3. **Save the module**

#### What it should look like:
```
📌 Visual:
┌─────────────────────────────────┐
│  🌐 HTTP - Make a request       │
│                                 │
│  URL: http://YOUR_IP:5000/...  │
│  Method: POST                   │
│  Headers:                       │
│    Content-Type: application/   │
│                  json           │
│  Body:                          │
│    {"url": "{{1.url}}",         │
│     "industry": "{{1.industry}}"}│
│  Timeout: 120s                  │
└─────────────────────────────────┘
```

#### Common Errors:
- ❌ **"Connection timeout"** → Check server is running and accessible
- ❌ **"Connection refused"** → Firewall blocking port 5000? Try opening it
- ❌ **"500 Internal Server Error"** → Check your Python script logs
- ❌ **"Module variables not showing"** → Make sure Module 1 ran successfully first

---

### MODULE 3: JSON Parser (Optional but Recommended)

This parses the JSON response from your Python script to make fields accessible.

> **Note:** If HTTP module already parsed the response (it usually does), you can skip this. But adding it makes your data structure clearer.

#### Steps:

1. **Add JSON Module:**
   - Click `+` after HTTP module
   - Search for: `JSON`
   - Select: **"JSON" app**
   - Choose: **"Parse JSON"**

2. **Configure:**

   **JSON string:**
   ```
   {{2.data}}
   ```
   *(This references the response from Module 2)*

   **Data structure:** Click **"Add"**
   - Name: `Marketing Audit Results`
   - Click **"Generator"**
   - Paste this sample output:

   ```json
   {
     "audit_metadata": {
       "timestamp": "2025-11-13T10:30:00Z",
       "company_url": "https://stripe.com",
       "industry": "FinTech",
       "model_used": "claude-sonnet-4-5-20250929"
     },
     "findings": {
       "seo_analysis": {
         "score": 8,
         "findings": ["Strong page titles", "Good meta descriptions"],
         "issues": ["Missing alt tags on images"]
       },
       "content_strategy": {
         "score": 9,
         "messaging_clarity": "Excellent",
         "blog_quality": "High-quality, relevant content",
         "cta_effectiveness": "Strong CTAs throughout",
         "findings": ["Clear value proposition", "Engaging copy"]
       },
       "social_media_presence": {
         "score": 7,
         "platforms_detected": ["LinkedIn", "Twitter"],
         "engagement_quality": "Good",
         "recommendations": ["Increase posting frequency"]
       },
       "paid_advertising": {
         "google_ads_potential": {
           "score": 9,
           "rationale": "High commercial intent keywords available",
           "recommended_keywords": ["payment processing", "online payments"]
         },
         "social_ads_potential": {
           "score": 8,
           "platforms": ["LinkedIn", "Facebook"],
           "rationale": "B2B audience matches well"
         }
       },
       "quick_wins": [
         {
           "title": "Add blog to homepage",
           "impact": "high",
           "effort": "low",
           "description": "Feature recent blog posts prominently",
           "expected_outcome": "20% increase in time on site"
         },
         {
           "title": "Implement schema markup",
           "impact": "medium",
           "effort": "low",
           "description": "Add structured data for rich snippets",
           "expected_outcome": "Better SERP visibility"
         },
         {
           "title": "Create lead magnet",
           "impact": "high",
           "effort": "medium",
           "description": "Develop downloadable resource",
           "expected_outcome": "Increase email signups 30%"
         }
       ],
       "overall_assessment": {
         "overall_score": 8,
         "strengths": ["Strong brand", "Clear messaging"],
         "weaknesses": ["Limited blog content", "No email capture"],
         "priority_actions": ["Start content marketing", "Build email list", "Improve SEO"]
       }
     }
   }
   ```

   - Click **"Save"**

3. **Save the module**

#### What it should look like:
```
📌 Visual:
┌─────────────────────────┐
│  📄 Parse JSON          │
│                         │
│  JSON string: {{2.data}}│
│                         │
│  Data structure:        │
│   Marketing Audit       │
│   Results               │
└─────────────────────────┘
```

#### Common Errors:
- ❌ **"Invalid JSON"** → Check your Python script returns valid JSON
- ❌ **"Data structure not matching"** → Re-generate structure with actual output
- ❌ **"Fields not accessible"** → Make sure you saved the data structure

---

### MODULE 4: Slack Message

Send a beautiful formatted message to Slack with the audit results.

#### Prerequisites:

1. **Create Slack Webhook:**
   - Go to [api.slack.com/apps](https://api.slack.com/apps)
   - Click **"Create New App"** → **"From scratch"**
   - Name: `Marketing Audit Bot`
   - Choose your workspace
   - Click **"Incoming Webhooks"** → Toggle ON
   - Click **"Add New Webhook to Workspace"**
   - Select channel: `#marketing-audits`
   - Copy the webhook URL (starts with `https://hooks.slack.com/...`)

#### Steps in Make.com:

1. **Add Slack Module:**
   - Click `+` after JSON module
   - Search for: `Slack`
   - Select: **"Slack" app**
   - Choose: **"Create a Message"**

2. **Configure Connection:**
   - Click **"Add"** next to Connection
   - Select **"Webhook"** connection type
   - Paste your Slack webhook URL
   - Click **"Save"**

3. **Configure Message:**

   **Channel:**
   ```
   #marketing-audits
   ```

   **Text:** *(Copy this exact template)*

   ```
   🎯 *Marketing Audit Complete!*

   *Company:* {{3.audit_metadata.company_url}}
   *Industry:* {{3.audit_metadata.industry}}
   *Overall Score:* {{3.findings.overall_assessment.overall_score}}/10

   📊 *Scores by Category:*
   • SEO: {{3.findings.seo_analysis.score}}/10
   • Content Strategy: {{3.findings.content_strategy.score}}/10
   • Social Media: {{3.findings.social_media_presence.score}}/10
   • Paid Ads Potential: {{3.findings.paid_advertising.google_ads_potential.score}}/10

   🎯 *Top 3 Quick Wins:*
   1. {{3.findings.quick_wins[1].title}} ({{3.findings.quick_wins[1].impact}} impact, {{3.findings.quick_wins[1].effort}} effort)
   2. {{3.findings.quick_wins[2].title}} ({{3.findings.quick_wins[2].impact}} impact, {{3.findings.quick_wins[2].effort}} effort)
   3. {{3.findings.quick_wins[3].title}} ({{3.findings.quick_wins[3].impact}} impact, {{3.findings.quick_wins[3].effort}} effort)

   💪 *Key Strengths:*
   {{join(3.findings.overall_assessment.strengths; newline)}}

   ⚠️ *Areas to Improve:*
   {{join(3.findings.overall_assessment.weaknesses; newline)}}

   📈 *Priority Actions:*
   {{join(3.findings.overall_assessment.priority_actions; newline)}}

   _Audit completed at {{formatDate(3.audit_metadata.timestamp; "YYYY-MM-DD HH:mm:ss")}}_
   ```

   **Message type:** `mrkdwn` *(Markdown formatting)*

4. **Save the module**

#### What it should look like:
```
📌 Visual:
┌─────────────────────────────┐
│  💬 Slack - Create Message  │
│                             │
│  Connection: Webhook        │
│  Channel: #marketing-audits │
│  Text: 🎯 Marketing Audit...│
│        (formatted message)  │
└─────────────────────────────┘
```

#### Common Errors:
- ❌ **"Invalid webhook"** → Double-check webhook URL is correct
- ❌ **"Message not formatting"** → Make sure text field has `mrkdwn` enabled
- ❌ **"Variables not showing"** → Verify Module 3 ran successfully
- ❌ **"Channel not found"** → Ensure #marketing-audits exists in your workspace

---

### MODULE 5: Google Sheets Row

Save audit results to a Google Sheet for tracking and analysis.

#### Prerequisites:

1. **Create Google Sheet:**
   - Go to [sheets.google.com](https://sheets.google.com)
   - Create new sheet, name it: `Marketing Audit Results`
   - Add these column headers in Row 1:

   | A | B | C | D | E | F | G | H | I | J | K |
   |---|---|---|---|---|---|---|---|---|---|---|
   | Timestamp | Company URL | Industry | Overall Score | SEO Score | Content Score | Social Score | Paid Ads Score | Top Quick Win | Strengths | Weaknesses |

   - Copy the Sheet ID from URL:
     ```
     https://docs.google.com/spreadsheets/d/[THIS_IS_THE_SHEET_ID]/edit
     ```

#### Steps in Make.com:

1. **Add Google Sheets Module:**
   - Click `+` after Slack module
   - Search for: `Google Sheets`
   - Select: **"Google Sheets" app**
   - Choose: **"Add a Row"**

2. **Configure Connection:**
   - Click **"Add"** next to Connection
   - Select **"Google (OAuth2)"**
   - Follow prompts to authorize Make.com to access your Google account
   - Click **"Save"**

3. **Configure Row:**

   **Spreadsheet:** Select your sheet from dropdown or paste Sheet ID:
   ```
   YOUR_SHEET_ID_HERE
   ```

   **Sheet Name:**
   ```
   Sheet1
   ```
   *(or whatever you named your tab)*

   **Values:** *(Map each field to a column)*

   **A - Timestamp:**
   ```
   {{formatDate(3.audit_metadata.timestamp; "YYYY-MM-DD HH:mm:ss")}}
   ```

   **B - Company URL:**
   ```
   {{3.audit_metadata.company_url}}
   ```

   **C - Industry:**
   ```
   {{3.audit_metadata.industry}}
   ```

   **D - Overall Score:**
   ```
   {{3.findings.overall_assessment.overall_score}}
   ```

   **E - SEO Score:**
   ```
   {{3.findings.seo_analysis.score}}
   ```

   **F - Content Score:**
   ```
   {{3.findings.content_strategy.score}}
   ```

   **G - Social Score:**
   ```
   {{3.findings.social_media_presence.score}}
   ```

   **H - Paid Ads Score:**
   ```
   {{3.findings.paid_advertising.google_ads_potential.score}}
   ```

   **I - Top Quick Win:**
   ```
   {{3.findings.quick_wins[1].title}}
   ```

   **J - Strengths:**
   ```
   {{join(3.findings.overall_assessment.strengths; ", ")}}
   ```

   **K - Weaknesses:**
   ```
   {{join(3.findings.overall_assessment.weaknesses; ", ")}}
   ```

4. **Save the module**

#### What it should look like:
```
📌 Visual:
┌────────────────────────────────┐
│  📊 Google Sheets - Add Row    │
│                                │
│  Spreadsheet: Marketing Audit  │
│               Results          │
│  Sheet: Sheet1                 │
│                                │
│  Values:                       │
│   A: {{3.audit_metadata...}}   │
│   B: {{3.audit_metadata...}}   │
│   C: {{3.audit_metadata...}}   │
│   ... (11 columns total)       │
└────────────────────────────────┘
```

#### Common Errors:
- ❌ **"Spreadsheet not found"** → Verify Sheet ID is correct
- ❌ **"Permission denied"** → Re-authorize Google Sheets connection
- ❌ **"Invalid column reference"** → Check that Sheet1 has headers in row 1
- ❌ **"Data not appearing"** → Make sure you're writing to correct sheet tab

---

## ✅ Testing Your Scenario

Now let's make sure everything works!

### 1. Save Your Scenario

- Click **"Save"** button (bottom left)
- Name it: `Marketing Audit Automation`

### 2. Turn It On

- Toggle the switch to **ON** (bottom left)
- Your scenario is now live!

### 3. Test the Webhook

Use this `curl` command (replace `YOUR_WEBHOOK_URL`):

```bash
curl -X POST YOUR_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://stripe.com",
    "industry": "FinTech"
  }'
```

**Or use Postman:**
- Method: `POST`
- URL: Your webhook URL
- Headers: `Content-Type: application/json`
- Body (raw JSON):
  ```json
  {
    "url": "https://stripe.com",
    "industry": "FinTech"
  }
  ```

### 4. Watch It Run

- Go to Make.com → Your scenario
- You'll see execution bubbles appear on each module
- Each should turn green ✅ if successful
- Red ❌ means error - click to see details

### 5. Verify Results

✅ Check Slack - should see audit message in #marketing-audits
✅ Check Google Sheet - should see new row with data
✅ Check Make.com execution log - all modules green

---

## 🧪 Test Payload Examples

### Basic Test (Minimal):
```json
{
  "url": "https://stripe.com",
  "industry": "FinTech"
}
```

### E-commerce Test:
```json
{
  "url": "https://www.shopify.com",
  "industry": "E-commerce"
}
```

### SaaS Test:
```json
{
  "url": "https://www.notion.so",
  "industry": "SaaS"
}
```

### Healthcare Test:
```json
{
  "url": "https://www.zocdoc.com",
  "industry": "Healthcare"
}
```

### Agency Test:
```json
{
  "url": "https://www.hubspot.com",
  "industry": "Marketing"
}
```

---

## 🐛 Troubleshooting

### Module 1: Webhook Issues

**Problem:** Webhook not receiving data
**Solution:**
- Check webhook URL is copied correctly
- Verify JSON is valid (use [jsonlint.com](https://jsonlint.com))
- Make sure scenario is turned ON

**Problem:** Data structure not matching
**Solution:**
- Delete and re-create data structure
- Use the Generator with your actual payload

---

### Module 2: HTTP Request Issues

**Problem:** Connection timeout
**Solution:**
- Verify your server is running: `curl http://YOUR_IP:5000/run-audit`
- Check firewall rules allow port 5000
- Try increasing timeout to 180 seconds

**Problem:** 500 Internal Server Error
**Solution:**
- Check Python script logs on server
- Verify `ANTHROPIC_API_KEY` is in `.env` file
- Test script manually: `echo '{"url":"https://stripe.com","industry":"FinTech"}' | python3 marketing_audit.py`

**Problem:** "ModuleNotFoundError" in Python
**Solution:**
- Install dependencies: `pip install anthropic requests beautifulsoup4 python-dotenv`
- Verify Python version: `python3 --version` (should be 3.8+)

---

### Module 3: JSON Parser Issues

**Problem:** "Invalid JSON" error
**Solution:**
- Check Module 2 response is valid JSON
- Look at execution history to see actual response
- Your Python script might be returning error messages instead of JSON

**Problem:** Fields not accessible in later modules
**Solution:**
- Make sure data structure was saved
- Re-generate data structure with actual output
- Try skipping this module if HTTP already parsed response

---

### Module 4: Slack Issues

**Problem:** Message not appearing in Slack
**Solution:**
- Verify webhook URL is correct (should start with `https://hooks.slack.com/services/`)
- Check #marketing-audits channel exists
- Test webhook directly: `curl -X POST YOUR_SLACK_WEBHOOK -H "Content-Type: application/json" -d '{"text":"Test"}'`

**Problem:** Formatting looks broken
**Solution:**
- Make sure you selected `mrkdwn` as message type
- Check that variables like `{{3.findings...}}` are mapping correctly
- Remove emojis if causing issues

**Problem:** Variables showing as blank
**Solution:**
- Verify Module 3 completed successfully
- Check that JSON structure matches what Python script returns
- Look at execution history to see actual data

---

### Module 5: Google Sheets Issues

**Problem:** "Permission denied"
**Solution:**
- Re-authorize Google Sheets connection
- Make sure you're logged into correct Google account
- Check sheet isn't restricted to specific users

**Problem:** Data appearing in wrong columns
**Solution:**
- Verify column headers in Row 1
- Check that sheet name matches (e.g., "Sheet1")
- Re-map fields in correct order

**Problem:** Row not being added
**Solution:**
- Check Sheet ID is correct (from URL)
- Make sure sheet tab name is exact match
- Verify connection has write permissions

---

## 📊 Expected Results

After successful execution, you should see:

### Slack Message:
```
🎯 Marketing Audit Complete!

Company: https://stripe.com
Industry: FinTech
Overall Score: 8/10

📊 Scores by Category:
• SEO: 8/10
• Content Strategy: 9/10
• Social Media: 7/10
• Paid Ads Potential: 9/10

🎯 Top 3 Quick Wins:
1. Add blog to homepage (high impact, low effort)
2. Implement schema markup (medium impact, low effort)
3. Create lead magnet (high impact, medium effort)

💪 Key Strengths:
Strong brand
Clear messaging

⚠️ Areas to Improve:
Limited blog content
No email capture

📈 Priority Actions:
Start content marketing
Build email list
Improve SEO

Audit completed at 2025-11-13 10:30:00
```

### Google Sheet Row:
| Timestamp | Company URL | Industry | Overall Score | SEO Score | Content Score | Social Score | Paid Ads Score | Top Quick Win | Strengths | Weaknesses |
|-----------|-------------|----------|---------------|-----------|---------------|--------------|----------------|---------------|-----------|------------|
| 2025-11-13 10:30:00 | https://stripe.com | FinTech | 8 | 8 | 9 | 7 | 9 | Add blog to homepage | Strong brand, Clear messaging | Limited blog content, No email capture |

---

## 🎯 Next Steps

Once your basic scenario works, consider adding:

1. **Error Handling:**
   - Add error handlers to each module
   - Send error notifications to Slack
   - Log errors to separate Google Sheet tab

2. **Validation:**
   - Add URL format validation before running script
   - Check that required fields aren't empty
   - Validate industry is in approved list

3. **Retry Logic:**
   - Use Repeater module to retry on failure
   - Add delays between retry attempts
   - Max 3 attempts recommended

4. **HubSpot Integration:**
   - Update company records with audit scores
   - Create tasks for sales team
   - Log activity timeline

5. **Email Notifications:**
   - Send audit results to requester
   - Include PDF report attachment
   - CC sales rep if company score is low

---

## 📚 Resources

- **Make.com Docs:** [make.com/en/help](https://make.com/en/help)
- **Slack Webhooks:** [api.slack.com/messaging/webhooks](https://api.slack.com/messaging/webhooks)
- **Google Sheets API:** [developers.google.com/sheets](https://developers.google.com/sheets)
- **Anthropic API:** [docs.anthropic.com](https://docs.anthropic.com)
- **Python Script:** [ResultantAI/marketing_audit.py](./marketing_audit.py)

---

## 🆘 Still Stuck?

1. **Check Make.com execution history** - Click on scenario → History tab
2. **Look at individual module outputs** - Click on each bubble to see data
3. **Test components individually** - Right-click module → "Run this module only"
4. **Check server logs** - SSH into server and check Python script output
5. **Verify all credentials** - API keys, webhooks, sheet IDs

---

## ✨ Tips for Success

✅ **Test incrementally** - Don't build all 5 modules at once. Test each one as you go.
✅ **Use real data** - Test with actual URLs to catch edge cases.
✅ **Watch execution history** - Make.com shows exactly what happened at each step.
✅ **Keep it simple first** - Get the basic flow working before adding bells and whistles.
✅ **Save often** - Make.com doesn't auto-save, so hit Save frequently.
✅ **Label modules** - Rename modules for clarity (right-click → Rename).
✅ **Use colors** - Color-code modules by function (right-click → Change color).

---

## 🎉 Congratulations!

You now have a working Marketing Audit automation!

Every time you send data to your webhook, Make.com will:
1. ✅ Receive the company info
2. ✅ Run the Python audit script
3. ✅ Parse the results
4. ✅ Send to Slack
5. ✅ Log to Google Sheets

**Total execution time:** ~30-60 seconds per audit

**Happy automating! 🚀**
