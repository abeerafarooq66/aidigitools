from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
deals_path = ROOT / "deals.html"
content = deals_path.read_text(encoding="utf-8")

bundles_to_add = """      <!-- Bundle 4 -->
      <div class="bundle-card">
        <span class="bundle-badge" style="background:#e11d48; color:#fff;">For Video Producers &amp; Animators</span>
        <h2 class="text-2xl font-black text-white">AI Filmmaker Motion Studio</h2>
        <p class="text-slate-300 text-sm mt-2">Generate cinematic clips and finish edits with 4K auto-caption workflows.</p>
        <div class="price-tag">Rs. 4,200 PKR <span class="period">(~$15 USD) / month (Save 15%)</span></div>
        <ul class="feature-list">
          <li><span class="check">&#10003;</span> <strong><a href="tools/google-veo.html" style="color:inherit; text-decoration:underline;">Google Veo Omni</a></strong>: High-fidelity cinematic 1080p video</li>
          <li><span class="check">&#10003;</span> <strong><a href="tools/runway-gen3.html" style="color:inherit; text-decoration:underline;">Runway Gen-3</a></strong>: Camera motion &amp; brush control</li>
          <li><span class="check">&#10003;</span> <strong><a href="tools/capcut-pro.html" style="color:inherit; text-decoration:underline;">CapCut Pro</a></strong>: 4K 60fps export &amp; auto-captions</li>
          <li><span class="check">&#10003;</span> EasyPaisa, JazzCash, SadaPay &amp; Wise/Crypto</li>
          <li><span class="check">&#10003;</span> 30-Day Full Replacement Guarantee</li>
        </ul>
        <a href="https://wa.me/923326861112?text=Filmmaker%20Bundle%20Order%20Rs%204200%20PKR" class="btn-primary w-full mt-4">Order Filmmaker Bundle on WhatsApp</a>
      </div>

      <!-- Bundle 5 -->
      <div class="bundle-card">
        <span class="bundle-badge" style="background:#8b5cf6; color:#fff;">For Musicians, Podcasters &amp; Voices</span>
        <h2 class="text-2xl font-black text-white">AI Voice &amp; Audio Creator Pack</h2>
        <p class="text-slate-300 text-sm mt-2">Ultra-realistic voice cloning and complete studio music generation.</p>
        <div class="price-tag">Rs. 4,800 PKR <span class="period">(~$17 USD) / month (Save 12%)</span></div>
        <ul class="feature-list">
          <li><span class="check">&#10003;</span> <strong><a href="tools/elevenlabs-creator.html" style="color:inherit; text-decoration:underline;">ElevenLabs Creator</a></strong>: 100K chars &amp; voice cloning</li>
          <li><span class="check">&#10003;</span> <strong><a href="tools/suno-ai.html" style="color:inherit; text-decoration:underline;">Suno AI Pro</a></strong>: 2,500 credits full commercial songs</li>
          <li><span class="check">&#10003;</span> EasyPaisa, JazzCash, SadaPay &amp; Wise/Crypto</li>
          <li><span class="check">&#10003;</span> 15-Minute Priority WhatsApp Delivery</li>
          <li><span class="check">&#10003;</span> 30-Day Full Replacement Guarantee</li>
        </ul>
        <a href="https://wa.me/923326861112?text=Voice%20Audio%20Pack%20Order%20Rs%204800%20PKR" class="btn-primary w-full mt-4">Order Voice &amp; Audio Pack on WhatsApp</a>
      </div>"""

target = '<a href="https://wa.me/923326861112?text=Privacy%20Pack%20Order%20Rs%202900%20PKR" class="btn-primary w-full mt-4">Order Privacy Pack on WhatsApp</a>\n      </div>'

if target in content:
    replacement = target + "\n\n" + bundles_to_add
    new_content = content.replace(target, replacement, 1)
    deals_path.write_text(new_content, encoding="utf-8")
    print("[SUCCESS] deals.html updated with 2 additional powerhouse bundles!")
else:
    # Try normalizing newlines
    content_norm = content.replace("\r\n", "\n")
    if target in content_norm:
        replacement = target + "\n\n" + bundles_to_add
        new_content = content_norm.replace(target, replacement, 1)
        deals_path.write_text(new_content, encoding="utf-8")
        print("[SUCCESS] deals.html updated with 2 additional powerhouse bundles (after newline normalization)!")
    else:
        print("[ERROR] target not found in deals.html")
