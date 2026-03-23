function TradeTable({ trades = [] }) {
  return (
    <div className="trade-table-card">
      <div className="trade-table-header">
        <span className="trade-table-title">Recent Trades</span>
        <span className="trade-count-badge">{trades.length} trades</span>
      </div>
      <div className="table-scroll">
        <table className="trades">
          <thead>
            <tr>
              <th>ID</th>
              <th>Symbol</th>
              <th>Price</th>
              <th>Volume</th>
              <th>Side</th>
              <th>Risk</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {trades.length === 0 ? (
              <tr>
                <td colSpan={7}>
                  <div className="empty-state">No trades to display</div>
                </td>
              </tr>
            ) : (
              trades.map((trade) => (
                <tr key={trade.id ?? trade.trade_id}>
                  <td className="cell-id">{trade.id}</td>
                  <td className="cell-symbol">{trade.symbol}</td>
                  <td className="cell-price">
                    ${parseFloat(trade.price || 0).toFixed(2)}
                  </td>
                  <td className="cell-volume">{trade.volume}</td>
                  <td>
                    <span
                      className={
                        String(trade.side).toUpperCase() === "BUY"
                          ? "side-buy"
                          : "side-sell"
                      }
                    >
                      {String(trade.side).toUpperCase()}
                    </span>
                  </td>
                  <td>
                    <span
                      className={`risk-badge ${
                        trade.risk_label === "HIGH RISK"
                          ? "high"
                          : trade.risk_label === "MEDIUM RISK"
                          ? "medium"
                          : "low"
                      }`}
                    >
                      <span className="risk-dot" />
                      {trade.risk_label === "HIGH RISK"
                        ? "HIGH"
                        : trade.risk_label === "MEDIUM RISK"
                        ? "MED"
                        : "LOW"}
                    </span>
                  </td>
                  <td className="cell-time">
                    {new Date(trade.timestamp).toLocaleString()}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default TradeTable;
