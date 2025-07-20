import { useEffect } from "react";

export default function useWebSocket(onMessage) {
  useEffect(() => {
    const socket = new WebSocket(`${import.meta.env.VITE_WS_URL}/ws/trades`);

    socket.onopen = () => {
      console.log("WebSocket connected!");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data); // Callback to update your trade state
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
      console.warn("WebSocket disconnected");
    };

    return () => {
      socket.close();
    };
  }, [onMessage]);
}
