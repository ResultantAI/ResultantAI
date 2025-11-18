# ResultantAI Website & API Deployment Guide

Complete guide for deploying the ResultantAI Revenue Recovery System website and API to production.

---

## 🚀 Quick Start (Local Development)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 3. Start the server
python server.py

# 4. Visit the website
open http://localhost:5000
```

---

## 📋 What's Included

### **Website** (Revenue Recovery System)
- **URL:** `http://localhost:5000/`
- Modern, conversion-focused landing page
- Interactive revenue loss calculator
- Live AI tool demos
- Mobile-responsive design

### **API Endpoints**
- `GET /` - Main website
- `GET /health` - Health check
- `GET /api/docs` - API documentation
- `POST /enrich` - Lead enrichment & scoring
- `POST /audit` - Marketing audit analysis
- `POST /qualify` - MCA qualification assessment

---

## 🌐 Production Deployment Options

### Option 1: Railway (Recommended for MVP)

**Why Railway:**
- ✅ One-click deploy from GitHub
- ✅ Automatic HTTPS
- ✅ Environment variable management
- ✅ Free tier available ($5/month after free tier)

**Steps:**

1. **Push code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Add ResultantAI website and API"
   git push origin main
   ```

2. **Deploy to Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your ResultantAI repository
   - Add environment variable: `ANTHROPIC_API_KEY=your_key_here`
   - Railway will auto-detect Python and deploy

3. **Configure domain** (optional)
   - Go to Settings → Domains
   - Add your custom domain or use Railway's free `.up.railway.app` domain

4. **Done!** Your site is live at `https://your-app.up.railway.app`

---

### Option 2: Heroku

**Why Heroku:**
- ✅ Battle-tested platform
- ✅ Easy scaling
- ✅ Great documentation

**Steps:**

1. **Create `Procfile`**
   ```bash
   echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT --timeout 180 server:app" > Procfile
   ```

2. **Create `runtime.txt`**
   ```bash
   echo "python-3.11.14" > runtime.txt
   ```

3. **Deploy**
   ```bash
   heroku create resultantai
   heroku config:set ANTHROPIC_API_KEY=your_key_here
   git push heroku main
   heroku open
   ```

---

### Option 3: Digital Ocean App Platform

**Why Digital Ocean:**
- ✅ Predictable pricing ($5/month)
- ✅ Full control
- ✅ Good performance

**Steps:**

1. **Go to App Platform**
   - Log into Digital Ocean
   - Create New App → GitHub
   - Select ResultantAI repo

2. **Configure Build Settings**
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn -w 4 -b 0.0.0.0:8080 --timeout 180 server:app`

3. **Add Environment Variables**
   - `ANTHROPIC_API_KEY` = your key
   - `PORT` = 8080

4. **Deploy**
   - Click "Create Resources"
   - Your app will be live at `https://your-app.ondigitalocean.app`

---

### Option 4: AWS Elastic Beanstalk

**Why AWS:**
- ✅ Enterprise-grade
- ✅ Auto-scaling
- ✅ AWS ecosystem integration

**Steps:**

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB**
   ```bash
   eb init -p python-3.11 resultantai
   ```

3. **Create environment**
   ```bash
   eb create production
   eb setenv ANTHROPIC_API_KEY=your_key_here
   ```

4. **Deploy**
   ```bash
   eb deploy
   eb open
   ```

---

### Option 5: Self-Hosted (VPS)

**Why Self-Hosted:**
- ✅ Full control
- ✅ Lowest cost at scale
- ✅ Custom configurations

**Requirements:**
- Ubuntu 22.04+ server
- Domain name (optional)

**Steps:**

1. **SSH into your server**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```

3. **Clone repository**
   ```bash
   cd /var/www
   sudo git clone https://github.com/ResultantAI/ResultantAI.git
   cd ResultantAI
   ```

4. **Setup Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure environment**
   ```bash
   sudo nano .env
   # Add: ANTHROPIC_API_KEY=your_key_here
   ```

6. **Setup Gunicorn service**
   ```bash
   sudo nano /etc/systemd/system/resultantai.service
   ```

   Add:
   ```ini
   [Unit]
   Description=ResultantAI Flask App
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/ResultantAI
   Environment="PATH=/var/www/ResultantAI/venv/bin"
   ExecStart=/var/www/ResultantAI/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 --timeout 180 server:app

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start service**
   ```bash
   sudo systemctl start resultantai
   sudo systemctl enable resultantai
   sudo systemctl status resultantai
   ```

8. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/resultantai
   ```

   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_read_timeout 180s;
       }

       location /static {
           alias /var/www/ResultantAI/static;
           expires 30d;
       }
   }
   ```

9. **Enable site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/resultantai /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

10. **Setup SSL (Optional but recommended)**
    ```bash
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d your-domain.com
    ```

11. **Done!** Your site is live at `https://your-domain.com`

---

## 🔒 Environment Variables

Required environment variables for production:

```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional (with defaults)
PORT=5000                                    # Server port
DEBUG=False                                  # Debug mode (set to False in production)
MODEL_NAME=claude-sonnet-4-5-20250929       # Claude model
MAX_TOKENS=4096                              # Max response tokens
REQUEST_TIMEOUT=30                           # API request timeout (seconds)
```

---

## 🔍 Health Checks & Monitoring

### Health Check Endpoint

```bash
curl https://your-domain.com/health
```

Response:
```json
{
  "status": "healthy",
  "service": "resultant-ai-api",
  "timestamp": "2025-11-18T22:00:00.000Z",
  "python_version": "3.11.14",
  "scripts_available": {
    "marketing_audit": true,
    "lead_enrichment": true,
    "mca_qualification": true
  }
}
```

### Monitoring Setup

**Use health endpoint for:**
- Uptime monitoring (UptimeRobot, Pingdom, etc.)
- Load balancer health checks
- CI/CD deployment verification

**Recommended tools:**
- [UptimeRobot](https://uptimerobot.com/) - Free uptime monitoring
- [Sentry](https://sentry.io/) - Error tracking
- [LogDNA](https://logdna.com/) - Log management

---

## 📊 Performance Optimization

### 1. **Enable Caching**

Add caching for static assets in Nginx:

```nginx
location /static {
    alias /var/www/ResultantAI/static;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### 2. **Use Gunicorn Workers**

Scale based on: `(2 x CPU cores) + 1`

```bash
# For 2 CPU cores:
gunicorn -w 5 -b 0.0.0.0:5000 server:app

# For 4 CPU cores:
gunicorn -w 9 -b 0.0.0.0:5000 server:app
```

### 3. **Set Appropriate Timeouts**

Claude API calls can take 30-60 seconds:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 180 server:app
```

### 4. **Enable Compression**

Add to Nginx config:

```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;
```

---

## 🛡️ Security Best Practices

### 1. **Protect API Keys**
- ✅ Never commit `.env` to git
- ✅ Use environment variables in production
- ✅ Rotate keys regularly

### 2. **HTTPS Only**
- ✅ Use Let's Encrypt for free SSL
- ✅ Force HTTPS redirects
- ✅ Set HSTS headers

### 3. **Rate Limiting**

Install rate limiting:
```bash
pip install flask-limiter
```

Add to `server.py`:
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)

@app.route('/enrich', methods=['POST'])
@limiter.limit("10 per minute")
def enrich():
    # ...existing code
```

### 4. **Firewall Configuration**

```bash
# Only allow HTTP, HTTPS, SSH
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 🧪 Testing Deployment

### 1. **Test Website**
```bash
curl -I https://your-domain.com
# Should return 200 OK
```

### 2. **Test Health Endpoint**
```bash
curl https://your-domain.com/health
# Should return JSON with status: "healthy"
```

### 3. **Test API**
```bash
curl -X POST https://your-domain.com/enrich \
  -H "Content-Type: application/json" \
  -d '{"domain": "stripe.com"}'
```

### 4. **Test Revenue Calculator**
- Visit `https://your-domain.com#calculator`
- Fill in the form
- Verify calculation works

---

## 📦 Continuous Deployment

### GitHub Actions (Recommended)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Deploy to Railway
      env:
        RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
      run: |
        npm i -g @railway/cli
        railway up
```

---

## 🐛 Troubleshooting

### Issue: 502 Bad Gateway

**Solution:**
- Check if Gunicorn is running: `sudo systemctl status resultantai`
- Check Nginx error logs: `sudo tail -f /var/log/nginx/error.log`
- Restart service: `sudo systemctl restart resultantai`

### Issue: ModuleNotFoundError

**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart resultantai
```

### Issue: API Timeouts

**Solution:**
- Increase timeout in Nginx:
  ```nginx
  proxy_read_timeout 180s;
  proxy_connect_timeout 180s;
  ```
- Increase Gunicorn timeout:
  ```bash
  gunicorn --timeout 180 server:app
  ```

### Issue: CORS Errors

**Solution:** Already configured in `server.py`, but verify:
```python
CORS(app, resources={r"/*": {"origins": "*"}})
```

---

## 📈 Scaling Guidelines

### Traffic Level → Infrastructure

**< 100 requests/day:**
- Railway/Heroku free tier
- 1 Gunicorn worker

**100-1,000 requests/day:**
- Railway Hobby ($5/mo) or DO App Platform ($5/mo)
- 2-4 Gunicorn workers

**1,000-10,000 requests/day:**
- Digital Ocean Droplet ($12-24/mo)
- 4-8 Gunicorn workers
- Load balancer

**10,000+ requests/day:**
- AWS Elastic Beanstalk with auto-scaling
- CloudFront CDN
- RDS for session storage
- 8+ Gunicorn workers across multiple instances

---

## 💰 Cost Estimates

### Development (Free)
- Local: $0
- GitHub: $0
- Railway Free Tier: $0

### Production (Small - 100-500 requests/day)
- Railway Hobby: $5/month
- Domain: $12/year
- **Total:** ~$6/month

### Production (Medium - 1K-5K requests/day)
- Digital Ocean Droplet (2GB): $12/month
- Domain: $12/year
- **Total:** ~$13/month

### Production (Large - 10K+ requests/day)
- AWS Elastic Beanstalk: $30-100/month
- CloudFront CDN: $5-20/month
- RDS: $15-50/month
- **Total:** $50-170/month

---

## ✅ Post-Deployment Checklist

- [ ] Website loads at production URL
- [ ] HTTPS is working
- [ ] Health endpoint returns 200 OK
- [ ] API endpoints work (test /enrich, /audit, /qualify)
- [ ] Revenue calculator functions correctly
- [ ] Live demos work
- [ ] Mobile responsiveness verified
- [ ] Uptime monitoring configured
- [ ] Error tracking setup (Sentry)
- [ ] Backup strategy in place
- [ ] SSL certificate auto-renewal configured
- [ ] Environment variables secured
- [ ] Rate limiting tested
- [ ] CORS working for expected origins

---

## 📞 Support

**Issues?**
- GitHub Issues: [https://github.com/ResultantAI/ResultantAI/issues](https://github.com/ResultantAI/ResultantAI/issues)
- Email: support@resultantai.com

---

**🎉 Congratulations! Your ResultantAI Revenue Recovery System is now live!**

Share it with the world: `https://your-domain.com`
