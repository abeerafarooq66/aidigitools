"""
Upgrade deals.html for AIDigiTools:
- Add official brand SVG icons for each bundled tool
- Remove old dark-theme classes (text-white, text-slate-300, font-black)
- Soft, elegant typography and refined bundle badges
- Workable dual buttons (Quick Order and Direct WhatsApp)
- 100% preservation of quick-answer, schema, and link integrity
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEALS_PATH = ROOT / "deals.html"

content = DEALS_PATH.read_text(encoding="utf-8")

# Replace the bundles grid inside <div class="grid"> ... </div>
bundles_html = """    <div class="grid">
      <!-- Bundle 1: Creator Studio Bundle -->
      <div class="bundle-card">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem;">
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <img src="assets/images/icons/chatgpt-plus.svg" alt="ChatGPT" width="36" height="36" style="border-radius:8px;">
            <img src="assets/images/icons/canva-pro.svg" alt="Canva" width="36" height="36" style="border-radius:8px;">
            <img src="assets/images/icons/capcut-pro.svg" alt="CapCut" width="36" height="36" style="border-radius:8px;">
          </div>
          <span class="bundle-badge">Top Seller</span>
        </div>
        <h2>Creator Studio Bundle</h2>
        <p>Everything required to script, design, and edit viral content at scale.</p>
        <div class="price-tag">Rs. 3,450 PKR <span class="period">(~$12 USD) / month (Save 15%)</span></div>
        <ul class="feature-list">
          <li><span class="check">✓</span> <strong><a href="tools/chatgpt-plus.html" style="color:inherit; text-decoration:none;">ChatGPT Plus</a></strong>: Scriptwriting &amp; Concept Ideation</li>
          <li><span class="check">✓</span> <strong><a href="tools/canva-pro.html" style="color:inherit; text-decoration:none;">Canva Pro</a></strong>: Thumbnails &amp; Brand Kits</li>
          <li><span class="check">✓</span> <strong><a href="tools/capcut-pro.html" style="color:inherit; text-decoration:none;">CapCut Pro Desktop</a></strong>: 4K 60fps &amp; Auto-Captions</li>
          <li><span class="check">✓</span> EasyPaisa, JazzCash, SadaPay &amp; Wise/Crypto</li>
          <li><span class="check">✓</span> 30-Day Guaranteed Replacement Warranty</li>
        </ul>
        <div style="display:flex; flex-direction:column; gap:0.5rem; margin-top:1.25rem;">
          <button type="button" class="btn-primary w-full" onclick="openQuickOrderModal('chatgpt-plus')">⚡ Quick Order Creator Bundle</button>
          <a href="https://wa.me/923326861112?text=Hi%20AIDigiTools,%20I%20want%20to%20order%20the%20Creator%20Studio%20Bundle%20for%20Rs%203450%20PKR%20/%20$12%20USD" class="btn-wa-subtle w-full" target="_blank" rel="noopener noreferrer">Order on WhatsApp</a>
        </div>
      </div>

      <!-- Bundle 2: Developer Power Suite -->
      <div class="bundle-card">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem;">
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <img src="assets/images/icons/claude-pro.svg" alt="Claude" width="36" height="36" style="border-radius:8px;">
            <img src="assets/images/icons/cursor-pro.svg" alt="Cursor" width="36" height="36" style="border-radius:8px;">
            <img src="assets/images/icons/chatgpt-plus.svg" alt="ChatGPT" width="36" height="36" style="border-radius:8px;">
          </div>
          <span class="bundle-badge" style="background:#EEF2FF; color:#4F46E5; border-color:#C7D2FE;">Dev Choice</span>
        </div>
        <h2>Developer Power Suite</h2>
        <p>The ultimate dual-engine coding workstation for full-stack engineering.</p>
        <div class="price-tag">Rs. 4,400 PKR <span class="period">(~$16 USD) / month (Save 10%)</span></div>
        <ul class="feature-list">
          <li><span class="check">✓</span> <strong><a href="tools/claude-pro.html" style="color:inherit; text-decoration:none;">Claude Pro</a></strong>: 3.5 Sonnet &amp; Artifacts Sandbox</li>
          <li><span class="check">✓</span> <strong><a href="tools/chatgpt-plus.html" style="color:inherit; text-decoration:none;">ChatGPT Plus</a></strong>: GPT-4o Canvas &amp; System Architecture</li>
          <li><span class="check">✓</span> EasyPaisa, JazzCash, SadaPay &amp; Wise/Crypto</li>
          <li><span class="check">✓</span> 15-Minute Priority WhatsApp Delivery</li>
          <li><span class="check">✓</span> 30-Day Guaranteed Replacement Warranty</li>
        </ul>
        <div style="display:flex; flex-direction:column; gap:0.5rem; margin-top:1.25rem;">
          <button type="button" class="btn-primary w-full" onclick="openQuickOrderModal('claude-pro')">⚡ Quick Order Developer Suite</button>
          <a href="https://wa.me/923326861112?text=Hi%20AIDigiTools,%20I%20want%20to%20order%20the%20Developer%20Power%20Suite%20for%20Rs%204400%20PKR%20/%20$16%20USD" class="btn-wa-subtle w-full" target="_blank" rel="noopener noreferrer">Order on WhatsApp</a>
        </div>
      </div>

      <!-- Bundle 3: Privacy & AI Pro Pack -->
      <div class="bundle-card">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem;">
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <img src="assets/images/icons/chatgpt-plus.svg" alt="ChatGPT" width="36" height="36" style="border-radius:8px;">
            <img src="assets/images/icons/nordvpn.svg" alt="NordVPN" width="36" height="36" style="border-radius:8px;">
          </div>
          <span class="bundle-badge" style="background:#ECFDF5; color:#059669; border-color:#A7F3D0;">Security Shield</span>
        </div>
        <h2>Privacy &amp; AI Pro Pack</h2>
        <p>Maximum intelligence combined with bank-grade encryption and security.</p>
        <div class="price-tag">Rs. 2,900 PKR <span class="period">(~$10 USD) / month (Save 20%)</span></div>
        <ul class="feature-list">
          <li><span class="check">✓</span> <strong><a href="tools/chatgpt-plus.html" style="color:inherit; text-decoration:none;">ChatGPT Plus</a></strong>: Full OpenAI GPT-4o Workspace</li>
          <li><span class="check">✓</span> <strong><a href="tools/nordvpn.html" style="color:inherit; text-decoration:none;">NordVPN Ultimate</a></strong>: 6,000+ Servers &amp; Threat Protection</li>
          <li><span class="check">✓</span> EasyPaisa, JazzCash, SadaPay &amp; Wise/Crypto</li>
          <li><span class="check">✓</span> Dedicated WhatsApp Setup Assistance</li>
          <li><span class="check">✓</span> 30-Day Guaranteed Replacement Warranty</li>
        </ul>
        <div style="display:flex; flex-direction:column; gap:0.5rem; margin-top:1.25rem;">
          <button type="button" class="btn-primary w-full" onclick="openQuickOrderModal('nordvpn')">⚡ Quick Order Privacy Pack</button>
          <a href="https://wa.me/923326861112?text=Hi%20AIDigiTools,%20I%20want%20to%20order%20the%20Privacy%20and%20AI%20Pro%20Pack%20for%20Rs%202900%20PKR%20/%20$10%20USD" class="btn-wa-subtle w-full" target="_blank" rel="noopener noreferrer">Order on WhatsApp</a>
        </div>
      </div>

      <!-- Bundle 4: AI Filmmaker Motion Studio -->
      <div class="bundle-card">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem;">
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <img src="assets/images/icons/google-veo.svg" alt="Google Veo" width="36" height="36" style="border-radius:8px;">
            <img src="assets/images/icons/runway-gen3.svg" alt="Runway" width="36" height="36" style="border-radius:8px;">
            <img src="assets/images/icons/capcut-pro.svg" alt="CapCut" width="36" height="36" style="border-radius:8px;">
          </div>
          <span class="bundle-badge" style="background:#FFF1F2; color:#E11D48; border-color:#FECDD3;">Cinematic FX</span>
        </div>
        <h2>AI Filmmaker Motion Studio</h2>
        <p>Generate cinematic clips and finish edits with 4K auto-caption workflows.</p>
        <div class="price-tag">Rs. 4,200 PKR <span class="period">(~$15 USD) / month (Save 15%)</span></div>
        <ul class="feature-list">
          <li><span class="check">✓</span> <strong><a href="tools/google-veo.html" style="color:inherit; text-decoration:none;">Google Veo Omni</a></strong>: High-fidelity cinematic 1080p video</li>
          <li><span class="check">✓</span> <strong><a href="tools/runway-gen3.html" style="color:inherit; text-decoration:none;">Runway Gen-3</a></strong>: Camera motion &amp; brush control</li>
          <li><span class="check">✓</span> <strong><a href="tools/capcut-pro.html" style="color:inherit; text-decoration:none;">CapCut Pro</a></strong>: 4K 60fps export &amp; auto-captions</li>
          <li><span class="check">✓</span> EasyPaisa, JazzCash, SadaPay &amp; Wise/Crypto</li>
          <li><span class="check">✓</span> 30-Day Guaranteed Replacement Warranty</li>
        </ul>
        <div style="display:flex; flex-direction:column; gap:0.5rem; margin-top:1.25rem;">
          <button type="button" class="btn-primary w-full" onclick="openQuickOrderModal('runway-gen3')">⚡ Quick Order Filmmaker Studio</button>
          <a href="https://wa.me/923326861112?text=Hi%20AIDigiTools,%20I%20want%20to%20order%20the%20Filmmaker%20Motion%20Studio%20for%20Rs%204200%20PKR%20/%20$15%20USD" class="btn-wa-subtle w-full" target="_blank" rel="noopener noreferrer">Order on WhatsApp</a>
        </div>
      </div>

      <!-- Bundle 5: AI Voice & Audio Creator Pack -->
      <div class="bundle-card">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem;">
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <img src="assets/images/icons/elevenlabs-creator.svg" alt="ElevenLabs" width="36" height="36" style="border-radius:8px;">
            <img src="assets/images/icons/suno-ai.svg" alt="Suno" width="36" height="36" style="border-radius:8px;">
          </div>
          <span class="bundle-badge" style="background:#F5F3FF; color:#7C3AED; border-color:#DDD6FE;">Audio Lab</span>
        </div>
        <h2>AI Voice &amp; Audio Creator Pack</h2>
        <p>Ultra-realistic voice cloning and complete studio music generation.</p>
        <div class="price-tag">Rs. 4,800 PKR <span class="period">(~$17 USD) / month (Save 12%)</span></div>
        <ul class="feature-list">
          <li><span class="check">✓</span> <strong><a href="tools/elevenlabs-creator.html" style="color:inherit; text-decoration:none;">ElevenLabs Creator</a></strong>: 100K chars &amp; voice cloning</li>
          <li><span class="check">✓</span> <strong><a href="tools/suno-ai.html" style="color:inherit; text-decoration:none;">Suno AI Pro</a></strong>: 2,500 credits full commercial songs</li>
          <li><span class="check">✓</span> EasyPaisa, JazzCash, SadaPay &amp; Wise/Crypto</li>
          <li><span class="check">✓</span> 15-Minute Priority WhatsApp Delivery</li>
          <li><span class="check">✓</span> 30-Day Guaranteed Replacement Warranty</li>
        </ul>
        <div style="display:flex; flex-direction:column; gap:0.5rem; margin-top:1.25rem;">
          <button type="button" class="btn-primary w-full" onclick="openQuickOrderModal('elevenlabs-creator')">⚡ Quick Order Audio Pack</button>
          <a href="https://wa.me/923326861112?text=Hi%20AIDigiTools,%20I%20want%20to%20order%20the%20Voice%20and%20Audio%20Pack%20for%20Rs%204800%20PKR%20/%20$17%20USD" class="btn-wa-subtle w-full" target="_blank" rel="noopener noreferrer">Order on WhatsApp</a>
        </div>
      </div>
    </div>"""

content = re.sub(r'<div class="grid">\s*<!-- Bundle 1 -->.*?</div>\s*</main>', bundles_html + '\n  </main>', content, flags=re.DOTALL)
DEALS_PATH.write_text(content, encoding="utf-8")
print(f"Successfully upgraded {DEALS_PATH} with official brand icons, soft styling, and workable buttons.")
