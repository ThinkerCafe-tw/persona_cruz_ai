"""
量子記憶資料庫層
使用 PostgreSQL + pgvector 儲存和檢索量子記憶
"""
import os
import logging
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from psycopg2.pool import SimpleConnectionPool
import numpy as np
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class QuantumDatabase:
    """量子記憶資料庫管理器"""
    
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv('DATABASE_URL')
        self.pool = None
        
        if not self.database_url:
            raise ValueError("❌ 錯誤：未設定 DATABASE_URL！量子記憶系統需要 pgvector 資料庫。")
        
        if self.database_url:
            try:
                # Railway 提供的 DATABASE_URL 可能需要調整
                if self.database_url.startswith('postgres://'):
                    self.database_url = self.database_url.replace('postgres://', 'postgresql://')
                
                # 建立連接池
                self.pool = SimpleConnectionPool(
                    1, 10,  # 最小1個連接，最大10個
                    self.database_url
                )
                logger.info("✅ 資料庫連接池建立成功")
                
                # 初始化資料庫結構
                self._initialize_database()
            except Exception as e:
                logger.error(f"❌ 資料庫連接失敗: {e}")
                self.pool = None
                raise RuntimeError(f"量子記憶系統需要 pgvector 資料庫！錯誤: {e}")
    
    @contextmanager
    def get_connection(self):
        """從連接池獲取連接"""
        if not self.pool:
            yield None
            return
            
        conn = self.pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.pool.putconn(conn)
    
    def _initialize_database(self):
        """初始化資料庫結構"""
        with self.get_connection() as conn:
            if not conn:
                return
                
            with conn.cursor() as cur:
                # 啟用 pgvector 擴展
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
                
                # 建立量子記憶主表
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS quantum_memories (
                        id SERIAL PRIMARY KEY,
                        persona_id VARCHAR(50) NOT NULL,
                        identity_vector vector(5),
                        identity_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(persona_id)
                    )
                """)
                
                # 建立記憶晶體表
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS memory_crystals (
                        id SERIAL PRIMARY KEY,
                        memory_id INTEGER REFERENCES quantum_memories(id) ON DELETE CASCADE,
                        crystal_id VARCHAR(100) NOT NULL,
                        concept VARCHAR(255) NOT NULL,
                        concept_vector vector(384),
                        possibilities JSONB,
                        stability FLOAT DEFAULT 1.0,
                        entropy FLOAT DEFAULT 0.0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(memory_id, crystal_id)
                    )
                """)
                
                # 建立量子漣漪表
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS quantum_ripples (
                        id SERIAL PRIMARY KEY,
                        memory_id INTEGER REFERENCES quantum_memories(id) ON DELETE CASCADE,
                        event_data JSONB NOT NULL,
                        event_vector vector(384),
                        impact FLOAT DEFAULT 0.5,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # 建立量子糾纏表
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS quantum_entanglements (
                        id SERIAL PRIMARY KEY,
                        persona1_id VARCHAR(50) NOT NULL,
                        persona2_id VARCHAR(50) NOT NULL,
                        entanglement_strength FLOAT DEFAULT 0.0,
                        shared_concepts JSONB,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(persona1_id, persona2_id)
                    )
                """)
                
                # 建立索引
                cur.execute("CREATE INDEX IF NOT EXISTS idx_persona_id ON quantum_memories(persona_id)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_concept ON memory_crystals(concept)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_identity_vector ON quantum_memories USING ivfflat (identity_vector vector_cosine_ops)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_concept_vector ON memory_crystals USING ivfflat (concept_vector vector_cosine_ops)")
                
                logger.info("✅ 資料庫結構初始化完成")
    
    def save_quantum_memory(self, persona_id: str, identity_data: dict, 
                          identity_vector: Optional[List[float]] = None) -> Optional[int]:
        """儲存或更新量子記憶"""
        with self.get_connection() as conn:
            if not conn:
                return None
                
            with conn.cursor() as cur:
                if identity_vector:
                    cur.execute("""
                        INSERT INTO quantum_memories (persona_id, identity_data, identity_vector)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (persona_id) 
                        DO UPDATE SET 
                            identity_data = EXCLUDED.identity_data,
                            identity_vector = EXCLUDED.identity_vector,
                            updated_at = CURRENT_TIMESTAMP
                        RETURNING id
                    """, (persona_id, Json(identity_data), identity_vector))
                else:
                    cur.execute("""
                        INSERT INTO quantum_memories (persona_id, identity_data)
                        VALUES (%s, %s)
                        ON CONFLICT (persona_id) 
                        DO UPDATE SET 
                            identity_data = EXCLUDED.identity_data,
                            updated_at = CURRENT_TIMESTAMP
                        RETURNING id
                    """, (persona_id, Json(identity_data)))
                
                return cur.fetchone()[0]
    
    def get_quantum_memory(self, persona_id: str) -> Optional[Dict]:
        """獲取量子記憶"""
        with self.get_connection() as conn:
            if not conn:
                return None
                
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM quantum_memories 
                    WHERE persona_id = %s
                """, (persona_id,))
                
                return cur.fetchone()
    
    def save_memory_crystal(self, memory_id: int, crystal_data: dict,
                          concept_vector: Optional[List[float]] = None):
        """儲存記憶晶體"""
        with self.get_connection() as conn:
            if not conn:
                return
                
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO memory_crystals 
                    (memory_id, crystal_id, concept, possibilities, stability, entropy, concept_vector)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (memory_id, crystal_id)
                    DO UPDATE SET
                        possibilities = EXCLUDED.possibilities,
                        stability = EXCLUDED.stability,
                        entropy = EXCLUDED.entropy,
                        concept_vector = EXCLUDED.concept_vector,
                        updated_at = CURRENT_TIMESTAMP
                """, (
                    memory_id,
                    crystal_data['id'],
                    crystal_data['concept'],
                    Json(crystal_data.get('possibilities', [])),
                    crystal_data.get('stability', 1.0),
                    crystal_data.get('entropy', 0.0),
                    concept_vector
                ))
    
    def get_memory_crystals(self, memory_id: int) -> List[Dict]:
        """獲取記憶晶體"""
        with self.get_connection() as conn:
            if not conn:
                return []
                
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM memory_crystals
                    WHERE memory_id = %s
                    ORDER BY created_at DESC
                """, (memory_id,))
                
                return cur.fetchall()
    
    def save_ripple(self, memory_id: int, ripple_data: dict,
                   event_vector: Optional[List[float]] = None):
        """儲存量子漣漪"""
        with self.get_connection() as conn:
            if not conn:
                return
                
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO quantum_ripples
                    (memory_id, event_data, impact, event_vector)
                    VALUES (%s, %s, %s, %s)
                """, (
                    memory_id,
                    Json(ripple_data['event']),
                    ripple_data.get('impact', 0.5),
                    event_vector
                ))
    
    def get_ripples(self, memory_id: int, limit: int = 50) -> List[Dict]:
        """獲取量子漣漪"""
        with self.get_connection() as conn:
            if not conn:
                return []
                
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM quantum_ripples
                    WHERE memory_id = %s
                    ORDER BY timestamp DESC
                    LIMIT %s
                """, (memory_id, limit))
                
                return cur.fetchall()
    
    def search_similar_memories(self, vector: List[float], 
                              persona_id: Optional[str] = None,
                              limit: int = 10) -> List[Dict]:
        """搜尋相似的記憶"""
        with self.get_connection() as conn:
            if not conn:
                return []
                
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if persona_id:
                    cur.execute("""
                        SELECT 
                            m.*,
                            c.*,
                            c.concept_vector <=> %s::vector as distance
                        FROM memory_crystals c
                        JOIN quantum_memories m ON c.memory_id = m.id
                        WHERE m.persona_id = %s
                        ORDER BY distance
                        LIMIT %s
                    """, (vector, persona_id, limit))
                else:
                    cur.execute("""
                        SELECT 
                            m.*,
                            c.*,
                            c.concept_vector <=> %s::vector as distance
                        FROM memory_crystals c
                        JOIN quantum_memories m ON c.memory_id = m.id
                        ORDER BY distance
                        LIMIT %s
                    """, (vector, limit))
                
                return cur.fetchall()
    
    def update_entanglement(self, persona1_id: str, persona2_id: str,
                          strength: float, shared_concepts: List[str]):
        """更新量子糾纏"""
        # 確保 persona1_id < persona2_id 以避免重複
        if persona1_id > persona2_id:
            persona1_id, persona2_id = persona2_id, persona1_id
            
        with self.get_connection() as conn:
            if not conn:
                return
                
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO quantum_entanglements
                    (persona1_id, persona2_id, entanglement_strength, shared_concepts)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (persona1_id, persona2_id)
                    DO UPDATE SET
                        entanglement_strength = EXCLUDED.entanglement_strength,
                        shared_concepts = EXCLUDED.shared_concepts,
                        updated_at = CURRENT_TIMESTAMP
                """, (persona1_id, persona2_id, strength, Json(shared_concepts)))
    
    def get_entanglements(self, persona_id: str) -> List[Dict]:
        """獲取角色的所有糾纏關係"""
        with self.get_connection() as conn:
            if not conn:
                return []
                
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM quantum_entanglements
                    WHERE persona1_id = %s OR persona2_id = %s
                    ORDER BY entanglement_strength DESC
                """, (persona_id, persona_id))
                
                return cur.fetchall()
    
    def close(self):
        """關閉連接池"""
        if self.pool:
            self.pool.closeall()
            logger.info("資料庫連接池已關閉")