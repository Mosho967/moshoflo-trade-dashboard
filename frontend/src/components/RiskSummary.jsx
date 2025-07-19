import React from 'react';

function RiskSummary({ trades }) {
  const high = trades.filter(t => t.risk_label === 'HIGH RISK').length;
  const medium = trades.filter(t => t.risk_label === 'MEDIUM RISK').length;
  const low = trades.filter(t => t.risk_label === 'LOW RISK').length;

  return (
    <div className="d-flex justify-content-center mb-4 gap-4 flex-wrap">
      <div className="card text-white bg-danger p-3 shadow" style={{ minWidth: '150px' }}>
        <h5 className="text-center">High Risk</h5>
        <h3 className="text-center">{high}</h3>
      </div>
      <div className="card text-dark bg-warning p-3 shadow" style={{ minWidth: '150px' }}>
        <h5 className="text-center">Medium Risk</h5>
        <h3 className="text-center">{medium}</h3>
      </div>
      <div className="card text-white bg-success p-3 shadow" style={{ minWidth: '150px' }}>
        <h5 className="text-center">Low Risk</h5>
        <h3 className="text-center">{low}</h3>
      </div>
    </div>
  );
}

export default RiskSummary;
