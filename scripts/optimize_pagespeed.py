"""Script to optimize CSS color contrast, composited animations, and defer script loading for PageSpeed 100/100."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def optimize_style_css():
    css_path = ROOT / "assets" / "style.css"
    content = css_path.read_text(encoding="utf-8")

    # 1. Update .btn-whatsapp background contrast to #047857 (5.1:1 ratio)
    content = content.replace(
        "background: #10B981 !important;\n  color: #FFFFFF !important;\n  font-weight: 700;\n  font-size: 0.9rem;\n  padding: 0.65rem 1.15rem;\n  border-radius: 8px;\n  border: none !important;\n  text-decoration: none;\n  transition: all 0.2s ease;\n  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);",
        "background: #047857 !important;\n  color: #FFFFFF !important;\n  font-weight: 700;\n  font-size: 0.9rem;\n  padding: 0.65rem 1.15rem;\n  border-radius: 8px;\n  border: none !important;\n  text-decoration: none;\n  transition: all 0.2s ease;\n  box-shadow: 0 2px 8px rgba(4, 120, 87, 0.25);"
    )
    content = content.replace(
        ".btn-whatsapp:hover,\n.btn.btn-whatsapp:hover {\n  background: #059669 !important;\n  transform: translateY(-1.5px);\n  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);\n  color: #FFFFFF !important;\n}",
        ".btn-whatsapp:hover,\n.btn.btn-whatsapp:hover {\n  background: #065F46 !important;\n  transform: translateY(-1.5px);\n  box-shadow: 0 4px 12px rgba(6, 95, 70, 0.35);\n  color: #FFFFFF !important;\n}"
    )

    # 2. Update section 3 #mWaLink rules
    content = content.replace(
        "background: #10B981 !important;\n  color: #FFFFFF !important;\n  border: none !important;\n  font-weight: 700 !important;\n  text-decoration: none !important;\n  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35) !important;",
        "background: #047857 !important;\n  color: #FFFFFF !important;\n  border: none !important;\n  font-weight: 700 !important;\n  text-decoration: none !important;\n  box-shadow: 0 4px 14px rgba(4, 120, 87, 0.35) !important;"
    )
    content = content.replace(
        "background: #059669 !important;\n  color: #FFFFFF !important;\n  box-shadow: 0 6px 18px rgba(16, 185, 129, 0.45) !important;",
        "background: #065F46 !important;\n  color: #FFFFFF !important;\n  box-shadow: 0 6px 18px rgba(6, 95, 70, 0.45) !important;"
    )

    # 3. Update pulse-ring keyframes to composite via transform and opacity (no box-shadow repaints)
    pulse_target = "@keyframes pulse-ring {\n  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }\n  70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }\n  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }\n}"
    pulse_replacement = "@keyframes pulse-ring {\n  0% { transform: scale(0.95); opacity: 0.8; }\n  50% { transform: scale(1.15); opacity: 1; }\n  100% { transform: scale(0.95); opacity: 0.8; }\n}"
    content = content.replace(pulse_target, pulse_replacement)

    # 4. Update satellite-float and star-twinkle to avoid filter: drop-shadow (compositor-only properties)
    content = content.replace(
        "@keyframes satellite-float {\n  0%, 100% { transform: translate(0, 0) scale(1); filter: drop-shadow(0 0 2px rgba(67, 97, 238, 0.4)); }\n  50% { transform: translate(-2px, -3px) scale(1.15); filter: drop-shadow(0 0 5px rgba(0, 229, 163, 0.7)); }\n}",
        "@keyframes satellite-float {\n  0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.85; }\n  50% { transform: translate(-2px, -3px) scale(1.15); opacity: 1; }\n}"
    )
    content = content.replace(
        "@keyframes star-twinkle {\n  0%, 100% { transform: scale(1); opacity: 0.75; }\n  50% { transform: scale(1.28); opacity: 1; filter: drop-shadow(0 0 3px #00E5A3); }\n}",
        "@keyframes star-twinkle {\n  0%, 100% { transform: scale(1); opacity: 0.75; }\n  50% { transform: scale(1.28); opacity: 1; }\n}"
    )

    css_path.write_text(content, encoding="utf-8")
    print("style.css successfully optimized for color contrast and GPU compositing!")

def defer_cart_js_in_html():
    count = 0
    for html_file in ROOT.rglob("*.html"):
        txt = html_file.read_text(encoding="utf-8")
        orig = txt
        txt = re.sub(r'<script src="([^"]*cart\.js\?v=2\.5)"(?!\s+defer)>', r'<script src="\1" defer>', txt)
        if txt != orig:
            html_file.write_text(txt, encoding="utf-8")
            count += 1
    print(f"Added defer to cart.js in {count} HTML files!")

if __name__ == "__main__":
    optimize_style_css()
    defer_cart_js_in_html()

