import { useEffect, useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import TradeTable from './components/TradeTable';
import RiskSummary from './components/RiskSummary';

function App() {
  const [trades, setTrades] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/trades')
      .then(response => setTrades(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className="d-flex flex-column align-items-center mt-5 px-3">

      {/* Logo and Heading */}
      <div className="text-center mb-4">
        <img
          src="/images/moshoflo_logo.png"
          alt="Moshoflo Logo"
          className="mx-auto d-block"
          style={{ maxHeight: '130px' }}
        />
        <h2 className="mt-3">Trade Overview</h2>
      </div>
      {/* Risk Summary Cards */}
      <RiskSummary trades={trades} /> 

      {/* Table Component */}
      <TradeTable trades={trades} />

    </div>
  );
}

export default App;
