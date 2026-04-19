import { useEffect, useMemo, useState, useCallback } from "react";
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
  const [wsStatus, setWsStatus] = useState("connecting");
  const [backendRestored, setBackendRestored] = useState(false);

  const fetchTrades = useCallback(async () => {
    try {
      const r = await fetch(`${API_BASE}/trades/`);
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json();
      setTrades(data);
    } catch (err) {
      console.error("Failed to load trades:", err);
    }
  }, []);

  useEffect(() => {
    let ws;
    let cancelled = false;
    let retryTimer;

    const connect = () => {
      if (cancelled) return;
      setWsStatus("connecting");
      ws = new WebSocket(WS_URL);

      ws.onopen = () => {
        if (cancelled) return;
        setWsStatus("live");
        setBackendRestored(false);
      };

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          if (msg?.type === "heartbeat") return;
          setTrades((prev) => upsertTrade(prev, msg));
        } catch (e) {
          console.error("Bad WS message:", e);
        }
      };

      ws.onerror = (e) => { console.error("WS error", e); };

      ws.onclose = () => {
        if (cancelled) return;
        setWsStatus("offline");
        const probe = () => {
          if (cancelled) return;
          const p = new WebSocket(WS_URL);
          p.onopen = () => { p.close(); setBackendRestored(true); };
          p.onerror = () => { retryTimer = setTimeout(probe, 3000); };
        };
        retryTimer = setTimeout(probe, 3000);
      };
    };

    fetchTrades();
    connect();

    return () => {
      cancelled = true;
      clearTimeout(retryTimer);
      ws?.close();
    };
  }, [fetchTrades]);

  const handleReconnect = async () => {
    setBackendRestored(false);
    setWsStatus("connecting");
    await fetchTrades();
    window.location.reload();
  };

  const filteredTrades = useMemo(() => {
    return riskFilter ? trades.filter((t) => t.risk_label === riskFilter) : trades;
  }, [trades, riskFilter]);

  return (
    <div className="app">
      <Header wsStatus={wsStatus} />

      {(wsStatus === "offline" || backendRestored) && (
        <div className={`connection-overlay ${backendRestored ? "connection-overlay--restored" : ""}`}>
          <div className="connection-overlay__box">
            {backendRestored ? (
              <>
                <div className="connection-overlay__icon connection-overlay__icon--green" />
                <p className="connection-overlay__title">Connection Regained</p>
                <p className="connection-overlay__sub">The service is back online.</p>
                <button className="connection-overlay__btn" onClick={handleReconnect}>
                  Reconnect
                </button>
              </>
            ) : (
              <>
                <div className="connection-overlay__icon connection-overlay__icon--red" />
                <p className="connection-overlay__title">Service Unavailable</p>
                <p className="connection-overlay__sub">Waiting for connection...</p>
                <div className="connection-overlay__spinner" />
              </>
            )}
          </div>
        </div>
      )}

      <main className={`main-container ${wsStatus === "offline" ? "main-container--blurred" : ""}`}>
        <RiskSummary
          trades={trades}
          riskFilter={riskFilter}
          onFilterChange={setRiskFilter}
        />
        <div className="content-row">
          <div className="table-section">
            <TradeTable trades={filteredTrades} />
          </div>
          <div className="chart-section">
            <RiskPieChart trades={filteredTrades} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;
