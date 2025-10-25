"""
Módulo que implementa el patrón Factory Method para la creación de recursos.
Permite crear diferentes tipos de recursos sin que el código cliente conozca los detalles de implementación.
"""
from abc import ABC, abstractmethod
from datetime import datetime
try:
    from .recurso import Recurso, LibroImpreso, Revista, RecursoDigital
except ImportError:
    from recursos.recurso import Recurso, LibroImpreso, Revista, RecursoDigital


class FabricaDeRecursos(ABC):
    """
    Clase abstracta que define la interfaz para crear recursos.
    Patrón Factory Method.
    """
    
    @abstractmethod
    def crear_recurso(self, **kwargs) -> Recurso:
        """
        Método factory que debe ser implementado por las fábricas concretas.
        Retorna un objeto Recurso específico.
        """
        pass
    
    def registrar_recurso(self, **kwargs) -> Recurso:
        """
        Método template que realiza operaciones comunes antes de crear el recurso.
        Principio Open/Closed: abierto a extensión, cerrado a modificación.
        """
        recurso = self.crear_recurso(**kwargs)
        print(f"[OK] Recurso registrado: {recurso}")
        return recurso


class FabricaLibroImpreso(FabricaDeRecursos):
    """Fábrica concreta para crear libros impresos."""
    
    def crear_recurso(self, **kwargs) -> LibroImpreso:
        """
        Crea y retorna un objeto LibroImpreso.
        
        Args:
            titulo: Título del libro
            autor: Autor del libro
            isbn: Código ISBN
            fecha_adquisicion: Fecha de adquisición del libro
            numero_paginas: Número de páginas
            editorial: Editorial del libro
        """
        return LibroImpreso(
            titulo=kwargs.get('titulo'),
            autor=kwargs.get('autor'),
            isbn=kwargs.get('isbn'),
            fecha_adquisicion=kwargs.get('fecha_adquisicion', datetime.now()),
            numero_paginas=kwargs.get('numero_paginas'),
            editorial=kwargs.get('editorial')
        )


class FabricaRevista(FabricaDeRecursos):
    """Fábrica concreta para crear revistas."""
    
    def crear_recurso(self, **kwargs) -> Revista:
        """
        Crea y retorna un objeto Revista.
        
        Args:
            titulo: Título de la revista
            autor: Autor/Editor
            isbn: Código ISBN
            fecha_adquisicion: Fecha de adquisición
            numero_edicion: Número de edición
            mes_publicacion: Mes de publicación
        """
        return Revista(
            titulo=kwargs.get('titulo'),
            autor=kwargs.get('autor'),
            isbn=kwargs.get('isbn'),
            fecha_adquisicion=kwargs.get('fecha_adquisicion', datetime.now()),
            numero_edicion=kwargs.get('numero_edicion'),
            mes_publicacion=kwargs.get('mes_publicacion')
        )


class FabricaRecursoDigital(FabricaDeRecursos):
    """Fábrica concreta para crear recursos digitales."""
    
    def crear_recurso(self, **kwargs) -> RecursoDigital:
        """
        Crea y retorna un objeto RecursoDigital.
        
        Args:
            titulo: Título del recurso
            autor: Autor del recurso
            isbn: Código ISBN
            fecha_adquisicion: Fecha de adquisición
            formato: Formato del archivo (PDF, EPUB, etc.)
            tamaño_mb: Tamaño en megabytes
            url_acceso: URL de acceso al recurso
        """
        return RecursoDigital(
            titulo=kwargs.get('titulo'),
            autor=kwargs.get('autor'),
            isbn=kwargs.get('isbn'),
            fecha_adquisicion=kwargs.get('fecha_adquisicion', datetime.now()),
            formato=kwargs.get('formato'),
            tamaño_mb=kwargs.get('tamaño_mb'),
            url_acceso=kwargs.get('url_acceso')
        )


class GestorDeInventario:
    """
    Gestor de inventario que utiliza las fábricas para crear recursos.
    Demuestra el desacoplamiento: no conoce los detalles de construcción de los recursos.
    """
    
    def __init__(self):
        self._recursos = []
    
    def agregar_recurso_con_fabrica(self, fabrica: FabricaDeRecursos, **kwargs) -> Recurso:
        """
        Agrega un recurso al inventario usando una fábrica específica.
        
        Args:
            fabrica: Instancia de una fábrica concreta
            **kwargs: Parámetros necesarios para crear el recurso
        
        Returns:
            El recurso creado
        """
        recurso = fabrica.registrar_recurso(**kwargs)
        self._recursos.append(recurso)
        return recurso
    
    def listar_recursos(self):
        """Lista todos los recursos en el inventario."""
        print("\n" + "="*60)
        print("INVENTARIO DE RECURSOS")
        print("="*60)
        for i, recurso in enumerate(self._recursos, 1):
            disponibilidad = "[OK] Disponible" if recurso.disponible else "[X] No disponible"
            print(f"{i}. {recurso} - {disponibilidad}")
            print(f"   ISBN: {recurso.isbn} | Antigüedad: {recurso.calcular_antiguedad_dias()} días")
        print("="*60)
    
    def obtener_recurso_por_isbn(self, isbn: str) -> Recurso:
        """Busca y retorna un recurso por su ISBN."""
        for recurso in self._recursos:
            if recurso.isbn == isbn:
                return recurso
        return None
    
    @property
    def recursos(self):
        return self._recursos.copy()