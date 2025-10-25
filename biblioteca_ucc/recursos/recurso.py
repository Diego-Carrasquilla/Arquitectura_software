"""
Módulo que define la jerarquía de recursos de la biblioteca.
Implementa el patrón Factory Method para crear diferentes tipos de recursos.
"""
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timedelta


class TipoRecurso(Enum):
    """Enum para los tipos de recursos disponibles en la biblioteca."""
    LIBRO_IMPRESO = "libro_impreso"
    REVISTA = "revista"
    RECURSO_DIGITAL = "recurso_digital"


class Recurso(ABC):
    """Clase abstracta que define la interfaz común para todos los recursos."""
    
    def __init__(self, titulo: str, autor: str, isbn: str, fecha_adquisicion: datetime):
        self._titulo = titulo
        self._autor = autor
        self._isbn = isbn
        self._fecha_adquisicion = fecha_adquisicion
        self._disponible = True
    
    @property
    def titulo(self) -> str:
        return self._titulo
    
    @property
    def autor(self) -> str:
        return self._autor
    
    @property
    def isbn(self) -> str:
        return self._isbn
    
    @property
    def fecha_adquisicion(self) -> datetime:
        return self._fecha_adquisicion
    
    @property
    def disponible(self) -> bool:
        return self._disponible
    
    def cambiar_disponibilidad(self, disponible: bool):
        """Cambia el estado de disponibilidad del recurso."""
        self._disponible = disponible
    
    def calcular_antiguedad_dias(self) -> int:
        """Calcula la antigüedad del recurso en días."""
        return (datetime.now() - self._fecha_adquisicion).days
    
    @abstractmethod
    def obtener_duracion_prestamo_base(self) -> int:
        """Retorna la duración base del préstamo en días para este tipo de recurso."""
        pass
    
    @abstractmethod
    def obtener_tipo_recurso(self) -> str:
        """Retorna una descripción del tipo de recurso."""
        pass
    
    def __str__(self) -> str:
        return f"{self.obtener_tipo_recurso()}: {self._titulo} por {self._autor}"


class LibroImpreso(Recurso):
    """Recurso de tipo libro impreso."""
    
    def __init__(self, titulo: str, autor: str, isbn: str, fecha_adquisicion: datetime, 
                 numero_paginas: int, editorial: str):
        super().__init__(titulo, autor, isbn, fecha_adquisicion)
        self._numero_paginas = numero_paginas
        self._editorial = editorial
    
    @property
    def numero_paginas(self) -> int:
        return self._numero_paginas
    
    @property
    def editorial(self) -> str:
        return self._editorial
    
    def obtener_duracion_prestamo_base(self) -> int:
        """Los libros impresos tienen un préstamo base de 14 días."""
        return 14
    
    def obtener_tipo_recurso(self) -> str:
        return "Libro Impreso"


class Revista(Recurso):
    """Recurso de tipo revista."""
    
    def __init__(self, titulo: str, autor: str, isbn: str, fecha_adquisicion: datetime,
                 numero_edicion: int, mes_publicacion: str):
        super().__init__(titulo, autor, isbn, fecha_adquisicion)
        self._numero_edicion = numero_edicion
        self._mes_publicacion = mes_publicacion
    
    @property
    def numero_edicion(self) -> int:
        return self._numero_edicion
    
    @property
    def mes_publicacion(self) -> str:
        return self._mes_publicacion
    
    def obtener_duracion_prestamo_base(self) -> int:
        """Las revistas tienen un préstamo base de 7 días."""
        return 7
    
    def obtener_tipo_recurso(self) -> str:
        return "Revista"


class RecursoDigital(Recurso):
    """Recurso de tipo digital."""
    
    def __init__(self, titulo: str, autor: str, isbn: str, fecha_adquisicion: datetime,
                 formato: str, tamaño_mb: float, url_acceso: str):
        super().__init__(titulo, autor, isbn, fecha_adquisicion)
        self._formato = formato
        self._tamaño_mb = tamaño_mb
        self._url_acceso = url_acceso
    
    @property
    def formato(self) -> str:
        return self._formato
    
    @property
    def tamaño_mb(self) -> float:
        return self._tamaño_mb
    
    @property
    def url_acceso(self) -> str:
        return self._url_acceso
    
    def obtener_duracion_prestamo_base(self) -> int:
        """Los recursos digitales tienen un préstamo base de 30 días."""
        return 30
    
    def obtener_tipo_recurso(self) -> str:
        return "Recurso Digital"