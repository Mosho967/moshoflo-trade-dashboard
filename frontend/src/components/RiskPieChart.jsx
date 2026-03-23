import { useMemo } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const COLORS = ["#f43f5e", "#f59e0b", "#10b981"];
const LABELS = ["HIGH", "MED", "LOW"];

const RiskPieChart = ({ trades = [] }) => {
  const data = useMemo(() => {
    const counts = { "HIGH RISK": 0, "MEDIUM RISK": 0, "LOW RISK": 0 };
    trades.forEach((trade) => {
      const label = trade.risk_label?.toUpperCase();
      if (counts[label] !== undefined) counts[label]++;
    });
    return Object.entries(counts).map(([key, value], i) => ({
      name: LABELS[i],
      value,
    }));
  }, [trades]);

  const total = data.reduce((s, d) => s + d.value, 0);

  return (
    <div className="chart-card">
      <div className="chart-card-title">Risk Distribution</div>
      <ResponsiveContainer width="100%" height={260}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="45%"
            innerRadius={62}
            outerRadius={92}
            paddingAngle={3}
            strokeWidth={0}
          >
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              background: "#0d1422",
              border: "1px solid rgba(255,255,255,0.07)",
              borderRadius: 8,
              color: "#e2e8f5",
              fontSize: 12,
              padding: "8px 12px",
            }}
            itemStyle={{ color: "#e2e8f5" }}
            formatter={(value) => [
              `${value} (${total ? ((value / total) * 100).toFixed(1) : 0}%)`,
            ]}
          />
          <Legend
            iconType="circle"
            iconSize={7}
            formatter={(value, entry) => (
              <span style={{ color: entry.color, fontSize: 12, fontWeight: 600 }}>
                {value}
              </span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RiskPieChart;
