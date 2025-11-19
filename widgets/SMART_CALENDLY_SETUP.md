# 🧠 Smart Calendly Setup Guide

## YOUR COMPETITIVE ADVANTAGE

While competitors blindly book everyone the same way, **you'll have AI working for you**:

✅ **Auto-qualify leads** before they book (high/medium/low value)
✅ **Route intelligently** based on revenue potential
✅ **Pre-enrich data** using your existing API
✅ **Personalize messages** for each tier
✅ **Send to CRM** automatically with full context

This is what separates YOU from everyone else doing "generic Calendly embeds."

---

## 📋 Quick Start (30 Minutes)

### Step 1: Create Your Calendly Event Types (15 min)

Go to [calendly.com/event_types](https://calendly.com/event_types) and create **4 event types**:

#### 1. VIP Revenue Audit (30 min)
- **Name**: "VIP Revenue Audit"
- **Duration**: 30 minutes
- **Your best time slots**: Limit to your peak performance hours
- **Custom questions** (set these up):
  1. "Monthly leads" → Text field
  2. "Average deal size" → Text field
  3. "Current close rate" → Text field
  4. "Annual revenue leak" → Text field
  5. "Company name" → Text field
  6. "Website" → Text field
  7. "Biggest challenge" → Textarea

#### 2. Standard Revenue Audit (30 min)
- Same as VIP, but with more availability
- Less restrictive time slots

#### 3. Discovery Call (15 min)
- **Duration**: 15 minutes
- Quick qualification call
- Same custom questions (shorter format)

#### 4. Group Workshop (60 min)
- **Duration**: 60 minutes
- **Type**: Group event (up to 10 people)
- Monthly recurring session

### Step 2: Update Configuration (5 min)

Edit `smart-booking-config.js` and replace the Calendly URLs:

```javascript
calendly: {
    vip: 'https://calendly.com/YOUR-NAME/vip-revenue-audit',
    standard: 'https://calendly.com/YOUR-NAME/revenue-audit',
    discovery: 'https://calendly.com/YOUR-NAME/15min-discovery',
    workshop: 'https://calendly.com/YOUR-NAME/group-workshop'
}
```

### Step 3: Customize Routing Thresholds (5 min)

Adjust routing rules based on your business:

```javascript
routing: {
    vip: {
        minRevenueLeak: 100000,  // Adjust threshold
        minMonthlyLeads: 50,     // Adjust minimum leads
        priority: 1
    },
    // ... etc
}
```

**Recommendations by business type:**

| Business Type | VIP Threshold | Standard Threshold |
|--------------|---------------|-------------------|
| Enterprise B2B | $250K+ | $75K+ |
| SMB B2B | $100K+ | $25K+ |
| Agency | $50K+ | $15K+ |
| Consulting | $75K+ | $20K+ |

### Step 4: Deploy (5 min)

Choose deployment method:

**Option A: Netlify Drop (fastest)**
```bash
# Drag /widgets folder to app.netlify.com/drop
# Get instant URL
```

**Option B: GitHub Pages**
```bash
# Enable in repo settings → Pages
# URL: https://yourusername.github.io/ResultantAI/widgets/smart-revenue-calculator.html
```

**Option C: Your domain**
```bash
# Upload to your hosting
# Access at: yourdomain.com/calculator
```

---

## 🔗 Integration Options

### Option A: Standalone (Week 1 - Fastest)

**Setup time**: 5 minutes
**Complexity**: ⭐ Easy

Just share the calculator URL directly:
- In email campaigns
- On LinkedIn
- In your bio links
- Direct traffic to it

**Pros**: Works immediately, no additional setup
**Cons**: No CRM integration yet

---

### Option B: Webhook → CRM (Week 2 - Recommended)

**Setup time**: 30 minutes
**Complexity**: ⭐⭐ Moderate

#### Using Make.com (Recommended)

1. **Create new scenario** at make.com
2. **Add webhook trigger**:
   - Copy webhook URL
   - Paste into `smart-booking-config.js` line 156

3. **Add router** based on tier:
   ```
   Webhook → Router →
     - If tier = "vip" → Send to CRM with tag "VIP"
     - If tier = "standard" → Send to CRM with tag "Standard"
     - If tier = "discovery" → Send to CRM with tag "Discovery"
     - If tier = "workshop" → Send to CRM with tag "Workshop"
   ```

4. **Connect your CRM**:
   - HubSpot: Add "Create/Update Contact" module
   - Salesforce: Add "Create Lead" module
   - Google Sheets: Add "Add Row" (simple CRM)
   - Your custom API: HTTP module

5. **Optional: Send Slack notification** for VIP leads

#### Sample Make.com Blueprint

```json
{
  "webhook": "{{WEBHOOK_URL}}",
  "filters": [
    {
      "condition": "tier = vip",
      "action": "send_to_crm",
      "tags": ["VIP", "Hot Lead", "Revenue Calculator"],
      "notification": "slack"
    }
  ]
}
```

---

### Option C: Full Automation (Week 3 - Ultimate)

**Setup time**: 2 hours
**Complexity**: ⭐⭐⭐ Advanced

**The complete flow:**

```
1. User fills calculator
   ↓
2. JavaScript sends to webhook
   ↓
3. Make.com receives data
   ↓
4. Trigger enrichment API (your existing /enrich endpoint)
   ↓
5. Get company data, employee count, tech stack
   ↓
6. Score lead (A/B/C)
   ↓
7. Send to CRM with enriched data
   ↓
8. If VIP: Send Slack alert + SMS to you
   ↓
9. Trigger email sequence based on tier
   ↓
10. User books on Calendly
    ↓
11. Calendly webhook → Make.com
    ↓
12. Generate pre-call AI brief
    ↓
13. Email you the brief 1 hour before call
```

**Make.com modules needed:**
- Webhook (trigger)
- HTTP Request (call your /enrich API)
- Router (route by tier)
- CRM module (HubSpot/Salesforce/etc)
- Email module (send sequences)
- Slack module (VIP alerts)
- OpenAI module (generate pre-call brief)

---

## 🎯 Calendly Pre-Fill Setup

To pass calculator data to Calendly, you need to configure **custom questions** in each event type.

### In Calendly Event Settings:

1. Go to event → Edit → Questions
2. Add these custom questions:

| Question Label | Field Name | Type |
|---------------|------------|------|
| "How many leads do you get monthly?" | `a1` | Short Text |
| "What's your average deal size?" | `a2` | Short Text |
| "What's your current close rate?" | `a3` | Short Text |
| "Calculated revenue leak" | `a4` | Short Text |
| "Company name" | `a5` | Short Text |
| "Website" | `a6` | Short Text |
| "Biggest challenge right now" | `a7` | Long Text |

### How It Works:

The calculator passes data via URL parameters:
```
https://calendly.com/you/vip-audit?
  name=John%20Smith&
  email=john@example.com&
  a1=100&
  a2=5000&
  a3=15&
  a4=$75000&
  a5=Acme%20Inc
```

When the booking form opens, **all fields are pre-filled** with the calculator data!

---

## 🚀 Advanced: Pre-Call Enrichment

This is YOUR secret weapon - get full company intel BEFORE the call.

### Workflow:

```javascript
// In smart-booking-config.js, line 171-193

enrichLead: async function(leadData) {
    // Calls YOUR existing /enrich endpoint
    // Returns: employee count, tech stack, funding, etc.
    // All stored in your system BEFORE the call
}
```

### Setup:

1. Make sure your Flask server is running
2. Enable the enrichment endpoint:
   ```bash
   python server.py
   ```
3. Update the API URL in config if hosted remotely:
   ```javascript
   const response = await fetch('https://your-api.com/enrich', {
       method: 'POST',
       body: JSON.stringify({ domain: domain })
   });
   ```

### What You Get:

Before every call, you'll have:
- Company size & revenue
- Technologies they use
- Recent funding rounds
- LinkedIn data
- Contact info
- ICP fit score

**This means you can**:
- Customize your pitch
- Reference their tech stack
- Show relevant case studies
- Skip unqualified leads
- Prioritize high-value calls

---

## 📊 Tracking & Analytics

### Google Analytics Integration

Add before `</head>` in both calculator files:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Events Tracked:

The calculator already tracks:
- ✅ `booking_initiated` - When CTA is clicked
- ✅ `tier` - Which calendar tier (vip/standard/etc)
- ✅ `value` - The calculated revenue leak amount

### Create Dashboard:

Track these metrics:
1. Calculator completions
2. Booking rate by tier
3. Average revenue leak
4. VIP lead rate
5. Email capture rate
6. Calendly booking completion

---

## 🎨 Customization Guide

### Change Tier Thresholds

Edit `smart-booking-config.js` line 28-53:

```javascript
routing: {
    vip: {
        minRevenueLeak: 150000,  // Raise to be more selective
        minMonthlyLeads: 100,    // Only larger companies
        priority: 1
    }
}
```

### Change Messages

Edit line 61-97 for tier-specific copy:

```javascript
messages: {
    vip: {
        heading: '🎯 Your Custom Heading',
        subheading: 'Custom message with {{leak}} variable',
        buttonText: 'Custom Button Text',
        guarantee: 'Custom guarantee'
    }
}
```

### Change Colors

Edit `smart-revenue-calculator.html` CSS:

```css
/* Main gradient */
background: linear-gradient(135deg, #YOUR-COLOR 0%, #YOUR-COLOR-2 100%);

/* Tier badges */
.tier-vip {
    background: linear-gradient(135deg, #gold 0%, #orange 100%);
}
```

---

## 🔧 Troubleshooting

### Calculator not routing correctly

**Issue**: Everyone gets same tier
**Fix**: Check `smart-booking-config.js` is loaded:
```html
<script src="smart-booking-config.js"></script>
```

### Calendly not pre-filling

**Issue**: Data not showing in Calendly form
**Fix**:
1. Verify custom questions are set up (a1, a2, etc.)
2. Check URL parameters are being passed
3. Open browser console, check for errors

### Webhook not receiving data

**Issue**: CRM not getting lead data
**Fix**:
1. Verify webhook URL is correct (line 156)
2. Check CORS headers (might need to enable)
3. Test webhook with Postman first
4. Check Make.com/Zapier logs

### Enrichment not working

**Issue**: No company data coming through
**Fix**:
1. Verify Flask server is running
2. Check API endpoint URL
3. Test /enrich endpoint directly:
   ```bash
   curl -X POST http://localhost:5000/enrich \
     -H "Content-Type: application/json" \
     -d '{"domain":"stripe.com"}'
   ```

---

## 📞 Week 1 Quick Win Setup

**Total time**: 45 minutes

1. ✅ Create 4 Calendly event types (15 min)
2. ✅ Update config with your URLs (5 min)
3. ✅ Deploy to Netlify (5 min)
4. ✅ Test calculator → booking flow (10 min)
5. ✅ Share link in email signature (2 min)
6. ✅ Post on LinkedIn (5 min)
7. ✅ Add to website (3 min)

**Result**: You're now capturing leads with intelligent routing!

---

## 🚀 Week 2 Power-Up

**Total time**: 1 hour

1. ✅ Set up Make.com webhook (20 min)
2. ✅ Connect to CRM (15 min)
3. ✅ Add Slack notifications for VIP leads (10 min)
4. ✅ Create email sequences by tier (15 min)

**Result**: Full automation from calculator → CRM → email sequence

---

## ⚡ Week 3 Ultimate System

**Total time**: 2 hours

1. ✅ Enable pre-call enrichment (30 min)
2. ✅ Build AI pre-call brief generator (45 min)
3. ✅ Set up analytics dashboard (30 min)
4. ✅ Create A/B testing variants (15 min)

**Result**: You have MORE data than your competitors before you even pick up the phone

---

## 💡 Pro Tips

1. **Test all tiers**: Book test calls through each tier to verify routing
2. **Watch for VIPs**: Set up mobile push notifications for VIP bookings
3. **Response time**: Aim to respond to VIP leads within 15 minutes
4. **Pre-call research**: Use the enrichment data to customize your pitch
5. **Follow-up**: If they calculate but don't book, capture their email anyway

---

## 🎯 Success Metrics to Track

Week 1:
- Calculator views
- Completion rate
- Booking rate
- Revenue leak average

Week 2:
- CRM integration success rate
- Email sequence open rates
- VIP lead percentage

Week 3:
- Pre-call data accuracy
- Show-up rate by tier
- Close rate by tier
- ROI from the system

---

**Built by ResultantAI** | Last updated: 2025-01-19

Need help? Check the main README or test your setup locally first.
