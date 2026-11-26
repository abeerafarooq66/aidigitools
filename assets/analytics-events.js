// AIDigiTools Google Analytics 4 Custom Conversion & Event Delegation Engine
// Captures WhatsApp Concierge Checkout, Quick Order Inquiries, and Plan Interactions with Beacon Reliability

(function () {
  'use strict';

  function extractDetailsFromWaUrl(urlStr) {
    if (!urlStr) return { name: '', price: 0 };
    try {
      var decoded = decodeURIComponent(urlStr);
      var matchOrder = decoded.match(/(?:order|availability for|terms for)\s+([^()]+?)(?:\s*\([^\)]*\))?\s+for\s+Rs\.?\s*([0-9,]+)/i);
      if (matchOrder) {
        return {
          name: matchOrder[1].replace(/^(Hi AIDigiTools!?\s*I want to\s*)/i, '').trim(),
          price: parseFloat(matchOrder[2].replace(/,/g, '')) || 0
        };
      }
      var nameMatch = decoded.match(/(?:order|availability for|terms for)\s+([a-zA-Z0-9\s+]+?)(?:\s*\([^\)]*\)|\s+for|\.|$)/i);
      var priceMatch = decoded.match(/Rs\.?\s*([0-9,]+)/i);
      return {
        name: nameMatch ? nameMatch[1].trim() : '',
        price: priceMatch ? (parseFloat(priceMatch[1].replace(/,/g, '')) || 0) : 0
      };
    } catch (e) {
      return { name: '', price: 0 };
    }
  }

  function trackWaCheckout(linkEl) {
    if (!linkEl) return;
    var parsedFromUrl = extractDetailsFromWaUrl(linkEl.href);

    var toolName = linkEl.getAttribute('data-tool-name') ||
                   linkEl.getAttribute('data-product') ||
                   (window.currentTool ? window.currentTool.name : '') ||
                   parsedFromUrl.name ||
                   document.title.split('|')[0].replace('AIDigiTools', '').replace(/^[—\-\s]+|[—\-\s]+$/g, '').trim();

    var toolPrice = linkEl.getAttribute('data-tool-price') ||
                    linkEl.getAttribute('data-price') ||
                    (window.currentPlan ? window.currentPlan.price_pkr : '') ||
                    parsedFromUrl.price ||
                    '0';

    var parsedPrice = parseFloat(toolPrice.toString().replace(/[^0-9.]/g, '')) || 0;

    if (typeof gtag === 'function') {
      var waParams = {
        'tool_name': toolName,
        'value': parsedPrice,
        'currency': 'PKR',
        'link_url': linkEl.href,
        'page_location': window.location.href,
        'transport_type': 'beacon'
      };
      // Primary custom concierge event
      gtag('event', 'wa_concierge_checkout', waParams);
      // Normalized tracking event
      gtag('event', 'whatsapp_click', waParams);
    }
  }

  function trackQuickOrderOpen(btnEl) {
    if (!btnEl) return;
    var onclickAttr = btnEl.getAttribute('onclick') || '';
    var match = onclickAttr.match(/openQuickOrderModal\('([^']+)'\)/);
    var toolSlug = match ? match[1] : (btnEl.getAttribute('data-tool') || 'general');

    if (typeof gtag === 'function') {
      var qoParams = {
        'tool_slug': toolSlug,
        'page_location': window.location.href,
        'transport_type': 'beacon'
      };
      // Primary custom modal event
      gtag('event', 'initiate_quick_order', qoParams);
      // Normalized tracking event
      gtag('event', 'quick_order_click', qoParams);
    }
  }

  // Document-level event delegation (captures dynamically created elements from cart.js / simulator)
  document.addEventListener('click', function (e) {
    var waLink = e.target.closest('a[href*="wa.me"], a[href*="api.whatsapp.com"]');
    if (waLink) {
      trackWaCheckout(waLink);
      return;
    }

    var qoBtn = e.target.closest('button[onclick*="openQuickOrderModal"], .btn-quick-order, .nav-cta[onclick*="openQuickOrderModal"]');
    if (qoBtn) {
      trackQuickOrderOpen(qoBtn);
      return;
    }
  }, true);
})();
