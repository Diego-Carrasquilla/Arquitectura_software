"""
Paquete de decoradores para préstamos.
Implementa el patrón Decorator para añadir servicios adicionales.
"""
from .decorador_prestamo import (
    DecoradorPrestamo,
    DecoradorNotificacionSMS,
    DecoradorReservaPreferencial,
    DecoradorSeguroExtravio
)

__all__ = [
    'DecoradorPrestamo',
    'DecoradorNotificacionSMS',
    'DecoradorReservaPreferencial',
    'DecoradorSeguroExtravio'
]