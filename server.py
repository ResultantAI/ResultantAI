#!/usr/bin/env python3
"""
Flask API Server for Make.com Integration
==========================================
Production-ready Flask server that exposes Python scripts as REST APIs.

Endpoints:
    POST /audit      - Run marketing_audit.py
    POST /enrich     - Run lead_enrichment.py
    POST /qualify    - Run mca_qualification.py
    GET  /health     - Health check

Usage:
    python server.py

    Or with gunicorn:
    gunicorn -w 4 -b 0.0.0.0:5000 server:app
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from typing import Dict, Any, Tuple

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

# ============================================================================
# FLASK APP CONFIGURATION
# ============================================================================

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Enable CORS for Make.com and other external services
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configuration
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Script paths (assuming they're in the same directory)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(SCRIPT_DIR, 'venv', 'bin', 'python3')

# Use venv python if available, otherwise system python
PYTHON_CMD = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def run_python_script(script_name: str, input_data: Dict[str, Any], timeout: int = 120) -> Tuple[Dict[str, Any], int]:
    """
    Run a Python script with JSON input via stdin.

    Args:
        script_name: Name of the Python script to run
        input_data: Dictionary to pass as JSON to the script
        timeout: Maximum execution time in seconds

    Returns:
        Tuple of (response_dict, http_status_code)
    """
    script_path = os.path.join(SCRIPT_DIR, script_name)

    # Verify script exists
    if not os.path.exists(script_path):
        return {
            'error': f'Script not found: {script_name}',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }, 500

    try:
        # Convert input to JSON
        input_json = json.dumps(input_data)

        # Log request (to stderr for production logging)
        print(f"[{datetime.utcnow().isoformat()}] Running {script_name}", file=sys.stderr)
        print(f"[{datetime.utcnow().isoformat()}] Input: {input_json}", file=sys.stderr)

        # Run script with JSON input via stdin
        process = subprocess.Popen(
            [PYTHON_CMD, script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=SCRIPT_DIR,
            text=True
        )

        # Send input and get output
        stdout, stderr = process.communicate(input=input_json, timeout=timeout)

        # Log stderr (script progress messages)
        if stderr:
            print(f"[{datetime.utcnow().isoformat()}] Script stderr:\n{stderr}", file=sys.stderr)

        # Check exit code
        if process.returncode != 0:
            return {
                'error': f'Script execution failed with exit code {process.returncode}',
                'script': script_name,
                'stderr': stderr,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }, 500

        # Parse JSON output
        try:
            result = json.loads(stdout)
            print(f"[{datetime.utcnow().isoformat()}] {script_name} completed successfully", file=sys.stderr)
            return result, 200

        except json.JSONDecodeError as e:
            return {
                'error': 'Failed to parse script output as JSON',
                'script': script_name,
                'parse_error': str(e),
                'stdout': stdout[:500],  # First 500 chars for debugging
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }, 500

    except subprocess.TimeoutExpired:
        process.kill()
        return {
            'error': f'Script execution timed out after {timeout} seconds',
            'script': script_name,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }, 504

    except Exception as e:
        return {
            'error': f'Unexpected error running script: {str(e)}',
            'script': script_name,
            'error_type': type(e).__name__,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }, 500


def validate_json_request() -> Tuple[Dict[str, Any], int, bool]:
    """
    Validate that request has valid JSON body.

    Returns:
        Tuple of (data_or_error, status_code, is_valid)
    """
    if not request.is_json:
        return {
            'error': 'Content-Type must be application/json',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }, 400, False

    try:
        data = request.get_json()
        if not data:
            return {
                'error': 'Request body is empty',
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }, 400, False
        return data, 200, True

    except Exception as e:
        return {
            'error': f'Invalid JSON: {str(e)}',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }, 400, False


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return jsonify({
        'status': 'healthy',
        'service': 'resultant-ai-api',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'python_version': sys.version,
        'scripts_available': {
            'marketing_audit': os.path.exists(os.path.join(SCRIPT_DIR, 'marketing_audit.py')),
            'lead_enrichment': os.path.exists(os.path.join(SCRIPT_DIR, 'lead_enrichment.py')),
            'mca_qualification': os.path.exists(os.path.join(SCRIPT_DIR, 'mca_qualification.py'))
        }
    }), 200


@app.route('/audit', methods=['POST'])
def audit():
    """
    Run marketing audit on a company website.

    Expected JSON:
    {
        "url": "https://example.com",
        "industry": "SaaS"
    }
    """
    # Validate request
    data, status, is_valid = validate_json_request()
    if not is_valid:
        return jsonify(data), status

    # Validate required fields
    if 'url' not in data or 'industry' not in data:
        return jsonify({
            'error': 'Missing required fields. Expected: url, industry',
            'received_fields': list(data.keys()),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 400

    # Run script
    result, status_code = run_python_script('marketing_audit.py', data)
    return jsonify(result), status_code


@app.route('/enrich', methods=['POST'])
def enrich():
    """
    Enrich company data and score lead.

    Expected JSON:
    {
        "domain": "stripe.com",
        "company": "Stripe" (optional)
    }
    """
    # Validate request
    data, status, is_valid = validate_json_request()
    if not is_valid:
        return jsonify(data), status

    # Validate required fields
    if 'domain' not in data:
        return jsonify({
            'error': 'Missing required field: domain',
            'received_fields': list(data.keys()),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 400

    # Run script
    result, status_code = run_python_script('lead_enrichment.py', data, timeout=90)
    return jsonify(result), status_code


@app.route('/qualify', methods=['POST'])
def qualify():
    """
    Qualify MCA application.

    Expected JSON:
    {
        "company_name": "Acme Corp",
        "annual_revenue": 500000,
        "credit_score": 650,
        "business_age_months": 24,
        "industry": "Retail" (optional),
        "monthly_revenue": 42000 (optional),
        "existing_debt": 50000 (optional),
        "notes": "Additional context" (optional)
    }
    """
    # Validate request
    data, status, is_valid = validate_json_request()
    if not is_valid:
        return jsonify(data), status

    # Validate required fields
    required = ['company_name', 'annual_revenue', 'credit_score', 'business_age_months']
    missing = [field for field in required if field not in data]

    if missing:
        return jsonify({
            'error': f'Missing required fields: {", ".join(missing)}',
            'required_fields': required,
            'received_fields': list(data.keys()),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 400

    # Run script
    result, status_code = run_python_script('mca_qualification.py', data, timeout=60)
    return jsonify(result), status_code


@app.route('/', methods=['GET'])
def index():
    """Serve the main website."""
    return send_from_directory('static', 'index.html')


@app.route('/api', methods=['GET'])
@app.route('/api/docs', methods=['GET'])
def api_docs():
    """API documentation endpoint."""
    return jsonify({
        'service': 'Resultant AI API Server',
        'version': '1.0.0',
        'website': request.host_url,
        'endpoints': {
            'GET /': 'Main website',
            'GET /health': 'Health check',
            'GET /api/docs': 'API documentation (this page)',
            'POST /audit': 'Run marketing audit (requires: url, industry)',
            'POST /enrich': 'Enrich company data (requires: domain)',
            'POST /qualify': 'Qualify MCA application (requires: company_name, annual_revenue, credit_score, business_age_months)'
        },
        'documentation': {
            'audit': {
                'method': 'POST',
                'endpoint': '/audit',
                'description': 'Generate comprehensive marketing audit for a company website',
                'required_fields': ['url', 'industry'],
                'example': {
                    'url': 'https://example.com',
                    'industry': 'SaaS'
                }
            },
            'enrich': {
                'method': 'POST',
                'endpoint': '/enrich',
                'description': 'Enrich company data and score against ICP criteria',
                'required_fields': ['domain'],
                'optional_fields': ['company'],
                'example': {
                    'domain': 'stripe.com',
                    'company': 'Stripe'
                }
            },
            'qualify': {
                'method': 'POST',
                'endpoint': '/qualify',
                'description': 'Qualify business for Merchant Cash Advance',
                'required_fields': ['company_name', 'annual_revenue', 'credit_score', 'business_age_months'],
                'optional_fields': ['industry', 'monthly_revenue', 'existing_debt', 'notes'],
                'example': {
                    'company_name': 'Acme Corp',
                    'annual_revenue': 500000,
                    'credit_score': 650,
                    'business_age_months': 24,
                    'industry': 'Retail'
                }
            }
        }
    }), 200


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    # If the request accepts JSON, return JSON error
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({
            'error': 'Endpoint not found',
            'path': request.path,
            'method': request.method,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'available_endpoints': ['GET /', 'GET /health', 'GET /api/docs', 'POST /audit', 'POST /enrich', 'POST /qualify']
        }), 404
    # Otherwise, redirect to home page
    return send_from_directory('static', 'index.html'), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        'error': 'Method not allowed',
        'path': request.path,
        'method': request.method,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'message': str(error),
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print(f"Starting ResultantAI Server on port {PORT}...", file=sys.stderr)
    print(f"Using Python: {PYTHON_CMD}", file=sys.stderr)
    print(f"Script directory: {SCRIPT_DIR}", file=sys.stderr)
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"🌐 Website:       http://localhost:{PORT}/", file=sys.stderr)
    print(f"📚 API Docs:      http://localhost:{PORT}/api/docs", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)
    print(f"\nAPI Endpoints:", file=sys.stderr)
    print(f"  GET  http://localhost:{PORT}/health", file=sys.stderr)
    print(f"  POST http://localhost:{PORT}/enrich", file=sys.stderr)
    print(f"  POST http://localhost:{PORT}/audit", file=sys.stderr)
    print(f"  POST http://localhost:{PORT}/qualify", file=sys.stderr)
    print(f"\nPress Ctrl+C to stop\n", file=sys.stderr)

    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=DEBUG
    )
