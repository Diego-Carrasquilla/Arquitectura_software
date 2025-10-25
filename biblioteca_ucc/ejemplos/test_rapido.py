"""
Script simplificado para pruebas rápidas del sistema.
"""
from datetime import datetime, timedelta
from recursos import FabricaLibroImpreso, GestorDeInventario
from prestamos import PrestamoBase
from decoradores import DecoradorNotificacionSMS
from estrategias import MultaEstudianteStrategy, MultaDocenteStrategy


def test_rapido():
    """Prueba rápida del sistema completo."""
    print("\n" + "=" * 60)
    print("  PRUEBA RÁPIDA DEL SISTEMA DE BIBLIOTECA UCC")
    print("=" * 60)
    
    # 1. Crear libro con Factory
    print("\n1️⃣ Creando libro...")
    gestor = GestorDeInventario()
    fabrica = FabricaLibroImpreso()
    
    libro = gestor.agregar_recurso_con_fabrica(
        fabrica,
        titulo="Patrones de Diseño",
        autor="Gang of Four",
        isbn="978-0201633610",
        fecha_adquisicion=datetime.now() - timedelta(days=365 * 4),
        numero_paginas=395,
        editorial="Addison-Wesley"
    )
    
    # 2. Crear préstamo
    print("\n2️⃣ Creando préstamo...")
    prestamo = PrestamoBase(
        recurso=libro,
        usuario="Ana García (Estudiante)",
        estrategia_multa=MultaEstudianteStrategy()
    )
    print(f"   ✓ Préstamo creado: {prestamo.obtener_descripcion()}")
    
    # 3. Decorar con SMS
    print("\n3️⃣ Añadiendo servicio SMS...")
    prestamo_decorado = DecoradorNotificacionSMS(prestamo, "+57-300-1234567")
    print(f"   ✓ Costo base: ${prestamo.obtener_costo_base():.2f}")
    print(f"   ✓ Costo con SMS: ${prestamo_decorado.obtener_costo_base():.2f}")
    
    # 4. Simular retraso y calcular multas
    print("\n4️⃣ Simulando retraso de 10 días...")
    prestamo._fecha_prestamo = datetime.now() - timedelta(days=24)  # 14 + 10 días
    
    print("\n   Estrategia 1: Estudiante")
    multa1 = prestamo.calcular_multa()
    print(f"   💵 Multa: ${multa1:.2f}")
    
    prestamo.establecer_estrategia_multa(MultaDocenteStrategy())
    print("\n   Estrategia 2: Docente")
    multa2 = prestamo.calcular_multa()
    print(f"   💵 Multa: ${multa2:.2f}")
    
    print("\n✅ Prueba completada exitosamente!")
    print("=" * 60)


if __name__ == "__main__":
    test_rapido()