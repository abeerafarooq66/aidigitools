"""
Update assets/style.css with:
1. Google-approved soft typography (semitones, font-weight 600, friendly readability)
2. Ambient Orbit Emblem animation keyframes (orbit trace, satellite float, twinkle stars)
3. Dynamic Floating WhatsApp Concierge widget
4. Universal Slide-Over Quick Order / Cart Drawer
5. Enhanced Card styling with official brand logos
6. Responsive Pricing Table with clean columns and action buttons
7. Living Showcase Console with 36 tools support
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
CSS_PATH = ROOT / "assets" / "style.css"

content = CSS_PATH.read_text(encoding="utf-8")

# 1. Soften typography in existing styles
# Replace font-weight: 800 or 750 in headings with 650/600
content = re.sub(r'h1\s*\{[^}]*\}', """h1 {
  font-size: clamp(1.85rem, 3.5vw, 2.4rem);
  font-weight: 650;
  line-height: 1.25;
  letter-spacing: -0.025em;
  color: var(--text-primary);
  margin-bottom: 1.25rem;
}""", content)

content = re.sub(r'h2\s*\{[^}]*\}', """h2 {
  font-size: clamp(1.35rem, 2.5vw, 1.7rem);
  font-weight: 600;
  line-height: 1.3;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  margin-bottom: 0.85rem;
}""", content)

content = re.sub(r'h3\s*\{[^}]*\}', """h3 {
  font-size: 1.18rem;
  font-weight: 600;
  letter-spacing: -0.015em;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}""", content)

content = re.sub(r'\.section-title\s*\{[^}]*\}', """.section-title {
  font-size: clamp(1.6rem, 3vw, 2rem);
  font-weight: 650;
  letter-spacing: -0.02em;
  text-align: center;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}""", content)

content = re.sub(r'\.logo-brand-name\s*\{[^}]*\}', """.logo-brand-name {
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: var(--text-primary);
}""", content)

content = re.sub(r'\.bundle-card h2\s*\{[^}]*\}', """.bundle-card h2 {
  font-size: 1.35rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--text-primary) !important;
  margin-bottom: 0.5rem;
}""", content)

# Append comprehensive design enhancements
NEW_STYLES = """

/* ========================================================
   ORBIT EMBLEM AMBIENT ANIMATION SYSTEM
   ======================================================== */
@keyframes orbit-trace-ambient {
  0% { stroke-dashoffset: 0; }
  50% { stroke-dashoffset: 50; }
  100% { stroke-dashoffset: 0; }
}

@keyframes satellite-float {
  0%, 100% { transform: translate(0, 0) scale(1); filter: drop-shadow(0 0 2px rgba(67, 97, 238, 0.4)); }
  50% { transform: translate(-2px, -3px) scale(1.15); filter: drop-shadow(0 0 5px rgba(0, 229, 163, 0.7)); }
}

@keyframes star-twinkle {
  0%, 100% { transform: scale(1); opacity: 0.75; }
  50% { transform: scale(1.28); opacity: 1; filter: drop-shadow(0 0 3px #00E5A3); }
}

.logo-brand-icon .orbit-front,
.aidigitools-orbit-logo .orbit-front {
  stroke-dasharray: 200;
  animation: orbit-trace-ambient 6s ease-in-out infinite;
}

.logo-brand-icon .orbit-back,
.aidigitools-orbit-logo .orbit-back {
  stroke-dasharray: 200;
  animation: orbit-trace-ambient 8s ease-in-out infinite reverse;
}

.logo-brand-icon .orbit-node,
.aidigitools-orbit-logo .orbit-node {
  animation: satellite-float 3.5s ease-in-out infinite;
  transform-origin: 124px 34px;
}

.logo-brand-icon .sparkle-star,
.aidigitools-orbit-logo .sparkle-star {
  animation: star-twinkle 2.8s ease-in-out infinite;
  transform-box: fill-box;
  transform-origin: center;
}

.logo-brand-icon .sparkle-star:nth-of-type(2),
.aidigitools-orbit-logo .sparkle-star:nth-of-type(2) {
  animation-delay: 1.4s;
}

@media (prefers-reduced-motion: reduce) {
  .logo-brand-icon .orbit-front,
  .logo-brand-icon .orbit-back,
  .logo-brand-icon .orbit-node,
  .logo-brand-icon .sparkle-star,
  .aidigitools-orbit-logo .orbit-front,
  .aidigitools-orbit-logo .orbit-back,
  .aidigitools-orbit-logo .orbit-node,
  .aidigitools-orbit-logo .sparkle-star {
    animation: none !important;
  }
}

/* ========================================================
   DYNAMIC FLOATING WHATSAPP CONCIERGE WIDGET
   ======================================================== */
.floating-wa-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
  pointer-events: none;
}

.floating-wa-badge {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(16, 185, 129, 0.3);
  padding: 5px 12px;
  border-radius: 9999px;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.76rem;
  font-weight: 600;
  color: #065F46;
  pointer-events: auto;
  transition: all 0.25s ease;
  animation: wa-badge-float 4s ease-in-out infinite;
}

.floating-wa-pulse {
  width: 7px;
  height: 7px;
  background: #10B981;
  border-radius: 50%;
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  animation: pulse-ring 2s infinite;
}

.floating-wa-btn {
  pointer-events: auto;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
  color: #FFFFFF !important;
  text-decoration: none;
  padding: 12px 18px 12px 14px;
  border-radius: 9999px;
  box-shadow: 0 8px 24px rgba(37, 211, 102, 0.35), 0 2px 6px rgba(15, 23, 42, 0.08);
  font-size: 0.92rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  animation: wa-btn-float 4s ease-in-out infinite;
}

.floating-wa-btn:hover {
  transform: translateY(-4px) scale(1.03);
  box-shadow: 0 14px 30px rgba(37, 211, 102, 0.45), 0 4px 10px rgba(15, 23, 42, 0.12);
  color: #FFFFFF !important;
}

.floating-wa-btn svg {
  flex-shrink: 0;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.15));
}

@keyframes wa-btn-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

@keyframes wa-badge-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

@media (max-width: 640px) {
  .floating-wa-container {
    bottom: 16px;
    right: 16px;
  }
  .floating-wa-label {
    display: none;
  }
  .floating-wa-btn {
    padding: 12px;
    border-radius: 50%;
  }
}

/* ========================================================
   SLIDE-OVER QUICK ORDER / CART DRAWER
   ======================================================== */
.cart-drawer-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 10000;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.cart-drawer-backdrop.active {
  opacity: 1;
  pointer-events: auto;
}

.cart-drawer {
  position: fixed;
  top: 0;
  right: -460px;
  width: 100%;
  max-width: 440px;
  height: 100%;
  background: #FFFFFF;
  box-shadow: -10px 0 35px rgba(15, 23, 42, 0.15);
  z-index: 10001;
  display: flex;
  flex-direction: column;
  transition: right 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  overflow-y: auto;
}

.cart-drawer.active {
  right: 0;
}

.cart-drawer-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #F8FAFC;
}

.cart-drawer-title {
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cart-drawer-close {
  background: none;
  border: none;
  font-size: 1.6rem;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px 8px;
  line-height: 1;
  border-radius: 6px;
  transition: all 0.2s;
}

.cart-drawer-close:hover {
  background: #E2E8F0;
  color: var(--text-primary);
}

.cart-drawer-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  flex-grow: 1;
}

.cart-item-preview {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
}

.cart-item-icon {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  border-radius: 10px;
}

.cart-item-name {
  font-weight: 600;
  font-size: 1.05rem;
  color: var(--text-primary);
}

.cart-item-vendor {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.cart-section-title {
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
  margin-bottom: 0.4rem;
}

.duration-pills-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
}

.duration-pill {
  padding: 0.65rem 0.5rem;
  text-align: center;
  border: 1px solid #CBD5E1;
  background: #FFFFFF;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.84rem;
  font-weight: 500;
  transition: all 0.2s;
}

.duration-pill:hover {
  border-color: #00B4D8;
  background: #F0F9FF;
}

.duration-pill.active {
  border-color: #00B4D8;
  background: #E0F2FE;
  color: #0369A1;
  font-weight: 600;
}

.duration-discount-tag {
  display: block;
  font-size: 0.7rem;
  color: #059669;
  font-weight: 600;
}

.payment-rails-selector {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

.rail-option {
  padding: 0.6rem 0.75rem;
  border: 1px solid #CBD5E1;
  border-radius: 8px;
  background: #FFFFFF;
  font-size: 0.84rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.rail-option:hover {
  border-color: #00B4D8;
  background: #F0F9FF;
}

.rail-option.active {
  border-color: #00B4D8;
  background: #E0F2FE;
  color: #0369A1;
  font-weight: 600;
}

.cart-summary-box {
  background: #F1F5F9;
  padding: 1.25rem;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
}

.cart-summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  margin-bottom: 0.4rem;
  color: var(--text-secondary);
}

.cart-total-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding-top: 0.75rem;
  margin-top: 0.5rem;
  border-top: 1px solid #CBD5E1;
  font-weight: 600;
  font-size: 1.15rem;
  color: var(--text-primary);
}

.cart-total-pkr {
  font-size: 1.35rem;
  color: #0284C7;
  font-weight: 700;
}

.cart-sla-box {
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
  border-radius: 10px;
  padding: 0.75rem;
  font-size: 0.82rem;
  color: #065F46;
  line-height: 1.5;
}

.cart-checkout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
  color: #FFFFFF !important;
  text-decoration: none;
  padding: 1rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  box-shadow: 0 4px 14px rgba(37, 211, 102, 0.35);
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
  width: 100%;
}

.cart-checkout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(37, 211, 102, 0.45);
}

/* ========================================================
   ENHANCED TOOL CARDS WITH OFFICIAL LOGOS (PIC 2)
   ======================================================== */
.tool-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1.75rem;
  border-radius: 16px;
  background: #FFFFFF;
  border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-card);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.tool-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-card-hover);
  border-color: #00B4D8;
}

.tool-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.tool-brand-logo {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
  transition: transform 0.2s ease;
}

.tool-card:hover .tool-brand-logo {
  transform: scale(1.08);
}

.tool-cat-badge {
  font-size: 0.74rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  border-radius: 9999px;
  background: #F1F5F9;
  color: #475569;
  border: 1px solid #E2E8F0;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.tool-card-title {
  font-size: 1.22rem;
  font-weight: 600;
  letter-spacing: -0.015em;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.tool-card-vendor {
  font-size: 0.8rem;
  color: var(--text-muted);
  display: block;
  margin-bottom: 0.75rem;
}

.tool-card-desc {
  font-size: 0.92rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1.25rem;
  min-height: 44px;
}

.tool-card-checklist {
  list-style: none;
  margin: 1rem 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-size: 0.84rem;
  color: var(--text-secondary);
}

.tool-card-checklist li {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.tool-card-checklist .check-icon {
  color: #059669;
  font-weight: 700;
}

.tool-card-actions {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  margin-top: 1.25rem;
}

.tool-card-cta-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.btn-quick-order {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  background: var(--brand-gradient);
  color: #FFFFFF !important;
  font-weight: 600;
  font-size: 0.88rem;
  padding: 0.65rem 0.85rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 180, 216, 0.2);
}

.btn-quick-order:hover {
  background: var(--brand-gradient-hover);
  transform: translateY(-1.5px);
  box-shadow: 0 4px 12px rgba(0, 180, 216, 0.3);
}

.btn-wa-subtle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  background: #F0FDF4;
  color: #15803D !important;
  border: 1px solid #BBF7D0;
  font-weight: 600;
  font-size: 0.88rem;
  padding: 0.65rem 0.85rem;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-wa-subtle:hover {
  background: #DCFCE7;
  border-color: #86EFAC;
}

.tool-specs-link {
  font-size: 0.84rem;
  font-weight: 600;
  color: #0284C7;
  text-decoration: none;
  text-align: center;
  padding: 0.35rem 0;
  transition: color 0.2s;
}

.tool-specs-link:hover {
  color: #0369A1;
  text-decoration: underline;
}

/* ========================================================
   ENHANCED RESPONSIVE PRICING TABLE (PIC 3)
   ======================================================== */
.table-responsive {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  border-radius: 16px;
  border: 1px solid var(--border-subtle);
  background: #FFFFFF;
  box-shadow: var(--shadow-card);
  margin-top: 1.5rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.92rem;
}

th {
  background: #F8FAFC;
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.85rem;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  padding: 1rem 1.25rem;
  border-bottom: 2px solid #E2E8F0;
  white-space: nowrap;
}

td {
  padding: 1.15rem 1.25rem;
  border-bottom: 1px solid #F1F5F9;
  vertical-align: middle;
  color: var(--text-secondary);
}

tr:last-child td {
  border-bottom: none;
}

tr:hover td {
  background: #F8FAFC;
}

.pricing-tool-cell {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.pricing-tool-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  flex-shrink: 0;
}

.pricing-tool-info {
  display: flex;
  flex-direction: column;
}

.pricing-tool-name {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.95rem;
}

.pricing-tool-vendor {
  font-size: 0.76rem;
  color: var(--text-muted);
}

.pricing-pkr-val {
  font-weight: 650;
  color: #0284C7;
  font-size: 1rem;
}

.pricing-usd-val {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.pricing-sla-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.82rem;
  font-weight: 500;
  color: #065F46;
}

.pricing-table-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-table-order {
  padding: 0.45rem 0.85rem;
  background: var(--brand-gradient);
  color: #FFFFFF !important;
  font-size: 0.82rem;
  font-weight: 600;
  border-radius: 8px;
  text-decoration: none;
  cursor: pointer;
  border: none;
  white-space: nowrap;
  transition: all 0.2s;
}

.btn-table-order:hover {
  background: var(--brand-gradient-hover);
  transform: translateY(-1px);
}

.btn-table-specs {
  font-size: 0.82rem;
  color: var(--text-muted);
  text-decoration: none;
  white-space: nowrap;
  padding: 0.45rem 0.5rem;
}

.btn-table-specs:hover {
  color: #0284C7;
}

/* ========================================================
   LIVING SHOWCASE CONSOLE ENHANCEMENTS (PIC 1)
   ======================================================== */
.authkit-cat-filter-pills {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  overflow-x: auto;
  padding: 0.5rem 0;
  margin-bottom: 0.85rem;
  -webkit-overflow-scrolling: touch;
}

.authkit-cat-pill {
  padding: 0.4rem 0.85rem;
  border-radius: 9999px;
  font-size: 0.82rem;
  font-weight: 500;
  background: #F1F5F9;
  color: var(--text-secondary);
  border: 1px solid #E2E8F0;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.authkit-cat-pill:hover,
.authkit-cat-pill.active {
  background: #E0F2FE;
  color: #0284C7;
  border-color: #00B4D8;
  font-weight: 600;
}

.authkit-tool-select {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
  background: #FFFFFF;
  border: 1.5px solid #CBD5E1;
  border-radius: 12px;
  cursor: pointer;
  margin-bottom: 1.25rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.authkit-tool-select:focus {
  border-color: #00B4D8;
  box-shadow: 0 0 0 3px rgba(0, 180, 216, 0.15);
}

.authkit-showcase-header {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  margin-bottom: 1rem;
}

.authkit-brand-icon {
  width: 60px;
  height: 60px;
  border-radius: 14px;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
  flex-shrink: 0;
}

.authkit-showcase-actions {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  margin-top: 1rem;
}
"""

CSS_PATH.write_text(content + NEW_STYLES, encoding="utf-8")
print(f"Successfully updated {CSS_PATH} with refined typography, animations, drawer, and tables.")
