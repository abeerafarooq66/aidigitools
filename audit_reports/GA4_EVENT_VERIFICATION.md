# GA4 Event Implementation & DebugView Verification Register

**Measurement ID:** `G-NE094X2Q7H`  
**Standard Reference:** *Universal Web Search & SEO Master Book V2*  
**Architecture:** Document-Level Beacon Delegation & Conversion Integrity  

---

## 1. Event Taxonomy & Anti-Double-Counting Governance

To prevent double-counting in Google Analytics 4, the event architecture establishes a strict hierarchy separating **Canonical Key Events (Conversions)** from **Secondary Diagnostic Events**:

| Event Name | Event Classification | Marked as Key Event in GA4? | Trigger Condition | Emitted Payload Parameters |
| :--- | :--- | :--- | :--- | :--- |
| **`wa_concierge_checkout`** | **Primary Macro-Conversion (Key Event)** | **YES (Key Event)** | Clicks on any WhatsApp checkout link (`wa.me/923326861112`) | `tool_name`, `value`, `currency: 'PKR'`, `link_url`, `page_location`, `transport_type: 'beacon'` |
| `whatsapp_click` | Secondary Diagnostic Event | **NO** (Do not toggle in GA4 Admin) | Same link click (for legacy attribution) | Same payload |
| **`initiate_quick_order`** | **Primary Micro-Conversion** | Optional Micro-Key Event | Clicks on Quick Order modal trigger buttons | `tool_slug`, `page_location`, `transport_type: 'beacon'` |
| `quick_order_click` | Secondary Diagnostic Event | **NO** (Diagnostic only) | Same button click | Same payload |
| **`select_payment_rail`** | **Funnel Step Interaction** | **NO** (Step telemetry) | Selecting a payment rail pill (SadaPay, NayaPay, EasyPaisa, etc.) in `cart.js` | `payment_rail`, `tool_slug`, `tool_name`, `currency: 'PKR'`, `value`, `transport_type: 'beacon'` |

> [!IMPORTANT]
> **Anti-Double-Counting Rule:** Only toggle `wa_concierge_checkout` as a **Key Event** in GA4 Admin (`Admin > Data display > Events > Mark as key event`). Keep `whatsapp_click` as an untoggled normal event. This guarantees that each conversion is counted exactly once in attribution models.

---

## 2. Real-Time DebugView Verification Procedure

To inspect live event telemetry in GA4 DebugView without waiting for 24-hour standard reports:

1. **Activate GA4 Debug Mode:**
   Append `?_dbg=1` to any page URL or enable the **Google Analytics Debugger** Chrome extension.
   Alternatively, open browser DevTools console and execute:
   ```javascript
   gtag('config', 'G-NE094X2Q7H', { 'debug_mode': true });
   ```
2. **Open GA4 DebugView:**
   Navigate to **Google Analytics > Admin > Data display > DebugView**.
3. **Execute Conversion Actions:**
   - Click `"Inquire on WhatsApp"` or any tool's WhatsApp order button.
   - Inspect the incoming event stream:
     - Verify event `wa_concierge_checkout` arrives in the timeline with green flag.
     - Inspect parameters: `currency: "PKR"`, `value: 2300`, `tool_name: "ChatGPT Plus"`.
   - Open Quick Order modal on an active tool (e.g. Cursor Pro).
     - Verify event `initiate_quick_order` arrives with parameter `tool_slug: "cursor-pro"`.
   - Switch payment rail from SadaPay to EasyPaisa in the cart drawer.
     - Verify event `select_payment_rail` arrives with parameter `payment_rail: "EasyPaisa"`.
4. **Network Beacon Verification:**
   In DevTools Network tab, filter for `collect?v=2`:
   - Inspect the request payload to `https://www.google-analytics.com/g/collect`
   - Confirm status `204 No Content`
   - Confirm `transport: beacon` (guaranteeing telemetry survives page unload when user jumps to `wa.me`).

---

## 3. Code Verification Status

- `assets/analytics-events.js`: Implemented with document-level event delegation and `transport_type: 'beacon'`.
- `assets/cart.js`: `window.selectCartRail` instrumented with `select_payment_rail` and `payment_rail_selected`.
- `tools/*.html` & `index.html`: Header includes `gtag('config', 'G-NE094X2Q7H')` with deferred `analytics-events.js`.
