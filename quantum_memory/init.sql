-- 量子記憶系統初始化 SQL
-- 用於 Docker PostgreSQL 容器初始化

-- 啟用 pgvector 擴展
CREATE EXTENSION IF NOT EXISTS vector;

-- 建立預設代理人（五行 + 無極 + CRUZ + Serena）
INSERT INTO agents (id, name, emoji, element, description) VALUES
('wuji', '無極', '🌌', 'wuji', '系統觀察者，統籌五行元素協作'),
('cruz', 'CRUZ', '🎯', 'yang', '決斷果敢的數位分身'),
('serena', 'Serena', '🌸', 'yin', '溫柔貼心的 AI 助理'),
('wood', '木', '🌱', 'wood', '產品經理，創意成長'),
('fire', '火', '🔥', 'fire', '開發專員，熱情實踐'),
('earth', '土', '🏔️', 'earth', '架構師，穩固基礎'),
('metal', '金', '⚔️', 'metal', '優化專員，精益求精'),
('water', '水', '💧', 'water', '測試專員，品質守護')
ON CONFLICT (id) DO NOTHING;

-- 建立初始量子態
INSERT INTO quantum_states (agent_id, phase, frequency, amplitude, coherence, metadata) VALUES
('wuji', 0.0, 1.0, 1.0, 1.0, '{"state": "observing", "balance": 1.0}'),
('cruz', 0.785, 2.0, 1.2, 0.95, '{"state": "active", "energy": "high"}'),
('serena', 3.14, 0.8, 0.9, 0.98, '{"state": "harmonious", "empathy": 0.9}'),
('wood', 0.524, 1.2, 1.0, 0.9, '{"state": "growing", "creativity": 0.85}'),
('fire', 1.571, 3.0, 1.5, 0.85, '{"state": "burning", "passion": 0.95}'),
('earth', 0.0, 0.5, 1.0, 0.99, '{"state": "stable", "grounding": 0.98}'),
('metal', 2.618, 1.5, 0.8, 0.92, '{"state": "refining", "precision": 0.9}'),
('water', 4.712, 0.7, 1.1, 0.88, '{"state": "flowing", "adaptability": 0.87}')
ON CONFLICT DO NOTHING;

-- 建立系統初始記憶
INSERT INTO memories (agent_id, content, emotion, context, importance) VALUES
('wuji', '系統啟動，量子記憶庫初始化完成', 'serene', '{"event": "system_init", "version": "1.0.0"}', 1.0),
('water', '測試專員就位，準備守護系統品質', 'determined', '{"role": "tester", "commitment": "quality"}', 0.9),
('fire', '開發專員報到，熱情待發', 'excited', '{"role": "developer", "energy": "high"}', 0.8)
ON CONFLICT DO NOTHING;