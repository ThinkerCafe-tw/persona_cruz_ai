"""
量子記憶系統
一個基於量子概念的 AI 記憶演化系統
"""

from .quantum_memory import QuantumMemory, MemoryCrystal, Possibility
from .quantum_bridge import QuantumMemoryBridge
from .evolution_engine import QuantumEvolutionEngine
from .quantum_monitor import QuantumMonitor

__version__ = "1.0.0"
__all__ = [
    'QuantumMemory',
    'MemoryCrystal', 
    'Possibility',
    'QuantumMemoryBridge',
    'QuantumEvolutionEngine',
    'QuantumMonitor'
]