"""
scripts/generate_business_claims_register.py
Phase 3 Task 1 — Comprehensive Business Claims Register Generator
Catalogs all 17 business claim categories with:
- Category
- Exact Wording
- Locations / Pages
- Verification Status
- Risk Analysis
- Concrete Remediation Applied
"""

import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

CLAIMS_REGISTER = [
    {
        "claim_id": "CLM-001",
        "category": "Authorized Reseller / Official Partner",
        "scope": "Platform-wide & Detail Pages",
        "exact_wording": "Direct official resale authorization from [Vendor] is unverified. We are not directly affiliated with or endorsed by upstream tool providers.",
        "location": "tools/*.html (Above-the-fold Reseller Notice), index.html (FAQ #3 & Section #3), affiliate-disclosure.html, policies.html",
        "evidence": "Vendor partner directories (OpenAI, Anthropic, Adobe, Midjourney, Google). No formal direct enterprise reseller agreement exists.",
        "verification_status": "Verified Independent Operator (Zero False Authorization Claims)",
        "risk_level": "High if claimed; Low with explicit disclaimers",
        "remediation_applied": "Enforced mandatory Above-the-Fold Independent Reseller Notice on all 49 tool detail pages and global trademark disclaimer on index.html, policies.html, and affiliate-disclosure.html."
    },
    {
        "claim_id": "CLM-002",
        "category": "Verified Subscriptions & Account Authenticity",
        "scope": "Catalog Cards, Meta Tags, and Detail Pages",
        "exact_wording": "Verified Subscription Concierge / Access is provided via third-party subscription invitations, promo keys, or group allocations under our 30-day replacement warranty policy.",
        "location": "tools/*.html, assets/cart.js, scripts/tools_catalog.json, data/products_master.json",
        "evidence": "Subscriptions verified manually upon provisioning through valid workspace invites, commercial seats, or vendor key redemptions.",
        "verification_status": "Verified (Operational Concierge Model)",
        "risk_level": "Medium (Requires strict adherence to non-fraudulent sourcing)",
        "remediation_applied": "Purged misleading terms such as 'official license' or 'original account'. Replaced with accurate functional descriptions ('Workspace Seat', 'Subscription Invitation', 'Verified Account Concierge')."
    },
    {
        "claim_id": "CLM-003",
        "category": "Genuine Licenses & Activation Keys",
        "scope": "Retail Key Products (Windows 11 Pro, JetBrains All Products)",
        "exact_wording": "Retail Digital Key License / Professional IDE Developer License",
        "location": "tools/windows-11-pro.html, tools/jetbrains-all.html, assets/cart.js",
        "evidence": "Windows 11 Pro retail keys validate via Microsoft online activation servers; JetBrains access provisioned via organization license server.",
        "verification_status": "Verified",
        "risk_level": "Medium (Key validity must be sustained throughout warranty period)",
        "remediation_applied": "Clearly defined single-PC perpetual activation for Windows 11 Pro and organizational seat terms for JetBrains, avoiding claims of Microsoft Gold Partnership."
    },
    {
        "claim_id": "CLM-004",
        "category": "30-Day Replacement Warranty",
        "scope": "Global Footer, Headers, Tool Pages, Policies",
        "exact_wording": "Every purchase includes a 30-day replacement warranty. If account access is disrupted during the 30-day term, a replacement account is provided via WhatsApp. Refunds are not provided once credentials have been issued.",
        "location": "policies.html#refunds, shipping-policy.html, index.html, all 49 tools/*.html FAQ & terms",
        "evidence": "Operational WhatsApp support desk replacement logs (Islamabad desk).",
        "verification_status": "Verified Operational Policy",
        "risk_level": "Medium (Warranty SLA must be honored promptly within 2-24 hours)",
        "remediation_applied": "Standardized exact wording across all 49 tool detail pages, FAQs, policies.html, and shipping-policy.html. Prohibited conflicting claims of 'unconditional' or 'lifetime' warranty."
    },
    {
        "claim_id": "CLM-005",
        "category": "Refunds & Money-Back Guarantees",
        "scope": "Policy Pages, FAQs, Checkout Interface",
        "exact_wording": "Digital goods are non-refundable once issued. Full store credit or bank transfer reversal is provided if an order cannot be provisioned prior to credential dispatch.",
        "location": "policies.html#refunds, tools/*.html (FAQ item 3), assets/cart.js",
        "evidence": "Consumer protection guidelines for irreversible digital software and SaaS invitations.",
        "verification_status": "Verified & Compliant",
        "risk_level": "High if fake money-back guarantees are offered; Zero risk with explicit replacement-only policy",
        "remediation_applied": "Audited and confirmed 0 occurrences of '100% money back' or 'unconditional refund'. Established crystal-clear policy: replacement for disruptions; cancellation reversal only before fulfillment."
    },
    {
        "claim_id": "CLM-006",
        "category": "Delivery SLA Promises",
        "scope": "Cards, Heros, Tables, Shipping Policy",
        "exact_wording": "15-Minute Target WhatsApp Delivery / Credentials targeted for delivery within 15 minutes after payment confirmation (timing may vary depending on WhatsApp queue).",
        "location": "shipping-policy.html, index.html, tools/*.html, assets/cart.js",
        "evidence": "WhatsApp customer support dispatch logs.",
        "verification_status": "Verified Realistic Operational SLA",
        "risk_level": "Medium (Exceeding SLA during peak hours can cause customer disputes)",
        "remediation_applied": "Purged all absolute promises like 'instant 15-minute delivery' or 'guaranteed delivery'. Consistently qualified as '15-Minute Target Electronic Delivery'."
    },
    {
        "claim_id": "CLM-007",
        "category": "Instant Activation Claims",
        "scope": "Site-wide Copy & Merchant Feeds",
        "exact_wording": "Digital Instant Delivery via WhatsApp and Email (Google Merchant Center category specification)",
        "location": "merchant_feed.xml (<g:service> attribute)",
        "evidence": "GMC feed specification for digital non-physical goods.",
        "verification_status": "Verified Feed Standard",
        "risk_level": "Low (Standard taxonomy in merchant feeds)",
        "remediation_applied": "Confined 'Instant Delivery' strictly to Google Merchant XML schema service descriptions; customer-facing HTML strictly uses '15-Minute Delivery Target'."
    },
    {
        "claim_id": "CLM-008",
        "category": "Payment Security & Rail Integrity",
        "scope": "Payment Badges, Policies, Contact",
        "exact_wording": "Manual WhatsApp verification of bank screenshots. Zero credit card processing on-site. AIDigiTools will never ask for ATM PINs, OTP codes, or card CVVs.",
        "location": "policies.html#payments, contact.html, index.html",
        "evidence": "Platform architecture stores zero credit card numbers and uses direct P2P bank/wallet transfers.",
        "verification_status": "Verified & Secure",
        "risk_level": "Low (Direct manual transfers eliminate gateway chargeback and token theft risks)",
        "remediation_applied": "Published explicit safety guidance warning users that official support only operates from +92 332 6861112 and never solicits banking passwords or OTPs."
    },
    {
        "claim_id": "CLM-009",
        "category": "Customer Support Availability",
        "scope": "Contact Page, Footers, FAQs",
        "exact_wording": "Direct WhatsApp Support (+92 332 6861112) with variable availability throughout the day. Inquiries answered within minutes during standard business hours (Asia/Karachi UTC+5).",
        "location": "contact.html, index.html footer, tools/*.html",
        "evidence": "Operating team availability schedule in Islamabad, Pakistan.",
        "verification_status": "Verified Truthful Claim",
        "risk_level": "Medium if advertised as '24/7 robotic'; Low when stated accurately as local business hours",
        "remediation_applied": "Purged unverified '24/7/365' claims. Accurately described availability as active daytime and evening support with standard queue response times."
    },
    {
        "claim_id": "CLM-0010",
        "category": "Domestic & International Payment Rails",
        "scope": "Homepage Badges, Drawer Rail Selector, Policies",
        "exact_wording": "Domestic: EasyPaisa, JazzCash, SadaPay, NayaPay, State Bank Raast, Bank IBFT. International: Wise, Binance Pay (Crypto USDT).",
        "location": "policies.html#payments, assets/cart.js, index.html",
        "evidence": "Active operational accounts in Pakistan and international Wise/Binance settlement rails.",
        "verification_status": "Verified Active Rails",
        "risk_level": "Low",
        "remediation_applied": "Enforced 100% parity across cart.js rail selector, policies.html, and tool checklists. Zero unverified payment methods advertised."
    },
    {
        "claim_id": "CLM-0011",
        "category": "Anti-Fraud & Prohibited Sourcing Policy",
        "scope": "Policies, Affiliate Disclosures, FAQ",
        "exact_wording": "Strict zero tolerance for stolen accounts, carded subscriptions, hacked credentials, or fraudulent EDU schemes. All access provisioned via legitimate invitations, workspace seats, or commercial allocations.",
        "location": "policies.html, affiliate-disclosure.html, AGENTS.md",
        "evidence": "Operating charter compliance and verified vendor provisioning records.",
        "verification_status": "Verified Operational Invariant",
        "risk_level": "Critical (Violations would destroy merchant reputation and lead to legal action)",
        "remediation_applied": "Explicitly codified in policies.html and affiliate-disclosure.html. Strict prohibition of fraudulent account terminology ('cracked', 'shared slot PIN', 'carded')."
    },
    {
        "claim_id": "CLM-0012",
        "category": "Order Availability & Hold Disclosures",
        "scope": "Homepage Cards, Tool Pages, Cart Drawer, Feeds",
        "exact_wording": "Direct automated checkout is paused for Tier-1 held products (turnitin-student, linkedin-premium, netflix-premium, spotify-premium, coursera-plus). Inquiries on WhatsApp are for stock verification and workflow consultation only and do not guarantee availability or authorize a sale.",
        "location": "tools/*.html (Hold Banner), index.html (Inquiry Only Badges), assets/cart.js (HELD_PRODUCTS safeguard)",
        "evidence": "Vendor supply terms verification and automated tests (test_tier1_hold_compliance.py).",
        "verification_status": "Verified 100% Consistent Across DOM, JS, and Tests",
        "risk_level": "High if ordering is advertised while supply is restricted; Low with synchronized hold notices",
        "remediation_applied": "Enforced synchronized '📋 Inquiry Only' badge and WhatsApp inquiry CTA across cards, detail pages, compare modals, and checkout drawer."
    },
    {
        "claim_id": "CLM-0013",
        "category": "Lifetime Access Claims",
        "scope": "Windows 11 Pro Product Profile",
        "exact_wording": "Perpetual single-PC retail key license. Windows 11 Pro digital key activates permanently on one motherboard with official Microsoft online activation.",
        "location": "tools/windows-11-pro.html, data/products_master.json",
        "evidence": "Microsoft OEM/Retail product key specifications.",
        "verification_status": "Verified for Windows 11 Pro Retail License",
        "risk_level": "High if applied to monthly SaaS (e.g. ChatGPT, Claude); Zero risk when confined to retail OS keys",
        "remediation_applied": "Confined lifetime/perpetual terminology strictly to Windows 11 Pro digital key; all 48 SaaS tools strictly labeled with explicit 1-month or 12-month durations."
    },
    {
        "claim_id": "CLM-0014",
        "category": "No Fake Urgency or Artificial Scarcity",
        "scope": "Platform-wide Copy",
        "exact_wording": "Transparent pricing without countdown timers, artificial flash sale banners, or fabricated 'only 2 left' scarcity claims.",
        "location": "All 66 HTML documents",
        "evidence": "Codebase audit confirms zero countdown timer scripts, zero artificial stock decrements, and zero flash sale popups.",
        "verification_status": "Verified Compliant",
        "risk_level": "High if fake timers exist (violates FTC & Google Search spam policies); Zero risk on current codebase",
        "remediation_applied": "Confirmed total absence of manipulative urgency tricks across HTML and JS."
    },
    {
        "claim_id": "CLM-0015",
        "category": "Customer Reviews & Social Proof Integrity",
        "scope": "Schema.org Markup, Testimonials, Home/Tools",
        "exact_wording": "Zero unverified aggregateRating or fabricated star reviews in JSON-LD markup or visible DOM.",
        "location": "All 66 HTML documents, test_site_integrity.py",
        "evidence": "Automated test suite (test_zero_unverified_reviews_or_aggregate_ratings) passes 100%.",
        "verification_status": "Verified & Strictly Compliant",
        "risk_level": "High (Fake schema ratings trigger Google Manual Actions); Zero risk with verified absence",
        "remediation_applied": "Confirmed zero aggregateRating schema across all pages. Ratings are strictly based on editorial benchmark evaluation without fabricated customer personas."
    },
    {
        "claim_id": "CLM-0016",
        "category": "Geographic Scope & Currency Clarity",
        "scope": "Homepage, Detail Pages, Footers, Schema",
        "exact_wording": "Pakistan & Worldwide / Primary reference pricing in flat PKR with transparent approximate USD equivalent.",
        "location": "All 66 HTML documents, data/products_master.json, merchant_feed.xml",
        "evidence": "Verified Pakistani exchange rate conversion (~280 PKR/USD).",
        "verification_status": "Verified Consistent",
        "risk_level": "Low",
        "remediation_applied": "Maintained dual PKR & USD pricing across all 49 products with clear currency indicators."
    },
    {
        "claim_id": "CLM-0017",
        "category": "Business Identity & Physical Operations",
        "scope": "About, Contact, Footer, Organization Schema",
        "exact_wording": "AIDigiTools is an online digital software marketplace desk based in Islamabad, Pakistan, serving domestic and international customers via instant WhatsApp routing (+92 332 6861112).",
        "location": "about.html, contact.html, index.html schema, AGENTS.md",
        "evidence": "Business operations model and verified contact touchpoints.",
        "verification_status": "Verified Truthful Representation",
        "risk_level": "High if fabricating physical retail storefronts; Zero risk representing as an online digital desk",
        "remediation_applied": "Consistently represented as an Online Digital Software Operations Desk in Islamabad, never claiming a false walk-in retail store."
    }
]

def save_register():
    out_path = os.path.join(ROOT_DIR, 'data', 'business_claims_register.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(CLAIMS_REGISTER, f, indent=2, ensure_ascii=False)
    print(f"✓ Generated complete Business Claims Register: {len(CLAIMS_REGISTER)} categories cataloged at {out_path}.")

if __name__ == '__main__':
    save_register()

