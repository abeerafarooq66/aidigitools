# Google Merchant Center & Google Ads Reseller Compliance Invariants

## 1. Google Merchant Center Feed Standards (`merchant_feed.xml`)
1. **Dynamic Catalog Parity**:
   - Every product page in the HTML catalog must exist as a valid `<item>` in `merchant_feed.xml`.
   - The `<g:id>` must exactly match the tool slug (e.g., `chatgpt-plus`, `canva-pro`).
2. **Mandatory Feed Attributes**:
   - `<g:title>`: Clean product title devoid of spammy superlatives ("CHEAP!!", "100% FREE").
   - `<g:description>`: Clear functional description specifying genuine software capabilities and subscription tier.
   - `<g:price>`: Must match the visible on-page price in PKR (e.g. `4500 PKR`).
   - `<g:availability>`: Must be set to `in_stock`.
   - `<g:condition>`: `new`.
   - `<g:image_link>`: Absolute HTTPS link to a valid 1200x630 `.png` asset in `assets/images/`.
   - `<g:shipping>`: Valid zero-cost digital delivery nodes covering target territories (`PK`, `US`, `GB`, `AE`, `CA`).

## 2. Policy Prohibitions (Zero-Tolerance)
1. **Account-Sharing Terminology**:
   - NEVER use disallowed terms: "shared account", "profile PIN", "slot", "cracked", "edu email".
   - Use compliant software industry phrasing: "Subscription Activation Service", "Workspace Seat", "Verified Account Concierge".
2. **Fake Physical Storefronts**:
   - Never fabricate physical suite or commercial office numbers in shopping feeds or contact pages.
   - Accurately describe the business as an *"Online Digital Operations Desk, Islamabad & Nationwide Digital Service, Pakistan"*.
3. **Transparent Payment & Refund Disclosure**:
   - Provide clear refund, return, and warranty policies on every product card and dedicated policy document.

## 3. Google Ads Reseller & Informational Site Policy
1. **Above-the-Fold Reseller Notice**:
   - To comply with Google's Reseller Policy regarding third-party brands and trademarks, every tool product page must render an above-the-fold disclaimer:
     > *"Independent Reseller & Service Desk: AIDigiTools is an independent subscription concierge and digital marketplace. All product names, logos, and trademarks belong to their respective owners. We are not directly affiliated with or endorsed by upstream tool providers."*
2. **Fair Use & Non-Deceptive Branding**:
   - Do not imply official sponsorship or partnership where none exists.
   - Clearly delineate reseller concierge services from original software development.
