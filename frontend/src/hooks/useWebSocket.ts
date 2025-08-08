import { useEffect, useRef } from "react";

export function useWebSocket(assemblyId: string, onMessage: (data: any) => void) {
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const socket = new WebSocket(`ws://${window.location.host}/ws/${assemblyId}`);
    socketRef.current = socket;
    socket.onmessage = event => {
      onMessage(JSON.parse(event.data));
    };
    return () => {
      socket.close();
    };
  }, [assemblyId, onMessage]);

  return socketRef.current;
}
