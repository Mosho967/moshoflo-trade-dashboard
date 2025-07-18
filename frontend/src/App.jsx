import { useEffect, useState } from 'react';

function App() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws/trades");

    socket.onopen = () => {
      console.log("WebSocket has successfully connected");
    };

    socket.onmessage = (event) => {
      const newTrade = JSON.parse(event.data);
      setMessages((prev) => [...prev, newTrade]);
    };

    socket.onclose = () => {
      console.log("WebSocket disconnected");
    };

    return () => socket.close();
  }, []);

  return (
    <div>
      <h1> Live Trades</h1>
      <ul>
        {messages.map((trade, index) => (
          <li key={index}>
            {trade.symbol} | {trade.price} | {trade.volume} | {trade.risk_label}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;


