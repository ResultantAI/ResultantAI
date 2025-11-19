/**
 * Smart Calendly Routing Configuration
 * =====================================
 *
 * This configuration enables intelligent calendar routing based on:
 * - Lead value (revenue leak amount)
 * - Company size (monthly leads)
 * - Urgency indicators
 *
 * YOUR COMPETITIVE ADVANTAGE:
 * While competitors book everyone the same way, you'll route:
 * - High-value leads ($100K+ leak) → Priority calendar (30min)
 * - Mid-value leads ($25K-$100K) → Standard calendar (30min)
 * - Low-value leads (<$25K) → Group workshop or self-serve
 */

const SmartBookingConfig = {
    // =================================================================
    // CALENDLY EVENT LINKS
    // =================================================================
    // Set these up in Calendly under "Event Types"

    calendly: {
        // High-value leads: Your best time slots, 30min deep dive
        vip: 'https://calendly.com/your-name/vip-revenue-audit',

        // Standard leads: Regular 30min call
        standard: 'https://calendly.com/your-name/revenue-audit',

        // Discovery leads: 15min quick chat or group session
        discovery: 'https://calendly.com/your-name/15min-discovery',

        // Group workshop: For smaller leads, monthly group sessions
        workshop: 'https://calendly.com/your-name/group-workshop'
    },

    // =================================================================
    // ROUTING RULES
    // =================================================================

    routing: {
        // VIP tier: High-value opportunities
        vip: {
            minRevenueLeak: 100000,  // $100K+ annual leak
            minMonthlyLeads: 50,     // 50+ leads/month
            priority: 1
        },

        // Standard tier: Good fit, worth personal attention
        standard: {
            minRevenueLeak: 25000,   // $25K+ annual leak
            minMonthlyLeads: 20,     // 20+ leads/month
            priority: 2
        },

        // Discovery tier: Might be good fit, need qualification
        discovery: {
            minRevenueLeak: 10000,   // $10K+ annual leak
            minMonthlyLeads: 10,     // 10+ leads/month
            priority: 3
        },

        // Workshop tier: Group setting or self-serve
        workshop: {
            minRevenueLeak: 0,       // Everyone else
            minMonthlyLeads: 0,
            priority: 4
        }
    },

    // =================================================================
    // PRE-FILL DATA
    // =================================================================
    // Data to pass to Calendly for context

    buildCalendlyUrl: function(tier, leadData) {
        const baseUrl = this.calendly[tier];

        // Calendly URL parameters for pre-filling
        const params = new URLSearchParams({
            // Basic info
            name: leadData.name || '',
            email: leadData.email || '',

            // Custom questions (set these up in Calendly)
            'a1': leadData.monthlyLeads || '',           // Monthly leads
            'a2': leadData.averageDealSize || '',        // Avg deal size
            'a3': leadData.currentCloseRate || '',       // Close rate
            'a4': leadData.revenueLeak || '',            // Calculated leak
            'a5': leadData.company || '',                // Company name
            'a6': leadData.website || '',                // Website
            'a7': leadData.biggestChallenge || ''        // Their challenge
        });

        return `${baseUrl}?${params.toString()}`;
    },

    // =================================================================
    // INTELLIGENT ROUTING LOGIC
    // =================================================================

    determineRoute: function(leadData) {
        const leak = leadData.revenueLeak || 0;
        const leads = leadData.monthlyLeads || 0;

        // Check VIP criteria
        if (leak >= this.routing.vip.minRevenueLeak &&
            leads >= this.routing.vip.minMonthlyLeads) {
            return {
                tier: 'vip',
                reason: 'High-value opportunity',
                priority: 1
            };
        }

        // Check Standard criteria
        if (leak >= this.routing.standard.minRevenueLeak &&
            leads >= this.routing.standard.minMonthlyLeads) {
            return {
                tier: 'standard',
                reason: 'Good fit for personal audit',
                priority: 2
            };
        }

        // Check Discovery criteria
        if (leak >= this.routing.discovery.minRevenueLeak &&
            leads >= this.routing.discovery.minMonthlyLeads) {
            return {
                tier: 'discovery',
                reason: 'Qualification call needed',
                priority: 3
            };
        }

        // Default to workshop
        return {
            tier: 'workshop',
            reason: 'Group session recommended',
            priority: 4
        };
    },

    // =================================================================
    // MESSAGING BY TIER
    // =================================================================

    messages: {
        vip: {
            heading: '🎯 Priority Booking - Reserved for You',
            subheading: 'Based on your potential ${{leak}} annual increase, you qualify for a priority audit slot.',
            buttonText: 'Book Your VIP Audit Now',
            guarantee: 'If we don\'t find at least ${{leak}} in opportunities, the audit is free.'
        },

        standard: {
            heading: '📅 Book Your Free Revenue Audit',
            subheading: 'Let\'s discuss how to capture that ${{leak}}/year you\'re leaving on the table.',
            buttonText: 'Schedule Your Audit',
            guarantee: 'No-obligation, 30-minute strategy session.'
        },

        discovery: {
            heading: '💡 Quick Discovery Call',
            subheading: 'Let\'s explore if we can help you capture that ${{leak}} opportunity.',
            buttonText: 'Book 15-Min Discovery',
            guarantee: 'Quick chat to see if we\'re a good fit.'
        },

        workshop: {
            heading: '🎓 Join Our Group Workshop',
            subheading: 'Learn proven strategies to increase close rates in our monthly group session.',
            buttonText: 'Reserve Workshop Seat',
            guarantee: 'Interactive session with other business owners.'
        }
    },

    // =================================================================
    // WEBHOOK / CRM INTEGRATION
    // =================================================================

    sendToWebhook: async function(leadData, bookingTier) {
        // Send to Make.com, Zapier, or your Flask API
        const webhookUrl = 'YOUR_WEBHOOK_URL'; // Replace with your webhook

        try {
            const response = await fetch(webhookUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    timestamp: new Date().toISOString(),
                    tier: bookingTier,
                    lead: leadData,
                    source: 'revenue_calculator',
                    action: 'booking_initiated'
                })
            });

            console.log('Lead data sent to webhook:', response.ok);
            return response.ok;

        } catch (error) {
            console.error('Failed to send to webhook:', error);
            return false;
        }
    },

    // =================================================================
    // ENRICHMENT TRIGGER
    // =================================================================
    // Automatically enrich the lead using your existing API

    enrichLead: async function(leadData) {
        if (!leadData.website) return leadData;

        try {
            // Call your existing /enrich endpoint
            const domain = new URL(leadData.website).hostname.replace('www.', '');

            const response = await fetch('http://localhost:5000/enrich', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    domain: domain,
                    company: leadData.company
                })
            });

            if (response.ok) {
                const enrichedData = await response.json();
                return {
                    ...leadData,
                    enriched: true,
                    ...enrichedData
                };
            }

        } catch (error) {
            console.error('Enrichment failed:', error);
        }

        return leadData;
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SmartBookingConfig;
}
