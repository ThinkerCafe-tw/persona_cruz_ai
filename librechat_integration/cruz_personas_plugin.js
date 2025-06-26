/**
 * CRUZ Personas Plugin for LibreChat
 * 提供人格切換和狀態顯示功能
 */

class CruzPersonasPlugin {
  constructor() {
    this.currentPersona = 'cruz-decisive';
    this.emotionState = 'determined';
    this.memoryEnabled = true;
    this.personas = {
      'cruz-decisive': {
        name: 'CRUZ',
        emoji: '🎯',
        description: 'Decisive action-oriented AI',
        color: '#ff6b6b'
      },
      'serena-supportive': {
        name: 'Serena',
        emoji: '🌸',
        description: 'Supportive empathetic AI',
        color: '#ff6bb5'
      },
      'wood-creative': {
        name: 'Wood',
        emoji: '🌳',
        description: 'Creative innovator',
        color: '#51cf66'
      },
      'fire-passionate': {
        name: 'Fire',
        emoji: '🔥',
        description: 'Passionate implementer',
        color: '#ff8787'
      },
      'earth-stable': {
        name: 'Earth',
        emoji: '🏔️',
        description: 'Stable architect',
        color: '#8b6f3e'
      },
      'metal-precise': {
        name: 'Metal',
        emoji: '⚔️',
        description: 'Precise optimizer',
        color: '#868e96'
      },
      'water-adaptive': {
        name: 'Water',
        emoji: '💧',
        description: 'Adaptive tester',
        color: '#339af0'
      }
    };
  }

  /**
   * 初始化插件
   */
  initialize() {
    // 創建人格選擇器 UI
    this.createPersonaSelector();
    
    // 創建狀態指示器
    this.createStatusIndicator();
    
    // 註冊快捷鍵
    this.registerHotkeys();
    
    // 監聽消息事件
    this.interceptMessages();
    
    console.log('🎯 CRUZ Personas Plugin initialized');
  }

  /**
   * 創建人格選擇器
   */
  createPersonaSelector() {
    const selector = document.createElement('div');
    selector.id = 'cruz-persona-selector';
    selector.className = 'cruz-persona-selector';
    selector.innerHTML = `
      <div class="persona-selector-header">
        <span class="current-persona">
          ${this.personas[this.currentPersona].emoji} ${this.personas[this.currentPersona].name}
        </span>
        <button class="persona-dropdown-toggle">▼</button>
      </div>
      <div class="persona-dropdown" style="display: none;">
        ${Object.entries(this.personas).map(([id, persona]) => `
          <div class="persona-option" data-persona="${id}">
            <span class="persona-emoji">${persona.emoji}</span>
            <div class="persona-info">
              <span class="persona-name">${persona.name}</span>
              <span class="persona-desc">${persona.description}</span>
            </div>
          </div>
        `).join('')}
      </div>
    `;

    // 添加樣式
    const style = document.createElement('style');
    style.textContent = `
      .cruz-persona-selector {
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--surface-primary);
        border: 1px solid var(--border-medium);
        border-radius: 8px;
        padding: 10px;
        z-index: 1000;
        min-width: 200px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
      }

      .persona-selector-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
        font-weight: 600;
      }

      .current-persona {
        font-size: 16px;
      }

      .persona-dropdown-toggle {
        background: none;
        border: none;
        cursor: pointer;
        padding: 5px;
        color: var(--text-primary);
      }

      .persona-dropdown {
        margin-top: 10px;
        border-top: 1px solid var(--border-light);
        padding-top: 10px;
      }

      .persona-option {
        display: flex;
        align-items: center;
        padding: 8px;
        cursor: pointer;
        border-radius: 6px;
        transition: background 0.2s;
      }

      .persona-option:hover {
        background: var(--surface-secondary);
      }

      .persona-emoji {
        font-size: 24px;
        margin-right: 10px;
      }

      .persona-info {
        display: flex;
        flex-direction: column;
      }

      .persona-name {
        font-weight: 600;
        font-size: 14px;
      }

      .persona-desc {
        font-size: 12px;
        color: var(--text-secondary);
      }

      .status-indicator {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--surface-primary);
        border: 1px solid var(--border-medium);
        border-radius: 20px;
        padding: 8px 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 14px;
      }

      .emotion-badge {
        background: var(--surface-tertiary);
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
      }

      .memory-status {
        color: var(--text-secondary);
        font-size: 12px;
      }
    `;
    document.head.appendChild(style);

    // 添加到頁面
    document.body.appendChild(selector);

    // 添加事件監聽器
    const header = selector.querySelector('.persona-selector-header');
    const dropdown = selector.querySelector('.persona-dropdown');
    
    header.addEventListener('click', () => {
      dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
    });

    // 人格選項點擊事件
    selector.querySelectorAll('.persona-option').forEach(option => {
      option.addEventListener('click', () => {
        this.switchPersona(option.dataset.persona);
        dropdown.style.display = 'none';
      });
    });
  }

  /**
   * 創建狀態指示器
   */
  createStatusIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'cruz-status-indicator';
    indicator.className = 'status-indicator';
    indicator.innerHTML = `
      <span class="emotion-badge">💪 ${this.emotionState}</span>
      <span class="memory-status">💾 Memory: ${this.memoryEnabled ? 'ON' : 'OFF'}</span>
    `;
    document.body.appendChild(indicator);
  }

  /**
   * 註冊快捷鍵
   */
  registerHotkeys() {
    document.addEventListener('keydown', (e) => {
      if (e.altKey) {
        switch(e.key) {
          case '1':
            this.switchPersona('cruz-decisive');
            break;
          case '2':
            this.switchPersona('serena-supportive');
            break;
          case '3':
            this.showFiveElementsMenu();
            break;
          case 'm':
            this.toggleMemory();
            break;
        }
      }
    });
  }

  /**
   * 切換人格
   */
  switchPersona(personaId) {
    if (this.personas[personaId]) {
      this.currentPersona = personaId;
      const persona = this.personas[personaId];
      
      // 更新 UI
      const currentPersonaSpan = document.querySelector('.current-persona');
      if (currentPersonaSpan) {
        currentPersonaSpan.textContent = `${persona.emoji} ${persona.name}`;
      }

      // 更新模型選擇
      this.updateModelSelection(personaId);

      // 顯示切換通知
      this.showNotification(`Switched to ${persona.emoji} ${persona.name}`);
      
      console.log(`🎯 Switched to persona: ${persona.name}`);
    }
  }

  /**
   * 更新模型選擇
   */
  updateModelSelection(personaId) {
    // 查找 LibreChat 的模型選擇器並更新
    const modelSelect = document.querySelector('[data-testid="model-select"]');
    if (modelSelect) {
      // 觸發模型變更事件
      const event = new CustomEvent('model-change', {
        detail: { model: personaId }
      });
      modelSelect.dispatchEvent(event);
    }

    // 同時更新存儲的端點配置
    if (window.localStorage) {
      const config = JSON.parse(localStorage.getItem('librechat-config') || '{}');
      config.lastModel = personaId;
      config.endpoint = this.getEndpointForPersona(personaId);
      localStorage.setItem('librechat-config', JSON.stringify(config));
    }
  }

  /**
   * 獲取人格對應的端點
   */
  getEndpointForPersona(personaId) {
    if (personaId.includes('cruz') || personaId.includes('serena')) {
      return 'CRUZ';
    } else if (['wood', 'fire', 'earth', 'metal', 'water'].some(e => personaId.includes(e))) {
      return 'FiveElements';
    }
    return 'CRUZ';
  }

  /**
   * 攔截並增強消息
   */
  interceptMessages() {
    // 攔截 fetch 請求
    const originalFetch = window.fetch;
    window.fetch = async (...args) => {
      const [url, options] = args;
      
      // 如果是聊天請求，添加自定義頭部
      if (url.includes('/chat/completions')) {
        options.headers = options.headers || {};
        options.headers['x-persona-type'] = this.currentPersona;
        options.headers['x-memory-enabled'] = String(this.memoryEnabled);
        
        // 修改請求體以包含人格參數
        if (options.body) {
          try {
            const body = JSON.parse(options.body);
            body.model = this.currentPersona;
            body.persona_traits = this.personas[this.currentPersona];
            body.emotion_engine = this.currentPersona === 'cruz-decisive';
            body.memory_integration = this.memoryEnabled;
            options.body = JSON.stringify(body);
          } catch (e) {
            console.error('Failed to modify request body:', e);
          }
        }
      }
      
      return originalFetch(url, options);
    };
  }

  /**
   * 切換記憶功能
   */
  toggleMemory() {
    this.memoryEnabled = !this.memoryEnabled;
    const memoryStatus = document.querySelector('.memory-status');
    if (memoryStatus) {
      memoryStatus.textContent = `💾 Memory: ${this.memoryEnabled ? 'ON' : 'OFF'}`;
    }
    this.showNotification(`Memory ${this.memoryEnabled ? 'enabled' : 'disabled'}`);
  }

  /**
   * 顯示通知
   */
  showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'cruz-notification';
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: var(--surface-primary);
      border: 2px solid var(--border-heavy);
      padding: 16px 24px;
      border-radius: 8px;
      font-weight: 600;
      z-index: 10000;
      animation: fadeInOut 2s ease-in-out;
    `;

    // 添加動畫
    const style = document.createElement('style');
    style.textContent = `
      @keyframes fadeInOut {
        0% { opacity: 0; }
        20% { opacity: 1; }
        80% { opacity: 1; }
        100% { opacity: 0; }
      }
    `;
    document.head.appendChild(style);

    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 2000);
  }

  /**
   * 顯示五行元素菜單
   */
  showFiveElementsMenu() {
    const menu = document.createElement('div');
    menu.className = 'five-elements-menu';
    menu.style.cssText = `
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: var(--surface-primary);
      border: 2px solid var(--border-heavy);
      padding: 20px;
      border-radius: 12px;
      z-index: 10000;
      min-width: 300px;
    `;
    
    menu.innerHTML = `
      <h3 style="margin: 0 0 16px 0;">🌌 Choose Five Elements Persona</h3>
      <div style="display: grid; gap: 8px;">
        ${['wood-creative', 'fire-passionate', 'earth-stable', 'metal-precise', 'water-adaptive']
          .map(id => {
            const persona = this.personas[id];
            return `
              <button class="element-option" data-persona="${id}" style="
                padding: 12px;
                border: 1px solid var(--border-light);
                border-radius: 8px;
                background: var(--surface-secondary);
                cursor: pointer;
                text-align: left;
                display: flex;
                align-items: center;
                gap: 12px;
                transition: all 0.2s;
              ">
                <span style="font-size: 24px;">${persona.emoji}</span>
                <div>
                  <div style="font-weight: 600;">${persona.name}</div>
                  <div style="font-size: 12px; color: var(--text-secondary);">${persona.description}</div>
                </div>
              </button>
            `;
          }).join('')}
      </div>
      <button onclick="this.parentElement.remove()" style="
        margin-top: 16px;
        padding: 8px 16px;
        background: var(--surface-tertiary);
        border: none;
        border-radius: 6px;
        cursor: pointer;
      ">Cancel</button>
    `;

    document.body.appendChild(menu);

    // 添加點擊事件
    menu.querySelectorAll('.element-option').forEach(option => {
      option.addEventListener('click', () => {
        this.switchPersona(option.dataset.persona);
        menu.remove();
      });
    });
  }
}

// 初始化插件
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.cruzPersonasPlugin = new CruzPersonasPlugin();
    window.cruzPersonasPlugin.initialize();
  });
} else {
  window.cruzPersonasPlugin = new CruzPersonasPlugin();
  window.cruzPersonasPlugin.initialize();
}