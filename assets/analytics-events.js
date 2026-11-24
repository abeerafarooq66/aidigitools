// AIDigiTools Google Analytics 4 Custom Conversion Instrumentation
// Captures WhatsApp Concierge Checkout & Inquiries for True ROI Attribution

document.addEventListener('DOMContentLoaded', function () {
  // 1. WhatsApp Concierge Direct Click Attribution
  document.querySelectorAll('a[href*="wa.me"]').forEach(function (link) {
    link.addEventListener('click', function () {
      var toolName = this.getAttribute('data-tool-name') || document.title.split('|')[0].trim();
      var toolPrice = this.getAttribute('data-tool-price') || '0';
      if (typeof gtag === 'function') {
        gtag('event', 'wa_concierge_checkout', {
          'tool_name': toolName,
          'value': parseFloat(toolPrice) || 0,
          'currency': 'PKR',
          'link_url': this.href,
          'page_location': window.location.href
        });
      }
    });
  });

  // 2. Quick Order Modal Open Tracking
  document.querySelectorAll('button[onclick*="openQuickOrderModal"]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var onclickAttr = this.getAttribute('onclick') || '';
      var match = onclickAttr.match(/openQuickOrderModal\('([^']+)'\)/);
      var toolSlug = match ? match[1] : 'general';
      if (typeof gtag === 'function') {
        gtag('event', 'initiate_quick_order', {
          'tool_slug': toolSlug,
          'page_location': window.location.href
        });
      }
    });
  });
});
