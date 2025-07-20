import { useEffect, useState } from 'react';
import axios from 'axios';
import useWebSocket from './hooks/useWebSocket'; 
import 'bootstrap/dist/css/bootstrap.min.css';
import TradeTable from './components/TradeTable';
import RiskSummary from './components/RiskSummary';

function App() {
  const [trades, setTrades] = useState([]);

  // Initial fetch
  useEffect(() => {
    axios.get(`${import.meta.env.VITE_API_URL}/trades`)
      .then(response => setTrades(response.data))
      .catch(error => console.error(error));
  }, []);

  // WebSocket hook
  useWebSocket((newTrade) => {
    console.log("📡 New trade received via WebSocket:", newTrade);
    setTrades(prev => [newTrade, ...prev]);
  });

  return (
    <div className="d-flex flex-column align-items-center mt-5 px-3">
      <div className="text-center mb-4">
        <img
          src="/images/moshoflo_logo.png"
          alt="Moshoflo Logo"
          className="mx-auto d-block"
          style={{ maxHeight: '130px' }}
        />
        <h2 className="mt-3">Trade Overview</h2>
      </div>

      <RiskSummary trades={trades} />
      <TradeTable trades={trades} />
    </div>
  );
}

export default App;

