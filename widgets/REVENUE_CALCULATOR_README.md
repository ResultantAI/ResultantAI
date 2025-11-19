# 💰 Revenue Calculator Widget

An interactive, conversion-optimized calculator widget that shows prospects how much revenue they're losing. Perfect for lead generation and booking audits/consultations.

## ✨ Features

- **Real-time Calculations**: Instant feedback as users input their data
- **Beautiful Animations**: Smooth, professional animations that engage users
- **Mobile Responsive**: Works perfectly on all devices
- **Conversion-Optimized**: Designed to drive bookings with compelling CTAs
- **Easy to Embed**: Simple iframe integration with Framer, Webflow, or any platform
- **Customizable**: Easy to modify colors, text, and booking links

## 📊 What It Calculates

The calculator takes three inputs:
1. **Number of leads per month**
2. **Average deal size**
3. **Current close rate**

It then calculates potential revenue increase with a conservative 12.5% improvement in close rate (most businesses see 20-40% improvement).

### Formula
```
Current Annual Revenue = (Leads × Close Rate × Deal Size) × 12
Improved Annual Revenue = (Leads × Improved Close Rate × Deal Size) × 12
Revenue Leak = Improved Annual Revenue - Current Annual Revenue
```

## 🚀 Quick Start

### Option 1: Host on Your Own Domain (Recommended)

1. Upload `revenue-calculator.html` to your web hosting
2. Access it at `https://yourdomain.com/revenue-calculator.html`
3. Embed in Framer (see below)

### Option 2: Use GitHub Pages (Free)

1. Push the file to a GitHub repository
2. Enable GitHub Pages in repository settings
3. Access at `https://yourusername.github.io/repo-name/widgets/revenue-calculator.html`
4. Embed in Framer (see below)

### Option 3: Use Netlify Drop (Fastest)

1. Go to [Netlify Drop](https://app.netlify.com/drop)
2. Drag and drop the `widgets` folder
3. Get instant live URL
4. Embed in Framer (see below)

## 🎨 Embedding in Framer

### Method 1: iframe Embed (Recommended)

1. In Framer, add an **Embed** component to your page
2. Paste this code:

```html
<iframe
  src="YOUR_HOSTED_URL/revenue-calculator.html"
  width="100%"
  height="900"
  frameborder="0"
  style="border: none; border-radius: 20px; overflow: hidden;"
></iframe>
```

3. Adjust height based on your needs (recommended: 800-1000px)

### Method 2: Full Page Embed

1. Create a new page in Framer
2. Add an Embed component that fills the entire page
3. Use the same iframe code above with `height="100vh"`

### Method 3: Modal/Popup (Advanced)

1. Create a modal/overlay in Framer
2. Add the iframe inside the modal
3. Trigger with a button: "Calculate Your Revenue Leak"

## ⚙️ Customization

### Update the Booking Link

Open `revenue-calculator.html` and find this line (around line 306):

```javascript
const bookingURL = 'https://calendly.com/your-calendar-link'; // UPDATE THIS
```

Replace with your actual booking link:
- **Calendly**: `https://calendly.com/your-name/audit`
- **Cal.com**: `https://cal.com/your-name/audit`
- **Custom form**: Link to your contact page

### Change Colors

Find the gradient backgrounds and modify the hex colors:

```css
/* Main background gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Result box (red alert) */
background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);

/* CTA button */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

**Recommended color schemes:**
- **Tech/SaaS**: `#667eea` → `#764ba2` (current)
- **Finance**: `#1e3a8a` → `#3b82f6`
- **Agency**: `#ec4899` → `#8b5cf6`
- **Professional**: `#0f172a` → `#475569`

### Modify Calculation Logic

The improvement rate is currently 12.5% (conservative). To change:

```javascript
// Line ~280
const improvedCloseRate = Math.min(closeRate * 1.125, 100);

// Change to 15% improvement:
const improvedCloseRate = Math.min(closeRate * 1.15, 100);

// Change to 20% improvement:
const improvedCloseRate = Math.min(closeRate * 1.20, 100);
```

### Update Text & Copy

1. **Headline**: Change line 19-20
2. **Subtitle**: Change line 21
3. **Input labels**: Change lines 24, 31, 38
4. **CTA button**: Change line 54
5. **Assumptions box**: Change lines 58-61

## 📱 Testing

Test locally:
```bash
cd widgets
python3 -m http.server 8000
```

Then open: `http://localhost:8000/revenue-calculator.html`

## 🎯 Best Practices for Lead Generation

### 1. Traffic Source Optimization
- Drive traffic from:
  - LinkedIn posts/ads
  - Email campaigns
  - Landing pages
  - Blog posts about revenue optimization

### 2. Placement Strategy
- **Homepage**: Feature prominently above the fold
- **Landing page**: Dedicated page for the calculator
- **Blog posts**: Embed in relevant articles
- **Email**: Link to calculator page

### 3. Follow-Up Sequence
When someone clicks "Book Free Audit":
1. Immediate booking confirmation
2. Pre-audit questionnaire (gather more info)
3. Reminder email 24h before
4. Follow-up if no-show

### 4. A/B Testing Ideas
- Different improvement percentages (10%, 15%, 20%)
- Different CTAs ("Book Audit" vs "Fix This Now" vs "Get Help")
- Different color schemes
- Different urgency messaging

## 📈 Tracking & Analytics

### Add Google Analytics

Add this before the closing `</head>` tag:

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

### Track Calculator Usage

The widget already includes event tracking for the CTA button (line 315-319). Make sure GA is installed to capture these events.

### Track Conversions
- Calculator page views
- Calculator engagement (input changes)
- CTA button clicks
- Actual bookings completed

## 🔧 Troubleshooting

### Calculator not showing in Framer
- Make sure the iframe height is sufficient (900px+)
- Check that the URL is accessible (test in incognito)
- Verify no CORS issues (host on same domain if possible)

### Styling looks off
- Some platforms strip certain CSS. If this happens, host the file externally
- Ensure the iframe has no width/height constraints
- Try adding `!important` to critical styles

### Button not working
- Update the `bookingURL` variable (line 306)
- Check browser console for errors
- Test the booking link separately

## 💡 Advanced Features (Optional)

### Add Email Capture Before Booking

Replace the booking function with:

```javascript
function bookAudit() {
    const email = prompt('Enter your email to book your free audit:');
    if (email && email.includes('@')) {
        // Send to your email capture system
        // Then redirect to booking
        window.open(bookingURL, '_blank');
    }
}
```

### Integrate with CRM

Use a webhook or API to send calculator data to your CRM:

```javascript
function calculateRevenueLeak() {
    // ... existing code ...

    // Send to CRM
    fetch('https://your-api.com/calculator-submission', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            leads: leads,
            dealSize: dealSize,
            closeRate: closeRate,
            revenueLeak: revenueLeak,
            timestamp: new Date().toISOString()
        })
    });
}
```

## 📞 Support

For questions or customization help, refer to the main ResultantAI documentation.

## 🎯 Conversion Optimization Tips

1. **Pre-fill with industry averages** to reduce friction
2. **Add social proof** below the calculator ("Join 500+ businesses...")
3. **Create urgency** ("Limited audit slots available this month")
4. **Show testimonials** after calculation
5. **Offer guarantee** ("If we don't find $X in revenue leaks, the audit is free")

---

**Built by ResultantAI** | Last updated: 2025-01-19
