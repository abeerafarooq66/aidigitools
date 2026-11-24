// AIDigiTools Google Analytics 4 Custom Conversion & Event Delegation Engine
// Captures WhatsApp Concierge Checkout, Quick Order Inquiries, and Plan Interactions with Beacon Reliability

(function () {
  'use strict';

  function trackWaCheckout(linkEl) {
    if (!linkEl) return;
    var toolName = linkEl.getAttribute('data-tool-name') ||
                   linkEl.getAttribute('data-product') ||
                   document.title.split('|')[0].replace('AIDigiTools', '').trim();
    var toolPrice = linkEl.getAttribute('data-tool-price') || linkEl.getAttribute('data-price') || '0';
    var parsedPrice = parseFloat(toolPrice.toString().replace(/[^0-9.]/g, '')) || 0;

    if (typeof gtag === 'function') {
      gtag('event', 'wa_concierge_checkout', {
        'tool_name': toolName,
        'value': parsedPrice,
        'currency': 'PKR',
        'link_url': linkEl.href,
        'page_location': window.location.href,
        'transport_type': 'beacon'
      });
    }
  }

  function trackQuickOrderOpen(btnEl) {
    if (!btnEl) return;
    var onclickAttr = btnEl.getAttribute('onclick') || '';
    var match = onclickAttr.match(/openQuickOrderModal\('([^']+)'\)/);
    var toolSlug = match ? match[1] : (btnEl.getAttribute('data-tool') || 'general');

    if (typeof gtag === 'function') {
      gtag('event', 'initiate_quick_order', {
        'tool_slug': toolSlug,
        'page_location': window.location.href,
        'transport_type': 'beacon'
      });
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
