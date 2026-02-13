import { useEffect, useMemo, useState } from "react";
import TradeTable from "./components/TradeTable";
import RiskSummary from "./components/RiskSummary";
import Header from "./components/Header";
import RiskPieChart from "./components/RiskPieChart";
import "./App.css";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

const toWsBase = (httpBase) =>
  httpBase.startsWith("https://")
    ? httpBase.replace("https://", "wss://")
    : httpBase.replace("http://", "ws://");

const WS_URL = import.meta.env.VITE_WS_URL ?? `${toWsBase(API_BASE)}/ws/trades`;

const upsertTrade = (prev, incoming) => {
  const id = incoming?.trade_id;
  if (!id) return [incoming, ...prev];
  if (prev.some((t) => t.trade_id === id)) return prev;
  return [incoming, ...prev];
};

const App = () => {
  const [trades, setTrades] = useState([]);
  const [riskFilter, setRiskFilter] = useState(null);

  useEffect(() => {
    let ws;
    let cancelled = false;

    const fetchTrades = async () => {
      try {
        const r = await fetch(`${API_BASE}/trades/`);
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const data = await r.json();
        if (!cancelled) setTrades(data);
      } catch (err) {
        console.error("Failed to load trades:", err);
      }
    };

    // initial load
    fetchTrades();

    // live updates
    ws = new WebSocket(WS_URL);

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg?.type === "heartbeat") return;
        setTrades((prev) => upsertTrade(prev, msg));
      } catch (e) {
        console.error("Bad WS message:", e);
      }
    };

    ws.onerror = (e) => console.error("WS error", e);
    ws.onclose = () => console.log("WS closed");

    return () => {
      cancelled = true;
      ws?.close();
    };
  }, []);

  const filteredTrades = useMemo(() => {
    return riskFilter ? trades.filter((t) => t.risk_label === riskFilter) : trades;
  }, [trades, riskFilter]);

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
          <RiskPieChart trades={filteredTrades} />
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
