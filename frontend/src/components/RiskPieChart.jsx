import React, { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import axios from 'axios';


const COLORS = ['#ff4d4f', '#faad14', '#52c41a']; // Red, Yellow, Green

const RiskPieChart = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/trades/')
      .then(response => {
        const trades = response.data;
        const counts = {
          "HIGH RISK": 0,
          "MEDIUM RISK": 0,
          "LOW RISK": 0,
        };

        trades.forEach(trade => {
          const label = trade.risk_label?.toUpperCase(); 
          if (counts[label] !== undefined) {
            counts[label]++;
          }
        });

        const formatted = Object.entries(counts).map(([key, value]) => ({
          name: key.replace(" RISK", ""), 
          value,
        }));

        setData(formatted);
      })
      .catch(err => console.error("Error fetching trades:", err));
  }, []);

  return (
    <div>
      <h3>Risk Distribution</h3>
      <PieChart width={400} height={300}>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          outerRadius={100}
          fill="#8884d8"
          label
        >
          {data.map((_, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
};

export default RiskPieChart;
