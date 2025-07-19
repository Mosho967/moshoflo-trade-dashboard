import { useEffect, useState } from 'react';

function App() {
  const [trades, setTrades] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/trades/')
      .then((res) => res.json())
      .then((data) => setTrades(data))
      .catch((err) => console.error('Error fetching trades:', err));
  }, []);

  return (
    <div className="container py-4">
  <h1 className="text-center mb-4">Live Trades</h1>
  <table className="table table-striped table-hover">
    <thead className="table-dark">
      <tr>
        <th>ID</th><th>Symbol</th><th>Volume</th><th>Side</th><th>Risk</th><th>Timestamp</th>
      </tr>
    </thead>
    <tbody>
      {trades.map((t) => (
        <tr key={t.id}>
          <td>{t.id}</td><td>{t.symbol}</td><td>{t.volume}</td>
          <td>{t.side}</td><td>{t.risk_label}</td>
          <td>{new Date(t.timestamp).toLocaleString()}</td>
        </tr>
      ))}
    </tbody>
  </table>
</div>

  );
}

export default App;
