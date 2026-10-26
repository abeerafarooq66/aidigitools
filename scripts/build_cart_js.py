# scripts/build_cart_js.py
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_FILE = os.path.join(BASE_DIR, "scripts", "tools_catalog.json")
CART_JS_FILE = os.path.join(BASE_DIR, "assets", "cart.js")

with open(CATALOG_FILE, "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Build compact tools object
tools_dict = {}
for slug, item in catalog.items():
    tools_dict[slug] = {
        "slug": item["slug"],
        "name": item["name"],
        "brand": item.get("brand", ""),
        "vendor": item.get("vendor", ""),
        "cat": item.get("category_label", ""),
        "icon": item.get("icon", f"assets/product-logos/{slug}.svg"),
        "desc": item.get("description", ""),
        "url": item.get("url", f"tools/{slug}.html"),
        "starting_price_pkr": item.get("starting_price_pkr", 0),
        "starting_price_usd": item.get("starting_price_usd", 0),
        "plans": item.get("plans", [])
    }

tools_json = json.dumps(tools_dict, indent=2)

cart_js_code = f"""/**
 * AIDigiTools Interactive Quick Order Drawer & Living Showcase Engine
 * Canonical Multi-Plan Support with Guaranteed Traceability and Zero Supplier Leaks.
 */

(function () {{
  'use strict';

  // Canonical Catalog Data with Verified Plans
  var TOOLS_DATA = {tools_json};

  // State variables for Quick Order Drawer
  var currentTool = TOOLS_DATA["chatgpt-plus"];
  var currentPlan = currentTool && currentTool.plans && currentTool.plans.length > 0 ? currentTool.plans[0] : null;
  var currentPaymentRail = "EasyPaisa";

  // Check prefix for assets (subfolder vs root)
  function getPathPrefix() {{
    var p = window.location.pathname;
    if (p.indexOf('/tools/') !== -1 || p.indexOf('/categories/') !== -1 || p.indexOf('/guides/') !== -1 || p.indexOf('/compare/') !== -1 || p.indexOf('/best/') !== -1) {{
      return '../';
    }}
    return '';
  }}

  // --- Living Centerpiece Showcase Engine ---
  window.setMasterTool = function (slug) {{
    var tool = TOOLS_DATA[slug];
    if (!tool) return;

    var prefix = getPathPrefix();

    var iconEl = document.getElementById('mToolIcon');
    var vendorEl = document.getElementById('mToolVendor');
    var titleEl = document.getElementById('mToolTitle');
    var descEl = document.getElementById('mToolDesc');
    var priceEl = document.getElementById('mToolPrice');
    var priceSubEl = document.getElementById('mToolPriceSub');
    var waLinkEl = document.getElementById('mWaLink');
    var specsLinkEl = document.getElementById('mSpecsLink');
    var selectEl = document.getElementById('showcaseToolSelect');

    var primaryPlan = tool.plans && tool.plans.length > 0 ? tool.plans[0] : null;
    var pricePkr = primaryPlan ? primaryPlan.price_pkr : tool.starting_price_pkr;
    var priceUsd = primaryPlan ? primaryPlan.price_usd : tool.starting_price_usd;

    if (iconEl) {{
      iconEl.src = prefix + tool.icon;
      iconEl.alt = tool.name + " Official Logo";
    }}
    if (vendorEl) vendorEl.textContent = tool.vendor;
    if (titleEl) titleEl.textContent = tool.name + " Subscription";
    if (descEl) descEl.textContent = tool.desc;
    if (priceEl) priceEl.textContent = "Rs. " + pricePkr.toLocaleString();
    if (priceSubEl) priceSubEl.textContent = "PKR (~$" + priceUsd.toFixed(2) + " USD) / month";

    if (specsLinkEl) {{
      specsLinkEl.href = prefix + tool.url;
      specsLinkEl.textContent = "View All " + (tool.plans ? tool.plans.length : 1) + " Verified Plans for " + tool.name + " →";
    }}

    var waMsg = "Hi AIDigiTools, I want to order " + tool.name + " for Rs " + pricePkr + " PKR / $" + priceUsd + " USD.";
    if (waLinkEl) {{
      waLinkEl.href = "https://wa.me/923326861112?text=" + encodeURIComponent(waMsg);
    }}

    if (selectEl && selectEl.value !== slug) {{
      selectEl.value = slug;
    }}

    // Update active tab buttons if present
    var tabBtns = document.querySelectorAll('.authkit-tab-btn');
    tabBtns.forEach(function (btn) {{
      var id = btn.id || '';
      if (id === 'mtab-' + slug) {{
        btn.classList.add('active');
      }} else {{
        btn.classList.remove('active');
      }}
    }});
  }};

  // Category filter for Living Showcase dropdown & tabs
  window.filterShowcaseCategory = function (catName, btnEl) {{
    var selectEl = document.getElementById('showcaseToolSelect');
    if (!selectEl) return;

    var pills = document.querySelectorAll('.authkit-cat-pill');
    pills.forEach(function (p) {{ p.classList.remove('active'); }});
    if (btnEl) btnEl.classList.add('active');

    var optgroups = selectEl.querySelectorAll('optgroup');
    var firstMatchingSlug = null;

    optgroups.forEach(function (grp) {{
      var grpCat = grp.getAttribute('data-cat') || '';
      if (catName === 'all' || grpCat === catName) {{
        grp.style.display = '';
        if (!firstMatchingSlug && grp.querySelector('option')) {{
          firstMatchingSlug = grp.querySelector('option').value;
        }}
      }} else {{
        grp.style.display = 'none';
      }}
    }});

    if (firstMatchingSlug) {{
      window.setMasterTool(firstMatchingSlug);
    }}
  }};

  // --- Canonical Plan Selector in Quick Order Drawer ---
  window.selectPlanInDrawer = function (planId) {{
    if (!currentTool || !currentTool.plans) return;
    var found = currentTool.plans.find(function (p) {{ return p.plan_id === planId; }});
    if (found) {{
      currentPlan = found;
      renderDrawerPlans();
      updateCartSummary();
    }}
  }};

  function renderDrawerPlans() {{
    var container = document.getElementById('drawerPlanSelectorContainer');
    if (!container) return;

    if (!currentTool.plans || currentTool.plans.length <= 1) {{
      container.style.display = 'none';
      return;
    }}

    container.style.display = 'block';
    var html = '<label style="display:block; font-size:0.82rem; font-weight:700; color:var(--text-secondary); margin-bottom:0.5rem; text-transform:uppercase; letter-spacing:0.04em;">Select Verified Plan</label>';
    html += '<div style="display:flex; flex-direction:column; gap:0.5rem;">';

    currentTool.plans.forEach(function (plan) {{
      var isSelected = currentPlan && currentPlan.plan_id === plan.plan_id;
      var activeStyle = isSelected
        ? 'border:1.5px solid #0284C7; background:#F0F9FF; box-shadow:0 2px 8px rgba(2,132,199,0.15);'
        : 'border:1px solid var(--border-color); background:var(--bg-card);';

      html += '<div onclick="selectPlanInDrawer(\\'' + plan.plan_id + '\\')" style="padding:0.65rem 0.85rem; border-radius:10px; cursor:pointer; transition:all 0.15s ease; display:flex; justify-content:space-between; align-items:center; ' + activeStyle + '">';
      html += '<div>';
      html += '<div style="font-size:0.9rem; font-weight:700; color:var(--text-primary);">' + plan.name + '</div>';
      html += '<div style="font-size:0.75rem; color:var(--text-muted);">' + plan.duration + ' • ' + plan.seats + '</div>';
      html += '</div>';
      html += '<div style="text-align:right;">';
      html += '<div style="font-size:0.92rem; font-weight:800; color:#0284C7;">Rs. ' + plan.price_pkr.toLocaleString() + '</div>';
      html += '<div style="font-size:0.72rem; color:var(--text-secondary);">(~$' + plan.price_usd.toFixed(2) + ' USD)</div>';
      html += '</div>';
      html += '</div>';
    }});

    html += '</div>';
    container.innerHTML = html;
  }}

  // --- Quick Order / Cart Drawer Engine ---
  window.openQuickOrderModal = function (slug, planId) {{
    var tool = TOOLS_DATA[slug] || currentTool;
    currentTool = tool;

    // Pick requested plan or default to first plan
    if (planId && tool.plans) {{
      var target = tool.plans.find(function (p) {{ return p.plan_id === planId; }});
      currentPlan = target || tool.plans[0];
    }} else if (tool.plans && tool.plans.length > 0) {{
      currentPlan = tool.plans[0];
    }} else {{
      currentPlan = null;
    }}

    var prefix = getPathPrefix();

    var nameEl = document.getElementById('drawerItemName');
    var vendorEl = document.getElementById('drawerItemVendor');
    var iconEl = document.getElementById('drawerItemIcon');

    if (nameEl) nameEl.textContent = tool.name;
    if (vendorEl) vendorEl.textContent = tool.vendor + " • " + tool.cat;
    if (iconEl) {{
      iconEl.src = prefix + tool.icon;
      iconEl.alt = tool.name + " Icon";
    }}

    renderDrawerPlans();
    window.selectCartRail('EasyPaisa');

    var drawer = document.getElementById('cartDrawer');
    var backdrop = document.getElementById('cartBackdrop');
    if (drawer && backdrop) {{
      drawer.classList.add('active');
      backdrop.classList.add('active');
      document.body.style.overflow = 'hidden';
    }}
  }};

  window.closeQuickOrderModal = function () {{
    var drawer = document.getElementById('cartDrawer');
    var backdrop = document.getElementById('cartBackdrop');
    if (drawer && backdrop) {{
      drawer.classList.remove('active');
      backdrop.classList.remove('active');
      document.body.style.overflow = '';
    }}
  }};

  window.selectCartRail = function (railName) {{
    currentPaymentRail = railName;
    var railOptions = document.querySelectorAll('.rail-option');
    railOptions.forEach(function (opt) {{
      if (opt.getAttribute('data-rail') === railName) {{
        opt.classList.add('active');
      }} else {{
        opt.classList.remove('active');
      }}
    }});

    updateCartSummary();
  }};

  function updateCartSummary() {{
    if (!currentTool) return;

    var pricePkr = currentPlan ? currentPlan.price_pkr : currentTool.starting_price_pkr;
    var priceUsd = currentPlan ? currentPlan.price_usd : currentTool.starting_price_usd;
    var planTitle = currentPlan ? currentPlan.name : (currentTool.name + " Standard Plan");
    var duration = currentPlan ? currentPlan.duration : "1 Month";

    var subtotalEl = document.getElementById('drawerSubtotal');
    var totalPkrEl = document.getElementById('drawerTotalPkr');
    var totalUsdEl = document.getElementById('drawerTotalUsd');
    var checkoutBtn = document.getElementById('drawerCheckoutBtn');

    if (subtotalEl) subtotalEl.textContent = "Rs. " + pricePkr.toLocaleString() + " PKR";
    if (totalPkrEl) totalPkrEl.textContent = "Rs. " + pricePkr.toLocaleString() + " PKR";
    if (totalUsdEl) totalUsdEl.textContent = "(~$" + priceUsd.toFixed(2) + " USD)";

    var waMsg = "Hi AIDigiTools! I want to order " + currentTool.name + " (" + planTitle + " - " + duration + ") for Rs. " + pricePkr.toLocaleString() + " PKR (~$" + priceUsd.toFixed(2) + " USD) via " + currentPaymentRail + ". Please share payment details and 15m delivery activation.";

    if (checkoutBtn) {{
      checkoutBtn.href = "https://wa.me/923326861112?text=" + encodeURIComponent(waMsg);
    }}
  }}

  // Close modal when pressing ESC or clicking backdrop
  document.addEventListener('keydown', function (e) {{
    if (e.key === 'Escape') {{
      window.closeQuickOrderModal();
    }}
  }});

  // Filter tool cards in search box
  window.searchTools = function (query) {{
    var q = (query || '').toLowerCase().trim();
    var cards = document.querySelectorAll('.tool-card');
    var visibleCount = 0;
    cards.forEach(function (card) {{
      var text = card.textContent.toLowerCase();
      var cat = (card.getAttribute('data-category') || '').toLowerCase();
      if (!q || text.indexOf(q) !== -1 || cat.indexOf(q) !== -1) {{
        card.style.display = '';
        visibleCount++;
      }} else {{
        card.style.display = 'none';
      }}
    }});
    var countEl = document.getElementById('searchCountBadge');
    if (countEl) {{
      countEl.textContent = 'Showing ' + visibleCount + ' of ' + cards.length + ' tools';
    }}
  }};

  window.filterTools = function (category) {{
    var input = document.getElementById('toolSearchInput');
    if (input) input.value = category;
    window.searchTools(category);
  }};

  // Initialize tool search listener if present
  document.addEventListener('DOMContentLoaded', function () {{
    var searchInput = document.getElementById('toolSearchInput');
    if (searchInput) {{
      searchInput.addEventListener('input', function (e) {{
        window.searchTools(e.target.value);
      }});
    }}
  }});

}})();
"""

with open(CART_JS_FILE, "w", encoding="utf-8") as f:
    f.write(cart_js_code)

print(f"Generated canonical assets/cart.js with {len(tools_dict)} tools and multi-plan selection!")
