import { useEffect, useState } from "react";
import TradeTable from "./components/TradeTable";
import RiskSummary from "./components/RiskSummary";
import Header from "./components/Header";
import RiskPieChart from "./components/RiskPieChart";
import "./App.css";

const App = () => {
  const [trades, setTrades] = useState([]);
  const [riskFilter, setRiskFilter] = useState(null);

  useEffect(() => {
    const fetchTrades = async () => {
      try {
        const response = await fetch("http://localhost:8000/trades/");
        const data = await response.json();
        setTrades(data);
      } catch (err) {
        console.error("Failed to load trades:", err);
      }
    };

    fetchTrades();
    const interval = setInterval(fetchTrades, 5000);
    return () => clearInterval(interval);
  }, []);

  const filteredTrades = riskFilter
    ? trades.filter((t) => t.risk_label === riskFilter)
    : trades;

  return (
    <div className="app">
      <Header />
      <main className="main-container">
        <div className="filter-topbar">
      <RiskSummary
    trades={trades}
    riskFilter={riskFilter}
    onFilterChange={setRiskFilter}
  />
           <RiskPieChart />
          </div>

        <div className="content-section">
          <div className="table-section">
            <TradeTable trades={filteredTrades} />
          </div>



         
        </div>
      </main>
    </div>
  );
};

export default App;
