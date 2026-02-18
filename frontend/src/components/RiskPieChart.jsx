import React, { useMemo } from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

const COLORS = ['#ff4d4f', '#faad14', '#52c41a']; // Red, Yellow, Green

const RiskPieChart = ({ trades = [] }) => {

  const data = useMemo(() => {
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

    return Object.entries(counts).map(([key, value]) => ({
      name: key.replace(" RISK", ""),
      value,
    }));
  }, [trades]);

  return (
    <div>
      <h3>Risk Distribution</h3>
      <PieChart width={400} height={300}>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          outerRadius={100}
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
