import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSS_PATH = os.path.join(REPO_ROOT, "assets", "style.css")

extra_css = """

/* ========================================================
   CATEGORY SHOWCASE CARDS & TRANSPARENCY CALLOUT
   ======================================================== */
.category-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.25rem;
  margin: 1.5rem 0;
}

.category-card {
  background: linear-gradient(165deg, #FFFFFF 0%, #F8FAFD 100%);
  border: 1.5px solid #D5E2F0;
  border-radius: 18px;
  padding: 1.6rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.04);
  transition: all 0.25s ease;
  position: relative;
  overflow: hidden;
  text-decoration: none;
  color: inherit;
}

.category-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3.5px;
  background: linear-gradient(90deg, #00B4D8 0%, #4361EE 100%);
}

.category-card:hover {
  transform: translateY(-2px);
  border-color: #00B4D8;
  box-shadow: 0 8px 24px -4px rgba(0, 180, 216, 0.12);
}

.category-card-icon {
  font-size: 2rem;
  margin-bottom: 0.75rem;
  display: inline-block;
}

.category-card-title {
  font-size: 1.2rem;
  font-weight: 750;
  color: #0F172A;
  margin: 0 0 0.4rem 0;
  letter-spacing: -0.015em;
}

.category-card-desc {
  font-size: 0.9rem;
  color: #475569;
  line-height: 1.5;
  margin: 0 0 1rem 0;
  flex-grow: 1;
}

.category-card-link {
  font-size: 0.88rem;
  font-weight: 700;
  color: #0284C7;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.transparency-callout {
  background: linear-gradient(135deg, #F0F9FF 0%, #EEF2FF 100%);
  border: 1.5px solid #BAE6FD;
  border-left: 4.5px solid #00B4D8;
  border-radius: 14px;
  padding: 1.25rem 1.6rem;
  margin: 1.5rem 0 2rem;
  font-size: 0.94rem;
  line-height: 1.6;
  color: #1E293B;
  box-shadow: 0 2px 8px rgba(0, 180, 216, 0.05);
}

.transparency-callout strong {
  color: #0F172A;
}
"""

with open(CSS_PATH, "r", encoding="utf-8") as f:
    css = f.read()

if ".category-cards-grid" not in css:
    css += extra_css
    with open(CSS_PATH, "w", encoding="utf-8") as f:
        f.write(css)
    print("Added category-cards-grid & transparency-callout styles to assets/style.css.")
else:
    print("category-cards-grid styles already present in assets/style.css.")
