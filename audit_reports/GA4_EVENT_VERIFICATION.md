# AIDigiTools GA4 Event Specification & Verification Report
**Repository:** `abeerafarooq66/aidigitools`  
**Measurement ID:** `G-NE094X2Q7H`  
**Standard Reference:** *Universal Web Search & SEO Master Book V2*

---

## 1. Analytics Event Architecture & Reconciliation
To reconcile historical reporting discrepancies and adhere strictly to data integrity standards, all client-side event tracking has been refactored to use document-level event delegation (`e.target.closest`) with `transport_type: 'beacon'`.

### Event Mapping & Reconciliation Matrix

| Interaction | Primary Custom Event | Normalized GA4 Event | File / Location | Payload Parameters | Business Semantic Meaning |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **WhatsApp Button Click** | `wa_concierge_checkout` | `whatsapp_click` | `assets/analytics-events.js` | `tool_name`, `value` (PKR), `currency`, `link_url`, `page_location`, `transport_type: 'beacon'` | Outbound dispatch to WhatsApp concierge desk. **Not** a confirmed order. |
| **Quick Order Open** | `initiate_quick_order` | `quick_order_click` | `assets/analytics-events.js` | `tool_slug`, `page_location`, `transport_type: 'beacon'` | User opens interactive checkout drawer for a specific tool. |
| **Payment Rail Select** | `payment_rail_selected` | `select_payment_rail` | `assets/cart.js` (`selectCartRail`) | `payment_rail`, `tool_slug`, `tool_name`, `currency`, `value`, `transport_type: 'beacon'` | User toggles preferred settlement rail (SadaPay, NayaPay, EasyPaisa, etc.). |

---

## 2. Technical Implementation Verification
1. **Document-Level Event Delegation:**
   - Elements rendered dynamically by `cart.js`, category filters, or search bars are captured immediately without requiring inline listener re-binding.
2. **Beacon Transport Reliability:**
   - Setting `transport_type: 'beacon'` guarantees event transmission even if the outbound WhatsApp link initiates immediate browser navigation or tab switching.
3. **Data Provenance Separation:**
   - Outbound chat clicks and drawer interactions are strictly documented as **Inquiries & Concierge Handoffs**, resolving past synthetic multiplier inflation.
