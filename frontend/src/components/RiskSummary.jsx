const RiskSummary = ({ trades = [], riskFilter, onFilterChange }) => {
  const toggleFilter = (label) => {
    onFilterChange(riskFilter === label ? null : label); // toggle
  };

  const total = trades.length;
  const count = (level) => trades.filter(t => t.risk_label === level).length;

  const averagePrice = trades.length
    ? (
        trades
          .map(t => parseFloat(t.price))
          .filter(p => !isNaN(p))
          .reduce((a, b) => a + b, 0) / trades.length
      ).toFixed(2)
    : "0.00";

  return (
    <div>
      <h3>Trade Summary</h3>

      <div className="chip-group">
        <span
          className={`chip ${!riskFilter ? "active" : ""}`}
          onClick={() => toggleFilter(null)}
        >
          All
        </span>
        <span
          className={`chip ${riskFilter === "HIGH RISK" ? "active" : ""}`}
          onClick={() => toggleFilter("HIGH RISK")}
        >
          🔴 High-Risk ({count("HIGH RISK")})
        </span>
        <span
          className={`chip ${riskFilter === "MEDIUM RISK" ? "active" : ""}`}
          onClick={() => toggleFilter("MEDIUM RISK")}
        >
          🟠 Medium-Risk ({count("MEDIUM RISK")})
        </span>
        <span
          className={`chip ${riskFilter === "LOW RISK" ? "active" : ""}`}
          onClick={() => toggleFilter("LOW RISK")}
        >
          🟢 Low-Risk ({count("LOW RISK")})
        </span>
      </div>

      <p style={{ marginTop: "12px" }}>
        <strong>Total Trades:</strong> {total}<br />
        <strong>Average Price:</strong> ${averagePrice}
      </p>
    </div>
  );
};

export default RiskSummary;
