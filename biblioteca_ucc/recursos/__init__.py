"""
Paquete de recursos de la biblioteca.
Implementa el patrón Factory Method para la creación de diferentes tipos de recursos.
"""
from .recurso import Recurso, LibroImpreso, Revista, RecursoDigital, TipoRecurso
from .fabrica_recursos import (
    FabricaDeRecursos,
    FabricaLibroImpreso,
    FabricaRevista,
    FabricaRecursoDigital,
    GestorDeInventario
)

__all__ = [
    'Recurso',
    'LibroImpreso',
    'Revista',
    'RecursoDigital',
    'TipoRecurso',
    'FabricaDeRecursos',
    'FabricaLibroImpreso',
    'FabricaRevista',
    'FabricaRecursoDigital',
    'GestorDeInventario'
]