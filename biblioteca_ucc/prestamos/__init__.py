"""
Paquete de préstamos.
Define la interfaz y clase base para préstamos.
"""
from .iprestamo import IPrestamo
from .prestamo_base import PrestamoBase

__all__ = [
    'IPrestamo',
    'PrestamoBase'
]