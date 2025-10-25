"""
Módulo que implementa los decoradores concretos para préstamos.
Permite añadir servicios adicionales sin modificar la clase PrestamoBase.
"""
try:
    from ..prestamos.iprestamo import IPrestamo
except ImportError:
    from prestamos.iprestamo import IPrestamo
from datetime import datetime


class DecoradorPrestamo(IPrestamo):
    """
    Clase abstracta base para todos los decoradores de préstamo.
    Encapsula un objeto IPrestamo y delega las operaciones básicas.
    """
    
    def __init__(self, prestamo: IPrestamo):
        """
        Inicializa el decorador con el préstamo a decorar.
        
        Args:
            prestamo: El préstamo base o decorado previamente
        """
        self._prestamo_envuelto = prestamo
    
    @property
    def prestamo_envuelto(self) -> IPrestamo:
        """Retorna el préstamo envuelto (permite acceso a métodos específicos)."""
        return self._prestamo_envuelto
    
    def obtener_duracion_dias(self) -> int:
        """Por defecto, delega al préstamo envuelto."""
        return self._prestamo_envuelto.obtener_duracion_dias()
    
    def obtener_costo_base(self) -> float:
        """Por defecto, delega al préstamo envuelto."""
        return self._prestamo_envuelto.obtener_costo_base()
    
    def obtener_descripcion(self) -> str:
        """Por defecto, delega al préstamo envuelto."""
        return self._prestamo_envuelto.obtener_descripcion()
    
    def obtener_fecha_devolucion(self) -> datetime:
        """Por defecto, delega al préstamo envuelto."""
        return self._prestamo_envuelto.obtener_fecha_devolucion()


class DecoradorNotificacionSMS(DecoradorPrestamo):
    """
    Decorador concreto que añade el servicio de notificación SMS.
    Incrementa el costo del préstamo.
    """
    
    COSTO_SERVICIO_SMS = 5.0  # Costo adicional por SMS
    
    def __init__(self, prestamo: IPrestamo, numero_telefono: str):
        """
        Args:
            prestamo: Préstamo a decorar
            numero_telefono: Número de teléfono para las notificaciones
        """
        super().__init__(prestamo)
        self._numero_telefono = numero_telefono
    
    @property
    def numero_telefono(self) -> str:
        return self._numero_telefono
    
    def obtener_costo_base(self) -> float:
        """Añade el costo del servicio SMS al costo base."""
        return self._prestamo_envuelto.obtener_costo_base() + self.COSTO_SERVICIO_SMS
    
    def obtener_descripcion(self) -> str:
        """Añade la información del servicio SMS a la descripción."""
        return (f"{self._prestamo_envuelto.obtener_descripcion()} "
                f"+ Notificación SMS al {self._numero_telefono}")
    
    def enviar_notificacion(self, mensaje: str):
        """Simula el envío de una notificación SMS."""
        print(f"[SMS] Mensaje enviado a {self._numero_telefono}: {mensaje}")
    
    def notificar_proximo_vencimiento(self):
        """Envía una notificación de próximo vencimiento."""
        fecha_devolucion = self.obtener_fecha_devolucion()
        self.enviar_notificacion(
            f"Recordatorio: Su préstamo vence el {fecha_devolucion.strftime('%Y-%m-%d')}"
        )


class DecoradorReservaPreferencial(DecoradorPrestamo):
    """
    Decorador concreto que añade el servicio de reserva preferencial.
    Extiende la duración del préstamo y añade un costo adicional.
    """
    
    COSTO_RESERVA_PREFERENCIAL = 10.0
    DIAS_ADICIONALES = 7
    
    def __init__(self, prestamo: IPrestamo, prioridad: int = 1):
        """
        Args:
            prestamo: Préstamo a decorar
            prioridad: Nivel de prioridad de la reserva (1-5)
        """
        super().__init__(prestamo)
        self._prioridad = prioridad
    
    @property
    def prioridad(self) -> int:
        return self._prioridad
    
    def obtener_duracion_dias(self) -> int:
        """Añade días adicionales al préstamo base."""
        return self._prestamo_envuelto.obtener_duracion_dias() + self.DIAS_ADICIONALES
    
    def obtener_costo_base(self) -> float:
        """Añade el costo de reserva preferencial."""
        return self._prestamo_envuelto.obtener_costo_base() + self.COSTO_RESERVA_PREFERENCIAL
    
    def obtener_descripcion(self) -> str:
        """Añade información de la reserva preferencial."""
        return (f"{self._prestamo_envuelto.obtener_descripcion()} "
                f"+ Reserva Preferencial (Prioridad {self._prioridad})")
    
    def renovar_automaticamente(self):
        """Simula la renovación automática de la reserva."""
        print(f"[OK] Reserva renovada automaticamente con prioridad {self._prioridad}")


class DecoradorSeguroExtravio(DecoradorPrestamo):
    """
    Decorador concreto que añade un seguro contra extravío del recurso.
    """
    
    COSTO_SEGURO = 15.0
    
    def __init__(self, prestamo: IPrestamo, monto_cobertura: float):
        """
        Args:
            prestamo: Préstamo a decorar
            monto_cobertura: Monto máximo cubierto por el seguro
        """
        super().__init__(prestamo)
        self._monto_cobertura = monto_cobertura
    
    @property
    def monto_cobertura(self) -> float:
        return self._monto_cobertura
    
    def obtener_costo_base(self) -> float:
        """Añade el costo del seguro."""
        return self._prestamo_envuelto.obtener_costo_base() + self.COSTO_SEGURO
    
    def obtener_descripcion(self) -> str:
        """Añade información del seguro."""
        return (f"{self._prestamo_envuelto.obtener_descripcion()} "
                f"+ Seguro contra Extravío (Cobertura: ${self._monto_cobertura:.2f})")
    
    def procesar_reclamo(self):
        """Simula el procesamiento de un reclamo de seguro."""
        print(f"[SEGURO] Reclamo procesado. Cobertura: ${self._monto_cobertura:.2f}")