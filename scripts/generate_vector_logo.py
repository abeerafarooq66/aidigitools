"""
Generate the vector SVG logo for AIDigiTools matching the Orbit Emblem reference:
- Fluid intertwined AD monogram with 3D ribbon folds
- Elliptical planetary orbit ring tilted dynamically
- Glowing celestial satellite node on the orbit
- 4-point accent star sparkles
- 'AI' in vibrant mint-to-cyan gradient
- 'DigiTools' in bold geometric midnight navy
- Tagline: SMART TOOLS • BIGGER POSSIBILITIES
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "assets" / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

# 1. Full Horizontal Logo (Emblem + Wordmark + Tagline) for Header & Branding
svg_full_logo = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 120" width="100%" height="100%" fill="none" class="aidigitools-orbit-logo" aria-label="AIDigiTools Logo">
  <defs>
    <!-- Vibrant Emerald / Mint to Cyan Gradient for A-Leg -->
    <linearGradient id="adGradTeal" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00E5A3"/>
      <stop offset="50%" stop-color="#05D5A6"/>
      <stop offset="100%" stop-color="#00B4D8"/>
    </linearGradient>

    <!-- Cyan to Royal Blue to Twilight Purple for D-Loop -->
    <linearGradient id="adGradPurple" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0077B6"/>
      <stop offset="35%" stop-color="#4361EE"/>
      <stop offset="70%" stop-color="#7209B7"/>
      <stop offset="100%" stop-color="#8B5CF6"/>
    </linearGradient>

    <!-- Ribbon Fold Shadow -->
    <linearGradient id="adGradFold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0077B6" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#1E1B4B" stop-opacity="0.3"/>
    </linearGradient>

    <!-- Orbit Ring Gradient -->
    <linearGradient id="adOrbitGrad" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#00E5A3"/>
      <stop offset="50%" stop-color="#00B4D8"/>
      <stop offset="85%" stop-color="#6366F1"/>
      <stop offset="100%" stop-color="#8B5CF6"/>
    </linearGradient>

    <!-- Satellite Node Glow -->
    <radialGradient id="adNodeGrad" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#A5B4FC"/>
      <stop offset="40%" stop-color="#6366F1"/>
      <stop offset="100%" stop-color="#4338CA"/>
    </radialGradient>

    <!-- Wordmark AI Gradient -->
    <linearGradient id="wordmarkAIGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00E5A3"/>
      <stop offset="100%" stop-color="#00B4D8"/>
    </linearGradient>
  </defs>

  <style>
    .orbit-ring {
      stroke-dasharray: 450;
      stroke-dashoffset: 0;
      transition: stroke-dashoffset 0.8s ease;
    }
    .orbit-node {
      transform-origin: 104px 34px;
      transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .sparkle-star {
      transform-origin: center;
      animation: sparkle-pulse 3s infinite ease-in-out;
    }
    .sparkle-star-1 { animation-delay: 0s; }
    .sparkle-star-2 { animation-delay: 1s; }
    .sparkle-star-3 { animation-delay: 2s; }

    @keyframes sparkle-pulse {
      0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.85; }
      50% { transform: scale(1.25) rotate(15deg); opacity: 1; }
    }

    .aidigitools-orbit-logo:hover .orbit-ring {
      animation: orbit-spin-trace 4s linear infinite;
    }
    .aidigitools-orbit-logo:hover .orbit-node {
      transform: scale(1.25);
    }

    @media (prefers-reduced-motion: reduce) {
      .sparkle-star { animation: none !important; }
      .orbit-ring { animation: none !important; }
      .orbit-node { transform: none !important; }
    }
  </style>

  <!-- ================= EMBLEM GROUP (120x120 viewBox centered at x=10, y=5) ================= -->
  <g class="emblem-group" transform="translate(10, 5)">
    <!-- Back Orbit Segment (Behind D-Loop) -->
    <path class="orbit-ring orbit-back" d="M 12 62 C 12 36, 126 18, 134 38" 
          stroke="url(#adOrbitGrad)" stroke-width="3" stroke-linecap="round" fill="none" opacity="0.6"/>

    <!-- Left Sparkle Star (Teal) -->
    <path class="sparkle-star sparkle-star-1" d="M 8 36 Q 8 41 3 41 Q 8 41 8 46 Q 8 41 13 41 Q 8 41 8 36 Z" fill="#00E5A3"/>

    <!-- Right Sparkle Star (Violet) -->
    <path class="sparkle-star sparkle-star-3" d="M 128 78 Q 128 82 124 82 Q 128 82 128 86 Q 128 82 132 82 Q 128 82 128 78 Z" fill="#8B5CF6"/>

    <!-- Left Leg of 'A' (Emerald to Cyan Ribbon) -->
    <path d="M 22 94 L 46 32 C 48 27, 54 22, 62 25 L 75 30 C 80 32, 81 37, 78 42 L 56 94 C 54 99, 46 102, 38 100 L 26 97 C 22 96, 21 95, 22 94 Z" 
          fill="url(#adGradTeal)"/>

    <!-- Top Fold Shading (creates the Möbius depth) -->
    <path d="M 62 25 C 70 20, 84 25, 94 34 L 82 46 C 75 40, 68 36, 62 34 Z" 
          fill="url(#adGradFold)"/>

    <!-- Outer 'D' Loop (Cyan to Indigo to Purple) -->
    <path d="M 68 34 C 88 22, 118 30, 118 56 C 118 82, 88 98, 62 98 L 74 82 C 90 82, 102 72, 102 56 C 102 42, 86 36, 72 44 Z" 
          fill="url(#adGradPurple)"/>

    <!-- Center Crossbar & Connection forming 'AD' Ligature -->
    <path d="M 46 64 C 52 58, 66 56, 80 62 L 72 74 C 62 70, 52 72, 46 76 Z" 
          fill="url(#adGradTeal)" opacity="0.95"/>

    <!-- Inner Sparkle Star (Teal inside D-Counter) -->
    <path class="sparkle-star sparkle-star-2" d="M 85 46 Q 85 50 81 50 Q 85 50 85 54 Q 85 50 89 50 Q 85 50 85 46 Z" fill="#00E5A3"/>

    <!-- Front Orbit Segment (Over A-Leg) -->
    <path class="orbit-ring orbit-front" d="M 134 38 C 142 58, 38 88, 16 66" 
          stroke="url(#adOrbitGrad)" stroke-width="3.5" stroke-linecap="round" fill="none"/>

    <!-- Celestial Satellite Node (Orbiter) -->
    <circle class="orbit-node" cx="124" cy="34" r="5.5" fill="url(#adNodeGrad)"/>
    <circle cx="122.5" cy="32.5" r="1.8" fill="#FFFFFF" opacity="0.8"/>
  </g>

  <!-- ================= BRAND TYPOGRAPHY ================= -->
  <!-- 'AI' in Vibrant Cyan-Mint Gradient -->
  <text x="160" y="74" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif" font-weight="900" font-size="46" letter-spacing="-1.5" fill="url(#wordmarkAIGrad)">AI</text>

  <!-- 'DigiTools' in Sleek Geometric Midnight Navy -->
  <text x="212" y="74" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif" font-weight="800" font-size="46" letter-spacing="-0.8" fill="#0F172A">DigiTools</text>

  <!-- Tagline: SMART TOOLS • BIGGER POSSIBILITIES -->
  <g transform="translate(162, 96)">
    <text x="0" y="0" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif" font-weight="700" font-size="10.5" letter-spacing="3.2" fill="#64748B" text-transform="uppercase">SMART TOOLS</text>
    <circle cx="108" cy="-3.5" r="3" fill="#00B4D8"/>
    <text x="122" y="0" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif" font-weight="700" font-size="10.5" letter-spacing="3.2" fill="#64748B" text-transform="uppercase">BIGGER POSSIBILITIES</text>
  </g>
</svg>
"""

# 2. Square Emblem Icon (for Favicons, App Icon, Social Avatars)
svg_emblem_icon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 160" width="100%" height="100%" fill="none" aria-label="AIDigiTools Emblem">
  <defs>
    <linearGradient id="embTeal" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00E5A3"/>
      <stop offset="50%" stop-color="#05D5A6"/>
      <stop offset="100%" stop-color="#00B4D8"/>
    </linearGradient>
    <linearGradient id="embPurple" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0077B6"/>
      <stop offset="35%" stop-color="#4361EE"/>
      <stop offset="70%" stop-color="#7209B7"/>
      <stop offset="100%" stop-color="#8B5CF6"/>
    </linearGradient>
    <linearGradient id="embFold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0077B6" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#1E1B4B" stop-opacity="0.3"/>
    </linearGradient>
    <linearGradient id="embOrbit" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#00E5A3"/>
      <stop offset="50%" stop-color="#00B4D8"/>
      <stop offset="85%" stop-color="#6366F1"/>
      <stop offset="100%" stop-color="#8B5CF6"/>
    </linearGradient>
    <radialGradient id="embNode" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#A5B4FC"/>
      <stop offset="40%" stop-color="#6366F1"/>
      <stop offset="100%" stop-color="#4338CA"/>
    </radialGradient>
  </defs>

  <g transform="translate(10, 20)">
    <!-- Back Orbit Segment -->
    <path d="M 12 62 C 12 36, 126 18, 134 38" 
          stroke="url(#embOrbit)" stroke-width="3.5" stroke-linecap="round" fill="none" opacity="0.6"/>

    <!-- Left Sparkle -->
    <path d="M 8 36 Q 8 41 3 41 Q 8 41 8 46 Q 8 41 13 41 Q 8 41 8 36 Z" fill="#00E5A3"/>

    <!-- Right Sparkle -->
    <path d="M 128 78 Q 128 82 124 82 Q 128 82 128 86 Q 128 82 132 82 Q 128 82 128 78 Z" fill="#8B5CF6"/>

    <!-- Left Leg of 'A' -->
    <path d="M 22 94 L 46 32 C 48 27, 54 22, 62 25 L 75 30 C 80 32, 81 37, 78 42 L 56 94 C 54 99, 46 102, 38 100 L 26 97 C 22 96, 21 95, 22 94 Z" 
          fill="url(#embTeal)"/>

    <!-- Top Fold Shading -->
    <path d="M 62 25 C 70 20, 84 25, 94 34 L 82 46 C 75 40, 68 36, 62 34 Z" 
          fill="url(#embFold)"/>

    <!-- Outer 'D' Loop -->
    <path d="M 68 34 C 88 22, 118 30, 118 56 C 118 82, 88 98, 62 98 L 74 82 C 90 82, 102 72, 102 56 C 102 42, 86 36, 72 44 Z" 
          fill="url(#embPurple)"/>

    <!-- Center Crossbar -->
    <path d="M 46 64 C 52 58, 66 56, 80 62 L 72 74 C 62 70, 52 72, 46 76 Z" 
          fill="url(#embTeal)" opacity="0.95"/>

    <!-- Center Sparkle -->
    <path d="M 85 46 Q 85 50 81 50 Q 85 50 85 54 Q 85 50 89 50 Q 85 50 85 46 Z" fill="#00E5A3"/>

    <!-- Front Orbit Segment -->
    <path d="M 134 38 C 142 58, 38 88, 16 66" 
          stroke="url(#embOrbit)" stroke-width="4" stroke-linecap="round" fill="none"/>

    <!-- Celestial Satellite Node -->
    <circle cx="124" cy="34" r="6" fill="url(#embNode)"/>
    <circle cx="122.5" cy="32.5" r="2" fill="#FFFFFF" opacity="0.8"/>
  </g>
</svg>
"""

(IMG_DIR / "aidigitools-logo.svg").write_text(svg_full_logo, encoding="utf-8")
(IMG_DIR / "aidigitools-emblem.svg").write_text(svg_emblem_icon, encoding="utf-8")
(ROOT / "favicon.svg").write_text(svg_emblem_icon, encoding="utf-8")

print(f"Generated logo SVG assets in {IMG_DIR} and root favicon.svg")
