# Flask API Server for Make.com Integration

Simple Flask server that exposes Python scripts as REST API endpoints for Make.com automation.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   # Make sure .env file has:
   ANTHROPIC_API_KEY=your_key_here
   ```

3. **Run the server:**
   ```bash
   python server.py
   ```

   Server starts on `http://localhost:5000`

## API Endpoints

### Health Check
```bash
GET /health
```

### Marketing Audit
```bash
POST /audit
Content-Type: application/json

{
  "url": "https://example.com",
  "industry": "SaaS"
}
```

### Lead Enrichment
```bash
POST /enrich
Content-Type: application/json

{
  "domain": "stripe.com",
  "company": "Stripe"
}
```

### MCA Qualification
```bash
POST /qualify
Content-Type: application/json

{
  "company_name": "Acme Corp",
  "annual_revenue": 500000,
  "credit_score": 650,
  "business_age_months": 24,
  "industry": "Retail"
}
```

## Make.com Integration

1. **Add HTTP Module** in Make.com
2. **Set URL:** `http://your-server:5000/audit` (or /enrich, /qualify)
3. **Method:** POST
4. **Headers:**
   - Content-Type: `application/json`
5. **Body:** Map your Make.com data to the required JSON fields
6. **Parse response:** Output is JSON that you can use in subsequent modules

## Production Deployment

For production, use gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 180 server:app
```

Options:
- `-w 4` = 4 worker processes
- `--timeout 180` = 3 minute timeout (scripts can take time)
- `-b 0.0.0.0:5000` = bind to all interfaces on port 5000

## Environment Variables

- `PORT` - Server port (default: 5000)
- `DEBUG` - Enable Flask debug mode (default: False)
- `ANTHROPIC_API_KEY` - Required for all endpoints
- `MODEL_NAME` - Claude model to use (default: claude-sonnet-4-5-20250929)
- `MAX_TOKENS` - Max response tokens (default: 4096)

## Error Handling

All endpoints return JSON with proper HTTP status codes:

- `200` - Success
- `400` - Bad request (missing fields, invalid JSON)
- `404` - Endpoint not found
- `500` - Script execution error
- `504` - Script timeout

Errors include a `timestamp` and detailed `error` message for debugging.

## CORS

CORS is enabled for all origins to support Make.com and other webhook services.

## Logging

- Server logs to stderr
- Script progress messages are captured and logged
- Each request is logged with timestamp and input data
