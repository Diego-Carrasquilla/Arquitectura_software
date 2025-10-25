"""
Script de prueba para demostrar el módulo de facturación.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from datetime import datetime, timedelta
from recursos import FabricaLibroImpreso, GestorDeInventario
from prestamos import PrestamoBase
from decoradores import DecoradorNotificacionSMS, DecoradorReservaPreferencial, DecoradorSeguroExtravio
from estrategias import MultaEstudianteStrategy, MultaDocenteStrategy
from facturacion import GestorFacturacion


def demo_facturacion():
    """Demostración del sistema de facturación."""
    print("\n" + "=" * 80)
    print("||" + " " * 76 + "||")
    print("||" + " " * 20 + "DEMO: SISTEMA DE FACTURACION" + " " * 28 + "||")
    print("||" + " " * 76 + "||")
    print("=" * 80)
    
    # 1. Crear recurso
    print("\n[PASO 1] Creando recurso...")
    gestor = GestorDeInventario()
    fabrica = FabricaLibroImpreso()
    libro = gestor.agregar_recurso_con_fabrica(
        fabrica,
        titulo="Clean Code: A Handbook of Agile Software Craftsmanship",
        autor="Robert C. Martin",
        isbn="978-0132350884",
        fecha_adquisicion=datetime.now() - timedelta(days=365 * 3),
        numero_paginas=464,
        editorial="Prentice Hall"
    )
    
    # 2. Crear préstamo con decoradores
    print("\n[PASO 2] Creando prestamo con servicios adicionales...")
    prestamo_base = PrestamoBase(
        recurso=libro,
        usuario="Maria Rodriguez (Estudiante)",
        estrategia_multa=MultaEstudianteStrategy()
    )
    
    # Aplicar decoradores
    prestamo = DecoradorNotificacionSMS(prestamo_base, "+57-300-1234567")
    prestamo = DecoradorReservaPreferencial(prestamo, prioridad=3)
    prestamo = DecoradorSeguroExtravio(prestamo, monto_cobertura=150000.0)
    
    print(f"   Servicios contratados:")
    print(f"   - Notificacion SMS: +$5.00")
    print(f"   - Reserva Preferencial: +$10.00")
    print(f"   - Seguro contra Extravio: +$15.00")
    print(f"   Costo total de servicios: ${prestamo.obtener_costo_base():.2f}")
    
    # 3. Simular retraso
    print("\n[PASO 3] Simulando retraso de 12 dias...")
    prestamo_base._fecha_prestamo = datetime.now() - timedelta(days=26)  # 14 + 12
    dias_retraso = prestamo_base.calcular_dias_retraso()
    print(f"   Dias de retraso: {dias_retraso}")
    
    # 4. Generar factura SIN multa
    print("\n[PASO 4] Generando factura SOLO POR SERVICIOS...")
    print("-" * 80)
    gestor_facturacion = GestorFacturacion()
    factura1 = gestor_facturacion.crear_factura(prestamo, prestamo_base, incluir_multa=False)
    print(factura1.generar_factura_texto(incluir_multa=False))
    
    input("\n>>> Presione ENTER para ver factura CON MULTA...")
    
    # 5. Generar factura CON multa
    print("\n[PASO 5] Generando factura INCLUYENDO MULTAS...")
    print("-" * 80)
    factura2 = gestor_facturacion.crear_factura(prestamo, prestamo_base, incluir_multa=True)
    print(factura2.generar_factura_texto(incluir_multa=False))
    
    # 6. Crear otro préstamo sin servicios pero con multa (Docente)
    input("\n>>> Presione ENTER para ver factura de DOCENTE con multa...")
    
    print("\n[PASO 6] Creando prestamo de docente con multa...")
    libro.cambiar_disponibilidad(True)
    prestamo_docente_base = PrestamoBase(
        recurso=libro,
        usuario="Dr. Carlos Mendez (Docente)",
        estrategia_multa=MultaDocenteStrategy()
    )
    
    # Simular 10 días de retraso
    prestamo_docente_base._fecha_prestamo = datetime.now() - timedelta(days=24)  # 14 + 10
    
    factura3 = gestor_facturacion.crear_factura(
        prestamo_docente_base, 
        prestamo_docente_base, 
        incluir_multa=True
    )
    print(factura3.generar_factura_texto(incluir_multa=False))
    
    # 7. Reporte final
    input("\n>>> Presione ENTER para ver reporte de facturacion...")
    
    print("\n" + "=" * 80)
    print("||" + " " * 76 + "||")
    print("||" + " " * 25 + "REPORTE DE FACTURACION" + " " * 29 + "||")
    print("||" + " " * 76 + "||")
    print("=" * 80)
    
    print(f"\nTotal de facturas generadas: {gestor_facturacion.obtener_cantidad_facturas()}")
    print(f"Total facturado: ${gestor_facturacion.obtener_total_facturado():.2f}")
    
    print("\n[DETALLE POR FACTURA]")
    print("-" * 80)
    for i, factura in enumerate(gestor_facturacion.facturas_generadas, 1):
        items, subtotal, total = factura.obtener_resumen()
        print(f"{i}. {factura.numero_factura}")
        print(f"   Cliente: {factura.prestamo_base.usuario}")
        print(f"   Items: {items}")
        print(f"   Total: ${total:.2f}")
        print()
    
    print("=" * 80)
    print("\n[OK] Demostracion de facturacion completada!")
    print("     El sistema permite generar facturas detalladas con:")
    print("     - Servicios contratados (decoradores)")
    print("     - Multas por retraso (estrategias)")
    print("     - Formato profesional para impresion")
    print("=" * 80)


if __name__ == "__main__":
    try:
        demo_facturacion()
    except KeyboardInterrupt:
        print("\n\n[INFO] Demo interrumpida por el usuario.")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()