import React from 'react';

function TradeTable({ trades }) {
  return (
    <div className="w-100" style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <div className="card shadow-sm">
        <div className="card-body">
          <div className="table-responsive" style={{ overflowX: 'auto' }}>
            <table className="table table-striped table-bordered text-center mx-auto" style={{ minWidth: '700px' }}>
              <thead className="thead-dark">
                <tr>
                  <th>ID</th>
                  <th>Symbol</th>
                  <th>Volume</th>
                  <th>Side</th>
                  <th>Risk</th>
                  <th>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {trades.map((trade) => (
                  <tr key={trade.id}>
                    <td>{trade.id}</td>
                    <td>{trade.symbol}</td>
                    <td>{trade.volume}</td>
                    <td>{trade.side}</td>
                    <td>
                      <span className={
                        trade.risk_label === 'HIGH RISK' ? 'badge bg-danger' :
                        trade.risk_label === 'MEDIUM RISK' ? 'badge bg-warning text-dark' :
                        'badge bg-success'
                      }>
                        {trade.risk_label}
                      </span>
                    </td>
                    <td>{new Date(trade.timestamp).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default TradeTable;
