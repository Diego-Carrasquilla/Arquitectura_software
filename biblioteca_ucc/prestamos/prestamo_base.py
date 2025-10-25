"""
Módulo que define el préstamo base y su integración con estrategias de multa.
"""
from datetime import datetime, timedelta
try:
    from .iprestamo import IPrestamo
    from ..recursos.recurso import Recurso
except ImportError:
    from prestamos.iprestamo import IPrestamo
    from recursos.recurso import Recurso


class PrestamoBase(IPrestamo):
    """
    Clase base que representa un préstamo simple sin servicios adicionales.
    Es el componente concreto que puede ser decorado.
    """
    
    def __init__(self, recurso: Recurso, usuario: str, estrategia_multa=None):
        """
        Inicializa un préstamo base.
        
        Args:
            recurso: El recurso que se está prestando
            usuario: Nombre del usuario que realiza el préstamo
            estrategia_multa: Estrategia para calcular multas (patrón Strategy)
        """
        self._recurso = recurso
        self._usuario = usuario
        self._fecha_prestamo = datetime.now()
        self._estrategia_multa = estrategia_multa
        self._costo_base = 0.0  # Costo base del préstamo (puede ser 0 para servicios gratuitos)
        
        # Marcar el recurso como no disponible
        self._recurso.cambiar_disponibilidad(False)
    
    @property
    def recurso(self) -> Recurso:
        return self._recurso
    
    @property
    def usuario(self) -> str:
        return self._usuario
    
    @property
    def fecha_prestamo(self) -> datetime:
        return self._fecha_prestamo
    
    @property
    def estrategia_multa(self):
        return self._estrategia_multa
    
    def establecer_estrategia_multa(self, estrategia):
        """
        Permite cambiar la estrategia de cálculo de multa en tiempo de ejecución.
        Demuestra el patrón Strategy.
        """
        self._estrategia_multa = estrategia
    
    def obtener_duracion_dias(self) -> int:
        """
        Retorna la duración base del préstamo según el tipo de recurso.
        """
        return self._recurso.obtener_duracion_prestamo_base()
    
    def obtener_costo_base(self) -> float:
        """Retorna el costo base del préstamo (sin servicios adicionales)."""
        return self._costo_base
    
    def obtener_descripcion(self) -> str:
        """Retorna una descripción del préstamo."""
        return f"Préstamo de '{self._recurso.titulo}' a {self._usuario}"
    
    def obtener_fecha_devolucion(self) -> datetime:
        """Calcula y retorna la fecha límite de devolución."""
        return self._fecha_prestamo + timedelta(days=self.obtener_duracion_dias())
    
    def calcular_dias_retraso(self) -> int:
        """
        Calcula los días de retraso si el préstamo está vencido.
        Retorna 0 si no hay retraso.
        """
        fecha_devolucion = self.obtener_fecha_devolucion()
        if datetime.now() > fecha_devolucion:
            return (datetime.now() - fecha_devolucion).days
        return 0
    
    def calcular_multa(self) -> float:
        """
        Calcula la multa por retraso usando la estrategia asignada.
        Demuestra la integración del patrón Strategy.
        """
        if self._estrategia_multa is None:
            raise ValueError("No se ha establecido una estrategia de multa para este préstamo")
        
        dias_retraso = self.calcular_dias_retraso()
        if dias_retraso <= 0:
            return 0.0
        
        # Delegar el cálculo a la estrategia
        return self._estrategia_multa.calcular_multa(
            dias_retraso=dias_retraso,
            costo_base_recurso=self.obtener_costo_base(),
            recurso=self._recurso
        )
    
    def devolver_recurso(self):
        """Marca el recurso como disponible nuevamente."""
        self._recurso.cambiar_disponibilidad(True)
        print(f"[OK] Recurso '{self._recurso.titulo}' devuelto por {self._usuario}")
    
    def __str__(self) -> str:
        return (f"{self.obtener_descripcion()}\n"
                f"  Fecha préstamo: {self._fecha_prestamo.strftime('%Y-%m-%d')}\n"
                f"  Fecha devolución: {self.obtener_fecha_devolucion().strftime('%Y-%m-%d')}\n"
                f"  Duración: {self.obtener_duracion_dias()} días\n"
                f"  Costo: ${self.obtener_costo_base():.2f}")