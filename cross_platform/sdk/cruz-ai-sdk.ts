/**
 * CRUZ AI SDK for TypeScript/JavaScript
 * 跨平台同步客戶端
 */

export interface Message {
  platform: string;
  userId: string;
  message: string;
  persona?: string;
  context?: Record<string, any>;
  metadata?: Record<string, any>;
}

export interface Response {
  messageId: string;
  platform: string;
  userId: string;
  persona: string;
  response: string;
  emotion?: string;
  memoryUsed: boolean;
  timestamp: string;
}

export interface SyncEvent {
  eventType: string;
  platform: string;
  userId: string;
  data: Record<string, any>;
  timestamp: string;
}

export interface Session {
  currentPersona: string;
  memoryEnabled: boolean;
  platforms: string[];
  lastSync: string | null;
}

export type PersonaType = 
  | 'cruz-decisive' 
  | 'serena-supportive' 
  | 'wood-creative' 
  | 'fire-passionate' 
  | 'earth-stable' 
  | 'metal-precise' 
  | 'water-adaptive';

export interface CruzAIConfig {
  apiUrl?: string;
  wsUrl?: string;
  apiKey: string;
  platform: string;
  autoReconnect?: boolean;
  reconnectInterval?: number;
}

export class CruzAISDK {
  private config: Required<CruzAIConfig>;
  private ws: WebSocket | null = null;
  private eventHandlers: Map<string, Set<Function>> = new Map();
  private reconnectTimer: NodeJS.Timeout | null = null;
  private userId: string | null = null;

  constructor(config: CruzAIConfig) {
    this.config = {
      apiUrl: 'http://localhost:8002',
      wsUrl: 'ws://localhost:8002',
      autoReconnect: true,
      reconnectInterval: 5000,
      ...config
    };
  }

  /**
   * 初始化 SDK
   */
  async initialize(userId: string): Promise<void> {
    this.userId = userId;
    await this.connectWebSocket();
  }

  /**
   * 連接 WebSocket
   */
  private async connectWebSocket(): Promise<void> {
    if (!this.userId) {
      throw new Error('User ID is required');
    }

    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(`${this.config.wsUrl}/ws/${this.userId}`);

        this.ws.onopen = () => {
          console.log('🔌 WebSocket connected');
          this.emit('connected', { userId: this.userId });
          
          // 註冊平台
          this.send({
            type: 'platform_register',
            platform: this.config.platform
          });
          
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this.handleSyncEvent(data);
          } catch (error) {
            console.error('Failed to parse message:', error);
          }
        };

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          this.emit('error', error);
        };

        this.ws.onclose = () => {
          console.log('🔌 WebSocket disconnected');
          this.emit('disconnected', { userId: this.userId });
          
          if (this.config.autoReconnect) {
            this.scheduleReconnect();
          }
        };
      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * 處理同步事件
   */
  private handleSyncEvent(event: any): void {
    switch (event.event_type) {
      case 'connection_established':
        this.emit('session_ready', event.session);
        break;
      case 'persona_changed':
        this.emit('persona_changed', event);
        break;
      case 'memory_toggled':
        this.emit('memory_toggled', event);
        break;
      case 'message_sync':
        this.emit('message_sync', event);
        break;
      default:
        this.emit(event.event_type, event);
    }
  }

  /**
   * 安排重連
   */
  private scheduleReconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }

    this.reconnectTimer = setTimeout(() => {
      console.log('🔄 Attempting to reconnect...');
      this.connectWebSocket().catch(console.error);
    }, this.config.reconnectInterval);
  }

  /**
   * 發送消息
   */
  async sendMessage(message: Omit<Message, 'platform' | 'userId'>): Promise<Response> {
    if (!this.userId) {
      throw new Error('SDK not initialized');
    }

    const response = await fetch(`${this.config.apiUrl}/message/unified`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`
      },
      body: JSON.stringify({
        ...message,
        platform: this.config.platform,
        userId: this.userId
      })
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return response.json();
  }

  /**
   * 切換人格
   */
  async switchPersona(persona: PersonaType): Promise<void> {
    this.send({
      type: 'persona_change',
      persona
    });
  }

  /**
   * 切換記憶功能
   */
  async toggleMemory(enabled: boolean): Promise<void> {
    this.send({
      type: 'memory_toggle',
      enabled
    });
  }

  /**
   * 獲取會話狀態
   */
  async getSession(): Promise<Session> {
    if (!this.userId) {
      throw new Error('SDK not initialized');
    }

    const response = await fetch(`${this.config.apiUrl}/user/${this.userId}/session`, {
      headers: {
        'Authorization': `Bearer ${this.config.apiKey}`
      }
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    return data.session;
  }

  /**
   * 發送 WebSocket 消息
   */
  private send(data: any): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.warn('WebSocket not connected');
    }
  }

  /**
   * 事件監聽
   */
  on(event: string, handler: Function): void {
    if (!this.eventHandlers.has(event)) {
      this.eventHandlers.set(event, new Set());
    }
    this.eventHandlers.get(event)!.add(handler);
  }

  /**
   * 移除事件監聽
   */
  off(event: string, handler: Function): void {
    const handlers = this.eventHandlers.get(event);
    if (handlers) {
      handlers.delete(handler);
    }
  }

  /**
   * 觸發事件
   */
  private emit(event: string, data: any): void {
    const handlers = this.eventHandlers.get(event);
    if (handlers) {
      handlers.forEach(handler => {
        try {
          handler(data);
        } catch (error) {
          console.error(`Error in event handler for ${event}:`, error);
        }
      });
    }
  }

  /**
   * 斷開連接
   */
  disconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

// 便利函數
export function createCruzAI(config: CruzAIConfig): CruzAISDK {
  return new CruzAISDK(config);
}

// React Hook (如果使用 React)
export function useCruzAI(config: CruzAIConfig, userId: string) {
  const [sdk, setSdk] = useState<CruzAISDK | null>(null);
  const [connected, setConnected] = useState(false);
  const [session, setSession] = useState<Session | null>(null);

  useEffect(() => {
    const client = createCruzAI(config);
    
    client.on('connected', () => setConnected(true));
    client.on('disconnected', () => setConnected(false));
    client.on('session_ready', (s: Session) => setSession(s));
    
    client.initialize(userId).then(() => {
      setSdk(client);
    });

    return () => {
      client.disconnect();
    };
  }, [config, userId]);

  return { sdk, connected, session };
}

// 匯出類型
export type { CruzAISDK };

// 使用範例
/*
const sdk = createCruzAI({
  apiKey: 'your-api-key',
  platform: 'web'
});

await sdk.initialize('user123');

// 發送消息
const response = await sdk.sendMessage({
  message: "Hello CRUZ!",
  persona: "cruz-decisive"
});

// 監聽事件
sdk.on('persona_changed', (event) => {
  console.log('Persona changed:', event.persona);
});

// 切換人格
await sdk.switchPersona('serena-supportive');
*/

// TypeScript 宣告 (為了 useState, useEffect)
declare function useState<T>(initialState: T | (() => T)): [T, (value: T) => void];
declare function useEffect(effect: () => void | (() => void), deps?: any[]): void;