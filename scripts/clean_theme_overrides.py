import re

def clean_theme():
    with open('assets/style.css', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove duplicate hero block (lines 356-432)
    # The duplicate block begins with .hero::after right after .hero .badge.emerald
    duplicate_hero_pattern = r'(\.hero \.badge\.emerald\s*\{[^}]*\}\s*)\n\s*\.hero::after\s*\{.*?(?=\.hero-pill)'
    content, count_hero = re.subn(duplicate_hero_pattern, r'\1\n', content, flags=re.DOTALL)
    print(f"Removed duplicate hero blocks: {count_hero}")

    # 2. Remove duplicate authkit block (lines 759-932)
    # This duplicate block starts with .authkit-cat-filter-pills having rgba(17, 24, 39, 0.7)
    duplicate_authkit_pattern = r'\.authkit-cat-filter-pills\s*\{[^}]*rgba\(17,\s*24,\s*39,\s*0\.7\).*?(?=\.authkit-tabs-bar)'
    content, count_auth = re.subn(duplicate_authkit_pattern, '', content, flags=re.DOTALL)
    print(f"Removed duplicate authkit blocks: {count_auth}")

    # 3. Update #features .card block at the end
    old_features_block = """/* ========================================================
   DELIBERATE SURFACE VARIATION: DARK FEATURE PANELS (#features)
   ======================================================== */
#features .card {
  background: #1F2937 !important; /* Deep Slate feature panel */
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  border-radius: 18px;
  color: #F9FAFB !important;
  box-shadow: 0 10px 25px -5px rgba(17, 24, 39, 0.15) !important;
  padding: 2rem;
}

#features .card::before {
  background: linear-gradient(90deg, #2CB6A5 0%, #8B83D7 100%) !important;
}

#features .card h2 {
  color: #FFFFFF !important;
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}

#features .card p {
  color: #98A2B3 !important;
  font-size: 0.94rem;
  line-height: 1.6;
}

/* Accessible Categories & Filter Controls */
.cat-pill-btn {
  background: #F3F4F6;
  border: 1px solid #E5E7EB;
  color: #344054;
  padding: 0.45rem 0.95rem;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 0.84rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cat-pill-btn:hover {
  background: #E5E7EB;
  color: #111827;
}

.cat-pill-btn.active {
  background: #2CB6A5 !important;
  border-color: #2CB6A5 !important;
  color: #FFFFFF !important;
  box-shadow: 0 2px 8px rgba(44, 182, 165, 0.35);
}

.search-input-field:focus {
  border-color: #2CB6A5 !important;
  box-shadow: 0 0 0 3px rgba(44, 182, 165, 0.25) !important;
}

/* FAQ Cards */
#faq .card {
  background: #FFFFFF;
  border: 1.5px solid #E2E8F0;
  border-radius: 16px;
  padding: 1.65rem 1.85rem;
}

#faq .card h2 {
  color: #111827;
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

#faq .card p {
  color: #344054;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 0;
}"""

    new_features_block = """/* ========================================================
   DELIBERATE SURFACE VARIATION: LUMINOUS LIGHT FEATURE PANELS (#features)
   ======================================================== */
#features .card {
  background: linear-gradient(145deg, #FFFFFF 0%, #F0F7FF 100%) !important;
  border: 1.5px solid #BAE6FD !important;
  border-radius: 18px;
  color: #0F172A !important;
  box-shadow: 0 4px 18px rgba(2, 132, 199, 0.06) !important;
  padding: 2rem;
}

#features .card::before {
  background: linear-gradient(90deg, #00B4D8 0%, #4361EE 100%) !important;
}

#features .card h2 {
  color: #0F172A !important;
  font-size: 1.25rem;
  font-weight: 750;
  margin-bottom: 0.75rem;
}

#features .card p {
  color: #334155 !important;
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Accessible Categories & Filter Controls */
.cat-pill-btn {
  background: #FFFFFF;
  border: 1.5px solid #CBD5E1;
  color: #334155;
  padding: 0.45rem 0.95rem;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 0.84rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cat-pill-btn:hover {
  background: #F1F5F9;
  border-color: #94A3B8;
  color: #0F172A;
}

.cat-pill-btn.active {
  background: linear-gradient(135deg, #00B4D8 0%, #0284C7 100%) !important;
  border-color: #0284C7 !important;
  color: #FFFFFF !important;
  box-shadow: 0 2px 8px rgba(2, 132, 199, 0.35);
}

.search-input-field:focus {
  border-color: #00B4D8 !important;
  box-shadow: 0 0 0 3px rgba(0, 180, 216, 0.25) !important;
}

/* FAQ Cards */
#faq .card {
  background: #FFFFFF;
  border: 1.5px solid #CBD5E1;
  border-radius: 16px;
  padding: 1.65rem 1.85rem;
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
}

#faq .card h2 {
  color: #0F172A;
  font-size: 1.15rem;
  font-weight: 750;
  margin-bottom: 0.5rem;
}

#faq .card p {
  color: #334155;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 0;
}"""

    # Normalize line endings before replacing
    content_norm = content.replace('\r\n', '\n')
    old_norm = old_features_block.replace('\r\n', '\n')
    new_norm = new_features_block.replace('\r\n', '\n')

    if old_norm in content_norm:
        content_norm = content_norm.replace(old_norm, new_norm)
        print("Successfully replaced features block!")
    else:
        print("Warning: old_features_block not found by exact string, checking regex...")

    # 4. Update compare dock
    old_compare_dock = """.compare-dock {
  position: fixed;
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 990;
  background: #0F172A;
  color: #FFFFFF;
  padding: 0.75rem 1.25rem;
  border-radius: 9999px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  animation: slideUp 0.25s ease-out;
}"""

    new_compare_dock = """.compare-dock {
  position: fixed;
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 990;
  background: #FFFFFF;
  color: #0F172A;
  padding: 0.75rem 1.25rem;
  border-radius: 9999px;
  box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15), 0 8px 10px -6px rgba(15, 23, 42, 0.1);
  border: 1.5px solid #CBD5E1;
  display: flex;
  align-items: center;
  gap: 1rem;
  animation: slideUp 0.25s ease-out;
}"""

    old_comp_norm = old_compare_dock.replace('\r\n', '\n')
    new_comp_norm = new_compare_dock.replace('\r\n', '\n')
    if old_comp_norm in content_norm:
        content_norm = content_norm.replace(old_comp_norm, new_comp_norm)
        print("Successfully replaced compare-dock styling!")

    # Write back with original or standard CRLF/LF
    with open('assets/style.css', 'w', encoding='utf-8', newline='\n') as f:
        f.write(content_norm)
    print("assets/style.css written successfully.")

if __name__ == '__main__':
    clean_theme()
