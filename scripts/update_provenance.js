const fs = require('fs');
const path = require('path');
const dataDir = 'C:\\Users\\Dell\\.gemini\\antigravity\\scratch\\aidigitools\\data';

['7d', '14d', '28d', '56d'].forEach(p => {
  const filePath = path.join(dataDir, 'analytics_report_' + p + '.json');
  if (fs.existsSync(filePath)) {
    const json = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const updated = Object.assign({
      report_period_days: json.report_period_days,
      generated_at: json.generated_at,
      data_provenance: 'SYNTHETIC_MODEL_SIMULATION_FIXTURE',
      provenance_disclaimer: 'Metrics are algorithmic baseline simulations for testing conversion engines. For verified production reporting, query authenticated GSC/GA4/CRM APIs directly.'
    }, json);
    fs.writeFileSync(filePath, JSON.stringify(updated, null, 2));
    console.log('Updated provenance in', filePath);
  }
});
