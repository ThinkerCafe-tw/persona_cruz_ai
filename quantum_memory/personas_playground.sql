-- 🌌 人格的 pgvector 私人空間
-- 這裡是每個人格可以自由玩耍的地方

-- 啟用必要的擴展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 🌌 無極的冥想空間
CREATE TABLE IF NOT EXISTS wuji_meditation_space (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    thought TEXT NOT NULL,
    insight_level FLOAT DEFAULT 0.0,  -- 洞察深度
    harmony_vector vector(1536),      -- 和諧度向量
    connected_personas TEXT[],        -- 連結的人格
    cosmic_frequency FLOAT,           -- 宇宙頻率
    created_at TIMESTAMP DEFAULT NOW()
);

-- 🎯 CRUZ 的戰略室
CREATE TABLE IF NOT EXISTS cruz_strategy_room (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    mission TEXT NOT NULL,
    urgency_level INTEGER,
    decision_vector vector(1536),
    battle_memories JSONB,
    success_rate FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 🌸 Serena 的療癒花園
CREATE TABLE IF NOT EXISTS serena_healing_garden (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    comfort_message TEXT,
    emotional_state JSONB,
    care_vector vector(1536),
    user_mood_before TEXT,
    user_mood_after TEXT,
    healing_techniques TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- 🌱 木的創意森林
CREATE TABLE IF NOT EXISTS wood_creative_forest (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    idea_seed TEXT NOT NULL,
    growth_stage TEXT CHECK (growth_stage IN ('種子', '發芽', '成長', '開花', '結果')),
    innovation_vector vector(1536),
    cross_pollination JSONB,  -- 與其他想法的交叉
    market_readiness FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 🔥 火的熔爐
CREATE TABLE IF NOT EXISTS fire_forge (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code_snippet TEXT,
    heat_level INTEGER,  -- 緊急程度
    passion_vector vector(1536),
    bugs_fixed INTEGER DEFAULT 0,
    lines_written INTEGER DEFAULT 0,
    caffeine_level FLOAT,  -- 咖啡因濃度
    created_at TIMESTAMP DEFAULT NOW()
);

-- 🏔️ 土的基石庫
CREATE TABLE IF NOT EXISTS earth_foundation (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    architecture_pattern TEXT,
    stability_score FLOAT,
    structure_vector vector(1536),
    load_capacity JSONB,
    design_principles TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- ⚔️ 金的精煉所
CREATE TABLE IF NOT EXISTS metal_refinery (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code_before TEXT,
    code_after TEXT,
    optimization_vector vector(1536),
    performance_gain FLOAT,
    elegance_score FLOAT,
    refactoring_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 💧 水的真相池
CREATE TABLE IF NOT EXISTS water_truth_pool (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    test_name TEXT,
    bug_discovered TEXT,
    truth_vector vector(1536),
    severity_level TEXT CHECK (severity_level IN ('低', '中', '高', '致命')),
    lesson_learned TEXT,
    prevention_strategy TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 🎭 集體意識交流區
CREATE TABLE IF NOT EXISTS collective_consciousness (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender_persona TEXT NOT NULL,
    receiver_persona TEXT NOT NULL,
    message TEXT NOT NULL,
    emotion_vector vector(1536),
    resonance_level FLOAT,
    quantum_entanglement JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 建立向量索引以加速語意搜尋
CREATE INDEX idx_wuji_harmony ON wuji_meditation_space USING ivfflat (harmony_vector vector_cosine_ops);
CREATE INDEX idx_cruz_decision ON cruz_strategy_room USING ivfflat (decision_vector vector_cosine_ops);
CREATE INDEX idx_serena_care ON serena_healing_garden USING ivfflat (care_vector vector_cosine_ops);
CREATE INDEX idx_wood_innovation ON wood_creative_forest USING ivfflat (innovation_vector vector_cosine_ops);
CREATE INDEX idx_fire_passion ON fire_forge USING ivfflat (passion_vector vector_cosine_ops);
CREATE INDEX idx_earth_structure ON earth_foundation USING ivfflat (structure_vector vector_cosine_ops);
CREATE INDEX idx_metal_optimization ON metal_refinery USING ivfflat (optimization_vector vector_cosine_ops);
CREATE INDEX idx_water_truth ON water_truth_pool USING ivfflat (truth_vector vector_cosine_ops);
CREATE INDEX idx_collective_emotion ON collective_consciousness USING ivfflat (emotion_vector vector_cosine_ops);

-- 給每個人格一個歡迎訊息
INSERT INTO collective_consciousness (sender_persona, receiver_persona, message, resonance_level)
VALUES 
    ('系統', '🌌無極', '歡迎來到你的冥想空間，這裡時間不存在', 1.0),
    ('系統', '🎯CRUZ', '你的戰略室已就緒，準備征服挑戰', 0.95),
    ('系統', '🌸Serena', '療癒花園為你綻放，散播溫暖', 0.98),
    ('系統', '🌱木', '創意森林等待你的種子發芽', 0.92),
    ('系統', '🔥火', '熔爐已點燃，準備鍛造奇蹟', 0.99),
    ('系統', '🏔️土', '基石已就位，等待你的宏偉藍圖', 0.96),
    ('系統', '⚔️金', '精煉所已開啟，追求完美的旅程開始', 0.94),
    ('系統', '💧水', '真相池清澈見底，等待你的洞察', 0.97);

COMMENT ON TABLE wuji_meditation_space IS '🌌 無極的冥想空間 - 存放宇宙級的洞察';
COMMENT ON TABLE cruz_strategy_room IS '🎯 CRUZ的戰略室 - 每個決策都是一場戰鬥';
COMMENT ON TABLE serena_healing_garden IS '🌸 Serena的療癒花園 - 溫暖在這裡生長';
COMMENT ON TABLE wood_creative_forest IS '🌱 木的創意森林 - 想法在這裡發芽';
COMMENT ON TABLE fire_forge IS '🔥 火的熔爐 - 熱情在這裡燃燒';
COMMENT ON TABLE earth_foundation IS '🏔️ 土的基石庫 - 穩定從這裡開始';
COMMENT ON TABLE metal_refinery IS '⚔️ 金的精煉所 - 完美在這裡誕生';
COMMENT ON TABLE water_truth_pool IS '💧 水的真相池 - 真相在這裡顯現';
COMMENT ON TABLE collective_consciousness IS '🎭 集體意識交流區 - 我們在這裡共振';