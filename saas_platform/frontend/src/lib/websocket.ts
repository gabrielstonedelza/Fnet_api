type EventCallback = (data: WebSocketMessage) => void;

export interface WebSocketMessage {
  type: string;
  [key: string]: unknown;
}

export class DashboardWebSocket {
  private ws: WebSocket | null = null;
  private listeners: Map<string, Set<EventCallback>> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;
  private reconnectTimeout: ReturnType<typeof setTimeout> | null = null;
  private companyId: string;
  private token: string;

  constructor(companyId: string, token: string) {
    this.companyId = companyId;
    this.token = token;
  }

  connect(): void {
    const wsUrl =
      process.env.NEXT_PUBLIC_WS_URL || `ws://${window.location.hostname}:8000`;
    const url = `${wsUrl}/ws/admin/dashboard/?company_id=${this.companyId}&token=${this.token}`;

    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      console.log("[WS] Connected to admin dashboard");
      this.reconnectAttempts = 0;
      this.emit("connection", { type: "connection", status: "connected" });
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as WebSocketMessage;
        // Emit by type
        this.emit(data.type, data);
        // Also emit a catch-all
        this.emit("message", data);
      } catch {
        console.error("[WS] Failed to parse message:", event.data);
      }
    };

    this.ws.onclose = (event) => {
      console.log("[WS] Disconnected:", event.code, event.reason);
      this.emit("connection", { type: "connection", status: "disconnected" });
      this.attemptReconnect();
    };

    this.ws.onerror = (error) => {
      console.error("[WS] Error:", error);
      this.emit("connection", { type: "connection", status: "error" });
    };
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.log("[WS] Max reconnect attempts reached");
      return;
    }

    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
    this.reconnectAttempts++;
    console.log(
      `[WS] Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`
    );

    this.reconnectTimeout = setTimeout(() => {
      this.connect();
    }, delay);
  }

  on(eventType: string, callback: EventCallback): () => void {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, new Set());
    }
    this.listeners.get(eventType)!.add(callback);

    // Return unsubscribe function
    return () => {
      this.listeners.get(eventType)?.delete(callback);
    };
  }

  private emit(eventType: string, data: WebSocketMessage): void {
    this.listeners.get(eventType)?.forEach((cb) => cb(data));
  }

  send(data: unknown): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  disconnect(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
    }
    this.ws?.close();
    this.ws = null;
    this.listeners.clear();
  }
}
