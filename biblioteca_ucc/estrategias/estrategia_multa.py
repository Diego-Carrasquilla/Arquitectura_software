"""
Módulo que implementa el patrón Strategy para el cálculo de multas.
Permite cambiar dinámicamente el algoritmo de cálculo según el tipo de usuario.
"""
from abc import ABC, abstractmethod
try:
    from ..recursos.recurso import Recurso
except ImportError:
    from recursos.recurso import Recurso


class IEstrategiaDeMulta(ABC):
    """
    Interfaz que define el contrato para todas las estrategias de multa.
    Patrón Strategy.
    """
    
    @abstractmethod
    def calcular_multa(self, dias_retraso: int, costo_base_recurso: float, 
                      recurso: Recurso) -> float:
        """
        Calcula la multa por retraso en la devolución.
        
        Args:
            dias_retraso: Número de días de retraso
            costo_base_recurso: Costo base del préstamo (incluyendo servicios)
            recurso: El recurso prestado (para considerar antigüedad u otros factores)
        
        Returns:
            Monto de la multa calculada
        """
        pass
    
    @abstractmethod
    def obtener_nombre_estrategia(self) -> str:
        """Retorna el nombre descriptivo de la estrategia."""
        pass


class MultaEstudianteStrategy(IEstrategiaDeMulta):
    """
    Estrategia de multa para estudiantes.
    Penalización estándar: $2.00 por día de retraso.
    Consideración: recursos más antiguos tienen menor multa (descuento por antigüedad).
    """
    
    TARIFA_BASE_DIA = 2.0
    ANTIGUEDAD_UMBRAL_DIAS = 365 * 5  # 5 años
    DESCUENTO_RECURSO_ANTIGUO = 0.5  # 50% de descuento
    
    def calcular_multa(self, dias_retraso: int, costo_base_recurso: float, 
                      recurso: Recurso) -> float:
        """
        Calcula multa para estudiantes con descuento por recursos antiguos.
        
        Formula:
        - Tarifa base: $2.00 por día
        - Si el recurso tiene más de 5 años: descuento del 50%
        - Multa mínima: $1.00
        """
        if dias_retraso <= 0:
            return 0.0
        
        multa = self.TARIFA_BASE_DIA * dias_retraso
        
        # Aplicar descuento si el recurso es antiguo
        antiguedad_dias = recurso.calcular_antiguedad_dias()
        if antiguedad_dias > self.ANTIGUEDAD_UMBRAL_DIAS:
            multa *= self.DESCUENTO_RECURSO_ANTIGUO
            print(f"  [INFO] Descuento por recurso antiguo aplicado ({antiguedad_dias} dias)")
        
        # Asegurar multa mínima
        multa = max(multa, 1.0)
        
        return round(multa, 2)
    
    def obtener_nombre_estrategia(self) -> str:
        return "Estrategia de Multa para Estudiantes"


class MultaDocenteStrategy(IEstrategiaDeMulta):
    """
    Estrategia de multa para docentes.
    Penalización reducida: $1.00 por día de retraso.
    Beneficio: sin multa los primeros 3 días de retraso (período de gracia).
    """
    
    TARIFA_BASE_DIA = 1.0
    DIAS_GRACIA = 3
    
    def calcular_multa(self, dias_retraso: int, costo_base_recurso: float, 
                      recurso: Recurso) -> float:
        """
        Calcula multa para docentes con período de gracia.
        
        Formula:
        - Período de gracia: primeros 3 días sin multa
        - Tarifa: $1.00 por día después del período de gracia
        - Beneficio docente: tarifa reducida
        """
        if dias_retraso <= 0:
            return 0.0
        
        # Aplicar período de gracia
        dias_penalizables = max(0, dias_retraso - self.DIAS_GRACIA)
        
        if dias_penalizables == 0:
            print(f"  [INFO] Periodo de gracia aplicado (0-{self.DIAS_GRACIA} dias)")
            return 0.0
        
        multa = self.TARIFA_BASE_DIA * dias_penalizables
        print(f"  [INFO] Multa calculada despues de {self.DIAS_GRACIA} dias de gracia")
        
        return round(multa, 2)
    
    def obtener_nombre_estrategia(self) -> str:
        return "Estrategia de Multa para Docentes"


class MultaRecargadaStrategy(IEstrategiaDeMulta):
    """
    Estrategia de multa recargada (para casos especiales o recursos de alta demanda).
    Penalización progresiva: aumenta con cada día adicional de retraso.
    """
    
    TARIFA_INICIAL = 3.0
    INCREMENTO_DIARIO = 0.5
    
    def calcular_multa(self, dias_retraso: int, costo_base_recurso: float, 
                      recurso: Recurso) -> float:
        """
        Calcula multa con penalización progresiva.
        
        Formula:
        - Primera semana: $3.00 por día
        - Cada día adicional: +$0.50 acumulativo
        - Ejemplo: día 1=$3, día 2=$6.50, día 3=$10.50, etc.
        """
        if dias_retraso <= 0:
            return 0.0
        
        # Multa progresiva: cada día cuesta más
        multa = 0.0
        for dia in range(1, dias_retraso + 1):
            tarifa_dia = self.TARIFA_INICIAL + (self.INCREMENTO_DIARIO * (dia - 1))
            multa += tarifa_dia
        
        print(f"  [INFO] Multa progresiva aplicada ({dias_retraso} dias)")
        
        return round(multa, 2)
    
    def obtener_nombre_estrategia(self) -> str:
        return "Estrategia de Multa Recargada (Progresiva)"


class MultaPorAntiguedadRecursoStrategy(IEstrategiaDeMulta):
    """
    Estrategia de multa basada en la antigüedad del recurso.
    Recursos nuevos (menos de 1 año) tienen multas más altas.
    Recursos antiguos (más de 5 años) tienen multas reducidas.
    """
    
    TARIFA_RECURSO_NUEVO = 5.0  # Menos de 1 año
    TARIFA_RECURSO_MEDIO = 2.5  # 1-5 años
    TARIFA_RECURSO_ANTIGUO = 1.0  # Más de 5 años
    
    def calcular_multa(self, dias_retraso: int, costo_base_recurso: float, 
                      recurso: Recurso) -> float:
        """
        Calcula multa basada en la antigüedad del recurso.
        
        Formula:
        - Recursos nuevos (<1 año): $5.00 por día
        - Recursos medios (1-5 años): $2.50 por día
        - Recursos antiguos (>5 años): $1.00 por día
        """
        if dias_retraso <= 0:
            return 0.0
        
        antiguedad_dias = recurso.calcular_antiguedad_dias()
        antiguedad_años = antiguedad_dias / 365
        
        # Determinar tarifa según antigüedad
        if antiguedad_años < 1:
            tarifa = self.TARIFA_RECURSO_NUEVO
            categoria = "Nuevo"
        elif antiguedad_años < 5:
            tarifa = self.TARIFA_RECURSO_MEDIO
            categoria = "Medio"
        else:
            tarifa = self.TARIFA_RECURSO_ANTIGUO
            categoria = "Antiguo"
        
        multa = tarifa * dias_retraso
        
        print(f"  [INFO] Recurso {categoria} ({antiguedad_años:.1f} años) - Tarifa: ${tarifa}/dia")
        
        return round(multa, 2)
    
    def obtener_nombre_estrategia(self) -> str:
        return "Estrategia de Multa por Antigüedad del Recurso"