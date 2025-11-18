// ResultantAI - Main JavaScript

// Configuration
// TODO: Update this to your deployed API URL (e.g., Railway, Heroku, etc.)
// For now, demos are disabled. The revenue calculator works without API.
const API_BASE_URL = 'https://your-api-url-here.up.railway.app'; // Change this!

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Close mobile menu when clicking on a link
    const mobileLinks = mobileMenu.querySelectorAll('a');
    mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
        });
    });

    // Setup form handlers
    setupFormHandlers();

    // Setup revenue calculator
    setupRevenueCalculator();

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Demo Tab Switching
function showDemo(demoId) {
    // Hide all demos
    document.querySelectorAll('.demo-content').forEach(demo => {
        demo.classList.add('hidden');
    });

    // Remove active class from all tabs
    document.querySelectorAll('.demo-tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Show selected demo
    const selectedDemo = document.getElementById(`demo-${demoId}`);
    if (selectedDemo) {
        selectedDemo.classList.remove('hidden');
    }

    // Add active class to selected tab
    const selectedTab = document.getElementById(`tab-${demoId}`);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
}

// Setup Form Handlers
function setupFormHandlers() {
    // Lead Enrichment Form
    const enrichForm = document.getElementById('form-enrich');
    if (enrichForm) {
        enrichForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await handleEnrichment(new FormData(enrichForm));
        });
    }

    // Marketing Audit Form
    const auditForm = document.getElementById('form-audit');
    if (auditForm) {
        auditForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await handleAudit(new FormData(auditForm));
        });
    }

    // MCA Qualification Form
    const qualifyForm = document.getElementById('form-qualify');
    if (qualifyForm) {
        qualifyForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await handleQualification(new FormData(qualifyForm));
        });
    }
}

// Handle Lead Enrichment
async function handleEnrichment(formData) {
    const loadingEl = document.getElementById('loading-enrich');
    const resultEl = document.getElementById('result-enrich');

    // Show loading, hide previous results
    loadingEl.classList.remove('hidden');
    resultEl.classList.add('hidden');
    resultEl.innerHTML = '';

    // Prepare request data
    const data = {
        domain: formData.get('domain').trim(),
    };

    if (formData.get('company')) {
        data.company = formData.get('company').trim();
    }

    try {
        const response = await fetch(`${API_BASE_URL}/enrich`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        // Hide loading
        loadingEl.classList.add('hidden');

        if (response.ok) {
            displayEnrichmentResult(result, resultEl);
        } else {
            displayError(result.error || 'An error occurred', resultEl);
        }
    } catch (error) {
        loadingEl.classList.add('hidden');
        displayError(`Network error: ${error.message}`, resultEl);
    }
}

// Handle Marketing Audit
async function handleAudit(formData) {
    const loadingEl = document.getElementById('loading-audit');
    const resultEl = document.getElementById('result-audit');

    // Show loading, hide previous results
    loadingEl.classList.remove('hidden');
    resultEl.classList.add('hidden');
    resultEl.innerHTML = '';

    // Prepare request data
    const data = {
        url: formData.get('url').trim(),
        industry: formData.get('industry')
    };

    try {
        const response = await fetch(`${API_BASE_URL}/audit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        // Hide loading
        loadingEl.classList.add('hidden');

        if (response.ok) {
            displayAuditResult(result, resultEl);
        } else {
            displayError(result.error || 'An error occurred', resultEl);
        }
    } catch (error) {
        loadingEl.classList.add('hidden');
        displayError(`Network error: ${error.message}`, resultEl);
    }
}

// Handle MCA Qualification
async function handleQualification(formData) {
    const loadingEl = document.getElementById('loading-qualify');
    const resultEl = document.getElementById('result-qualify');

    // Show loading, hide previous results
    loadingEl.classList.remove('hidden');
    resultEl.classList.add('hidden');
    resultEl.innerHTML = '';

    // Prepare request data
    const data = {
        company_name: formData.get('company_name').trim(),
        annual_revenue: parseInt(formData.get('annual_revenue')),
        credit_score: parseInt(formData.get('credit_score')),
        business_age_months: parseInt(formData.get('business_age_months'))
    };

    // Add optional fields
    if (formData.get('industry')) data.industry = formData.get('industry').trim();
    if (formData.get('monthly_revenue')) data.monthly_revenue = parseInt(formData.get('monthly_revenue'));
    if (formData.get('existing_debt')) data.existing_debt = parseInt(formData.get('existing_debt'));

    try {
        const response = await fetch(`${API_BASE_URL}/qualify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        // Hide loading
        loadingEl.classList.add('hidden');

        if (response.ok) {
            displayQualificationResult(result, resultEl);
        } else {
            displayError(result.error || 'An error occurred', resultEl);
        }
    } catch (error) {
        loadingEl.classList.add('hidden');
        displayError(`Network error: ${error.message}`, resultEl);
    }
}

// Display Enrichment Result
function displayEnrichmentResult(data, container) {
    const score = data.icp_score || data.score || 0;
    const category = data.category || getScoreCategory(score);

    let html = `
        <div class="result-card">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
                <div>
                    <h4 class="text-3xl font-bold mb-2">${data.company_name || 'Company'}</h4>
                    <p class="text-gray-600">${data.domain || ''}</p>
                </div>
                <div class="text-center mt-4 md:mt-0">
                    <div class="result-score">${score}</div>
                    <span class="badge badge-${category.toLowerCase()}">${category.toUpperCase()}</span>
                </div>
            </div>

            <div class="grid md:grid-cols-2 gap-6 mb-6">
    `;

    // Display company profile if available
    if (data.company_profile) {
        const profile = data.company_profile;
        html += `
            <div>
                <h5 class="font-bold text-lg mb-3 flex items-center">
                    <i class="fas fa-building text-primary mr-2"></i>
                    Company Profile
                </h5>
                <dl class="space-y-2 text-sm">
                    ${profile.industry ? `<div><dt class="font-semibold inline">Industry:</dt> <dd class="inline">${profile.industry}</dd></div>` : ''}
                    ${profile.company_size ? `<div><dt class="font-semibold inline">Size:</dt> <dd class="inline">${profile.company_size}</dd></div>` : ''}
                    ${profile.location ? `<div><dt class="font-semibold inline">Location:</dt> <dd class="inline">${profile.location}</dd></div>` : ''}
                    ${profile.business_model ? `<div><dt class="font-semibold inline">Model:</dt> <dd class="inline">${profile.business_model}</dd></div>` : ''}
                </dl>
            </div>
        `;
    }

    // Display ICP breakdown if available
    if (data.icp_breakdown) {
        html += `
            <div>
                <h5 class="font-bold text-lg mb-3 flex items-center">
                    <i class="fas fa-chart-bar text-accent mr-2"></i>
                    ICP Score Breakdown
                </h5>
                <div class="space-y-3">
        `;

        for (const [key, value] of Object.entries(data.icp_breakdown)) {
            const scoreValue = typeof value === 'object' ? value.score : value;
            html += `
                <div>
                    <div class="flex justify-between text-sm mb-1">
                        <span class="font-semibold capitalize">${key.replace(/_/g, ' ')}</span>
                        <span>${scoreValue}/100</span>
                    </div>
                    <div class="score-bar">
                        <div class="score-bar-fill" style="width: ${scoreValue}%"></div>
                    </div>
                </div>
            `;
        }

        html += `
                </div>
            </div>
        `;
    }

    html += `</div>`;

    // Display recommendations if available
    if (data.recommendations) {
        html += `
            <div class="bg-blue-50 border-l-4 border-blue-500 p-4 mb-4">
                <h5 class="font-bold mb-2 flex items-center">
                    <i class="fas fa-lightbulb text-blue-500 mr-2"></i>
                    Recommendations
                </h5>
                <p class="text-sm text-gray-700">${data.recommendations}</p>
            </div>
        `;
    }

    // Add JSON toggle
    html += `
            <div class="mt-6">
                <button onclick="toggleJson('enrich-json')" class="text-sm text-gray-600 hover:text-primary font-semibold">
                    <i class="fas fa-code mr-2"></i>View Full JSON Response
                </button>
                <div id="enrich-json" class="hidden mt-4">
                    <div class="json-display code-container">
                        <button onclick="copyToClipboard('enrich-json-content')" class="copy-button">
                            <i class="fas fa-copy mr-1"></i>Copy
                        </button>
                        <pre id="enrich-json-content">${JSON.stringify(data, null, 2)}</pre>
                    </div>
                </div>
            </div>
        </div>
    `;

    container.innerHTML = html;
    container.classList.remove('hidden');
}

// Display Audit Result
function displayAuditResult(data, container) {
    let html = `
        <div class="result-card">
            <h4 class="text-3xl font-bold mb-6">
                <i class="fas fa-clipboard-check text-accent mr-3"></i>
                Marketing Audit Results
            </h4>
    `;

    // SEO Analysis
    if (data.seo_analysis) {
        html += `
            <div class="mb-6">
                <h5 class="font-bold text-xl mb-3 flex items-center">
                    <i class="fas fa-search text-primary mr-2"></i>
                    SEO Analysis
                </h5>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-700 whitespace-pre-line">${formatText(data.seo_analysis)}</p>
                </div>
            </div>
        `;
    }

    // Content Strategy
    if (data.content_strategy) {
        html += `
            <div class="mb-6">
                <h5 class="font-bold text-xl mb-3 flex items-center">
                    <i class="fas fa-edit text-accent mr-2"></i>
                    Content Strategy
                </h5>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-700 whitespace-pre-line">${formatText(data.content_strategy)}</p>
                </div>
            </div>
        `;
    }

    // Quick Wins
    if (data.quick_wins) {
        html += `
            <div class="mb-6">
                <h5 class="font-bold text-xl mb-3 flex items-center">
                    <i class="fas fa-rocket text-green-500 mr-2"></i>
                    Top 3 Quick Wins
                </h5>
                <div class="bg-green-50 border-l-4 border-green-500 p-4">
        `;

        if (Array.isArray(data.quick_wins)) {
            data.quick_wins.forEach((win, index) => {
                html += `<div class="mb-3 last:mb-0">
                    <span class="font-bold text-green-700">${index + 1}.</span>
                    <span class="text-sm text-gray-700">${formatText(win)}</span>
                </div>`;
            });
        } else {
            html += `<p class="text-sm text-gray-700 whitespace-pre-line">${formatText(data.quick_wins)}</p>`;
        }

        html += `
                </div>
            </div>
        `;
    }

    // Add JSON toggle
    html += `
            <div class="mt-6">
                <button onclick="toggleJson('audit-json')" class="text-sm text-gray-600 hover:text-accent font-semibold">
                    <i class="fas fa-code mr-2"></i>View Full JSON Response
                </button>
                <div id="audit-json" class="hidden mt-4">
                    <div class="json-display code-container">
                        <button onclick="copyToClipboard('audit-json-content')" class="copy-button">
                            <i class="fas fa-copy mr-1"></i>Copy
                        </button>
                        <pre id="audit-json-content">${JSON.stringify(data, null, 2)}</pre>
                    </div>
                </div>
            </div>
        </div>
    `;

    container.innerHTML = html;
    container.classList.remove('hidden');
}

// Display Qualification Result
function displayQualificationResult(data, container) {
    const qualified = data.qualified || data.qualification_status === 'qualified';

    let html = `
        <div class="result-card">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
                <h4 class="text-3xl font-bold mb-4 md:mb-0">
                    ${data.company_name || 'Business'} Qualification
                </h4>
                <span class="badge ${qualified ? 'badge-success' : 'badge-warning'}">
                    ${qualified ? 'QUALIFIED' : 'REVIEW NEEDED'}
                </span>
            </div>
    `;

    // Qualification Score
    if (data.qualification_score !== undefined) {
        html += `
            <div class="mb-6">
                <div class="flex justify-between items-center mb-2">
                    <span class="font-bold text-lg">Qualification Score</span>
                    <span class="text-3xl font-bold gradient-text">${data.qualification_score}/100</span>
                </div>
                <div class="score-bar">
                    <div class="score-bar-fill" style="width: ${data.qualification_score}%"></div>
                </div>
            </div>
        `;
    }

    // Assessment Summary
    if (data.assessment) {
        html += `
            <div class="mb-6">
                <h5 class="font-bold text-xl mb-3 flex items-center">
                    <i class="fas fa-clipboard-list text-secondary mr-2"></i>
                    Assessment Summary
                </h5>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-700 whitespace-pre-line">${formatText(data.assessment)}</p>
                </div>
            </div>
        `;
    }

    // Risk Factors
    if (data.risk_factors) {
        html += `
            <div class="mb-6">
                <h5 class="font-bold text-xl mb-3 flex items-center">
                    <i class="fas fa-exclamation-triangle text-yellow-500 mr-2"></i>
                    Risk Factors
                </h5>
                <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4">
        `;

        if (Array.isArray(data.risk_factors)) {
            data.risk_factors.forEach(risk => {
                html += `<div class="mb-2 text-sm text-gray-700">• ${formatText(risk)}</div>`;
            });
        } else {
            html += `<p class="text-sm text-gray-700">${formatText(data.risk_factors)}</p>`;
        }

        html += `
                </div>
            </div>
        `;
    }

    // Recommendations
    if (data.recommendations) {
        html += `
            <div class="mb-6">
                <h5 class="font-bold text-xl mb-3 flex items-center">
                    <i class="fas fa-lightbulb text-blue-500 mr-2"></i>
                    Recommendations
                </h5>
                <div class="bg-blue-50 border-l-4 border-blue-500 p-4">
                    <p class="text-sm text-gray-700 whitespace-pre-line">${formatText(data.recommendations)}</p>
                </div>
            </div>
        `;
    }

    // Add JSON toggle
    html += `
            <div class="mt-6">
                <button onclick="toggleJson('qualify-json')" class="text-sm text-gray-600 hover:text-secondary font-semibold">
                    <i class="fas fa-code mr-2"></i>View Full JSON Response
                </button>
                <div id="qualify-json" class="hidden mt-4">
                    <div class="json-display code-container">
                        <button onclick="copyToClipboard('qualify-json-content')" class="copy-button">
                            <i class="fas fa-copy mr-1"></i>Copy
                        </button>
                        <pre id="qualify-json-content">${JSON.stringify(data, null, 2)}</pre>
                    </div>
                </div>
            </div>
        </div>
    `;

    container.innerHTML = html;
    container.classList.remove('hidden');
}

// Display Error
function displayError(message, container) {
    const html = `
        <div class="alert alert-error">
            <i class="fas fa-exclamation-circle mr-2"></i>
            <strong>Error:</strong> ${message}
        </div>
    `;
    container.innerHTML = html;
    container.classList.remove('hidden');
}

// Utility Functions
function getScoreCategory(score) {
    if (score >= 80) return 'Hot';
    if (score >= 60) return 'Warm';
    if (score >= 40) return 'Cold';
    return 'Poor';
}

function formatText(text) {
    if (typeof text === 'string') {
        return text.replace(/\n/g, '<br>');
    }
    return JSON.stringify(text, null, 2);
}

function toggleJson(id) {
    const element = document.getElementById(id);
    if (element) {
        element.classList.toggle('hidden');
    }
}

function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        const text = element.textContent;
        navigator.clipboard.writeText(text).then(() => {
            // Show success feedback
            const button = event.target.closest('button');
            const originalText = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check mr-1"></i>Copied!';
            setTimeout(() => {
                button.innerHTML = originalText;
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    }
}

// Revenue Calculator
function setupRevenueCalculator() {
    const form = document.getElementById('revenue-calculator');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        calculateRevenueLoss();
    });
}

function calculateRevenueLoss() {
    // Get input values
    const leadsPerMonth = parseInt(document.getElementById('leads-per-month').value);
    const dealValue = parseInt(document.getElementById('deal-value').value);
    const closeRate = parseInt(document.getElementById('close-rate').value) / 100;

    // Calculate annual leads
    const annualLeads = leadsPerMonth * 12;

    // Assumptions for revenue leak calculations
    const missedCallRate = 0.35; // 35% of leads call during off-hours
    const noVoicemailRate = 0.78; // 78% won't leave voicemail
    const missedLeads = annualLeads * missedCallRate * noVoicemailRate;
    const leak1 = missedLeads * dealValue * closeRate;

    // Leak 2: Unqualified prospects (40% of sales time wasted)
    const currentDeals = annualLeads * closeRate;
    const wastedTimeRate = 0.40; // 40% of sales time wasted on bad fits
    const timeCostPerLead = dealValue * 0.15; // Assume 15% of deal value in sales cost
    const leak2 = annualLeads * wastedTimeRate * timeCostPerLead;

    // Leak 3: Dead pipelines (60% of deals need 5+ touches, most give up after 2-3)
    const needsMultipleTouches = 0.60;
    const giveUpRate = 0.65; // 65% of multi-touch deals lost
    const potentialDeals = annualLeads * closeRate * needsMultipleTouches;
    const lostDeals = potentialDeals * giveUpRate;
    const leak3 = lostDeals * dealValue;

    // Total loss
    const totalLoss = leak1 + leak2 + leak3;

    // With our system - improved metrics
    const improvedCloseRate = Math.min(closeRate * 1.5, 0.40); // 50% improvement, capped at 40%
    const capturedLeads = missedLeads * 0.90; // Capture 90% of missed calls
    const betterQualification = wastedTimeRate * 0.30; // Reduce waste by 70%
    const betterFollowUp = lostDeals * 0.50; // Recover 50% of lost deals

    const recovered1 = capturedLeads * dealValue * improvedCloseRate;
    const recovered2 = annualLeads * (wastedTimeRate - betterQualification) * timeCostPerLead;
    const recovered3 = betterFollowUp * dealValue;
    const totalRecovered = recovered1 + recovered2 + recovered3;

    // Display results
    displayCalculatorResults({
        leadsPerMonth,
        annualLeads,
        dealValue,
        closeRate: closeRate * 100,
        leak1,
        leak2,
        leak3,
        totalLoss,
        totalRecovered,
        roi: (totalRecovered / 18000) // Assuming $18K annual fee
    });
}

function displayCalculatorResults(data) {
    const resultContainer = document.getElementById('calculator-result');

    const html = `
        <div class="text-center mb-8">
            <h3 class="text-2xl font-bold mb-4">Your Revenue Loss Analysis</h3>
            <p class="text-gray-600">Based on ${data.leadsPerMonth} leads/month at $${data.dealValue.toLocaleString()} per deal with ${data.closeRate}% close rate</p>
        </div>

        <div class="grid md:grid-cols-3 gap-6 mb-8">
            <div class="bg-red-50 p-6 rounded-lg border-2 border-red-300">
                <i class="fas fa-phone-slash text-red-500 text-3xl mb-3"></i>
                <h4 class="font-bold mb-2">Missed Calls</h4>
                <div class="text-3xl font-bold text-red-600 mb-2">$${Math.round(data.leak1).toLocaleString()}</div>
                <p class="text-sm text-gray-600">Lost per year</p>
            </div>

            <div class="bg-orange-50 p-6 rounded-lg border-2 border-orange-300">
                <i class="fas fa-user-times text-orange-500 text-3xl mb-3"></i>
                <h4 class="font-bold mb-2">Bad Fit Prospects</h4>
                <div class="text-3xl font-bold text-orange-600 mb-2">$${Math.round(data.leak2).toLocaleString()}</div>
                <p class="text-sm text-gray-600">Wasted per year</p>
            </div>

            <div class="bg-purple-50 p-6 rounded-lg border-2 border-purple-300">
                <i class="fas fa-chart-line-down text-purple-500 text-3xl mb-3"></i>
                <h4 class="font-bold mb-2">Dead Pipelines</h4>
                <div class="text-3xl font-bold text-purple-600 mb-2">$${Math.round(data.leak3).toLocaleString()}</div>
                <p class="text-sm text-gray-600">Lost per year</p>
            </div>
        </div>

        <div class="bg-gradient-to-r from-red-600 to-purple-600 text-white p-8 rounded-xl mb-8 text-center">
            <h4 class="text-xl mb-3">Total Annual Revenue Loss:</h4>
            <div class="text-6xl font-bold mb-2">$${Math.round(data.totalLoss).toLocaleString()}</div>
            <p class="text-lg">That's ${Math.round(data.totalLoss / 12).toLocaleString()}/month bleeding from your business</p>
        </div>

        <div class="bg-green-50 p-8 rounded-xl border-2 border-green-400">
            <div class="text-center mb-6">
                <i class="fas fa-hand-holding-usd text-green-600 text-5xl mb-4"></i>
                <h4 class="text-2xl font-bold mb-2">With Our Revenue Recovery System:</h4>
            </div>

            <div class="grid md:grid-cols-2 gap-6 mb-6">
                <div class="text-center p-4 bg-white rounded-lg">
                    <p class="text-sm text-gray-600 mb-2">Revenue Recovered</p>
                    <div class="text-4xl font-bold text-green-600">$${Math.round(data.totalRecovered).toLocaleString()}</div>
                </div>
                <div class="text-center p-4 bg-white rounded-lg">
                    <p class="text-sm text-gray-600 mb-2">ROI (First Year)</p>
                    <div class="text-4xl font-bold text-green-600">${Math.round(data.roi)}X</div>
                </div>
            </div>

            <div class="text-center">
                <p class="text-gray-700 mb-4">
                    <strong>Translation:</strong> For every $1 you invest, you recover $${Math.round(data.roi)} in lost revenue.
                </p>
                <a href="https://github.com/ResultantAI/ResultantAI" target="_blank" class="inline-block bg-green-600 text-white px-8 py-4 rounded-lg font-bold hover:bg-green-700 transition">
                    <i class="fas fa-rocket mr-2"></i>Stop The Bleeding Now
                </a>
            </div>
        </div>

        <div class="text-center mt-6 text-sm text-gray-600">
            <i class="fas fa-shield-check text-green-500 mr-1"></i>
            90-day ROI guarantee | This calculation is conservative - many agencies recover even more
        </div>
    `;

    resultContainer.innerHTML = html;
    resultContainer.classList.remove('hidden');

    // Scroll to results
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Export functions to window for onclick handlers
window.showDemo = showDemo;
window.toggleJson = toggleJson;
window.copyToClipboard = copyToClipboard;
