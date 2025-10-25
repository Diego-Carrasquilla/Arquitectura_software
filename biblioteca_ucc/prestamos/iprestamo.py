"""
Módulo que implementa el patrón Decorator para préstamos.
Permite añadir servicios adicionales a un préstamo de forma dinámica.
"""
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional


class IPrestamo(ABC):
    """
    Interfaz que define el contrato para todos los préstamos.
    Permite que decoradores y préstamos base sean intercambiables.
    """
    
    @abstractmethod
    def obtener_duracion_dias(self) -> int:
        """Retorna la duración del préstamo en días."""
        pass
    
    @abstractmethod
    def obtener_costo_base(self) -> float:
        """Retorna el costo base del préstamo."""
        pass
    
    @abstractmethod
    def obtener_descripcion(self) -> str:
        """Retorna una descripción del préstamo y sus servicios."""
        pass
    
    @abstractmethod
    def obtener_fecha_devolucion(self) -> datetime:
        """Retorna la fecha límite de devolución."""
        pass