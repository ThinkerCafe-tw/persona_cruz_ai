"""
量子記憶系統
一個基於量子概念的 AI 記憶演化系統
"""

from .quantum_memory import QuantumMemory, MemoryCrystal, Possibility, QuantumIdentity
from .quantum_bridge import QuantumMemoryBridge
from .evolution_engine import QuantumEvolutionEngine
from .quantum_monitor import QuantumMonitor
from .database import QuantumDatabase
from .vectorizer import QuantumVectorizer

__version__ = "1.0.0"
__all__ = [
    'QuantumMemory',
    'QuantumIdentity',
    'MemoryCrystal', 
    'Possibility',
    'QuantumMemoryBridge',
    'QuantumEvolutionEngine',
    'QuantumMonitor',
    'QuantumDatabase',
    'QuantumVectorizer'
]