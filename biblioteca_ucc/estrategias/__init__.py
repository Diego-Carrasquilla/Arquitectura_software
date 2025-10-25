"""
Paquete de estrategias de multa.
Implementa el patrón Strategy para calcular multas de forma intercambiable.
"""
from .estrategia_multa import (
    IEstrategiaDeMulta,
    MultaEstudianteStrategy,
    MultaDocenteStrategy,
    MultaRecargadaStrategy,
    MultaPorAntiguedadRecursoStrategy
)

__all__ = [
    'IEstrategiaDeMulta',
    'MultaEstudianteStrategy',
    'MultaDocenteStrategy',
    'MultaRecargadaStrategy',
    'MultaPorAntiguedadRecursoStrategy'
]