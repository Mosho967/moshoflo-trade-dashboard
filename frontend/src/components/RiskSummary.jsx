const RiskSummary = ({ trades = [], riskFilter, onFilterChange }) => {
  const toggle = (label) => onFilterChange(riskFilter === label ? null : label);

  const total = trades.length;
  const highCount = trades.filter((t) => t.risk_label === "HIGH RISK").length;
  const medCount = trades.filter((t) => t.risk_label === "MEDIUM RISK").length;
  const lowCount = trades.filter((t) => t.risk_label === "LOW RISK").length;

  const avgPrice = trades.length
    ? (
        trades
          .map((t) => parseFloat(t.price))
          .filter((p) => !isNaN(p))
          .reduce((a, b) => a + b, 0) / trades.length
      ).toFixed(2)
    : "0.00";

  return (
    <div className="kpi-row">
      <div
        className={`kpi-card ${!riskFilter ? "active" : ""}`}
        onClick={() => toggle(null)}
      >
        <div className="kpi-label">Total Trades</div>
        <div className="kpi-value">{total}</div>
      </div>

      <div
        className={`kpi-card ${riskFilter === "HIGH RISK" ? "active-high" : ""}`}
        onClick={() => toggle("HIGH RISK")}
      >
        <div className="kpi-label">
          <span className="kpi-dot" style={{ background: "var(--risk-high)" }} />
          High Risk
        </div>
        <div className="kpi-value" style={{ color: "var(--risk-high)" }}>
          {highCount}
        </div>
      </div>

      <div
        className={`kpi-card ${riskFilter === "MEDIUM RISK" ? "active-medium" : ""}`}
        onClick={() => toggle("MEDIUM RISK")}
      >
        <div className="kpi-label">
          <span className="kpi-dot" style={{ background: "var(--risk-medium)" }} />
          Medium Risk
        </div>
        <div className="kpi-value" style={{ color: "var(--risk-medium)" }}>
          {medCount}
        </div>
      </div>

      <div
        className={`kpi-card ${riskFilter === "LOW RISK" ? "active-low" : ""}`}
        onClick={() => toggle("LOW RISK")}
      >
        <div className="kpi-label">
          <span className="kpi-dot" style={{ background: "var(--risk-low)" }} />
          Low Risk
        </div>
        <div className="kpi-value" style={{ color: "var(--risk-low)" }}>
          {lowCount}
        </div>
      </div>

      <div className="kpi-card" style={{ cursor: "default" }}>
        <div className="kpi-label">Avg Price</div>
        <div className="kpi-value" style={{ fontSize: "22px", color: "var(--accent)" }}>
          ${avgPrice}
        </div>
      </div>
    </div>
  );
};

export default RiskSummary;
