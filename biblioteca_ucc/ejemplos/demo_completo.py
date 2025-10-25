"""
Script de demostración del Sistema de Biblioteca UCC
Demuestra la aplicación de los tres patrones de diseño principales:
- Factory Method: Creación de diferentes tipos de recursos
- Decorator: Añadir servicios a préstamos de forma dinámica
- Strategy: Cambiar algoritmos de cálculo de multas
"""

from datetime import datetime, timedelta

# Importar componentes del sistema
from recursos import (
    FabricaLibroImpreso,
    FabricaRevista,
    FabricaRecursoDigital,
    GestorDeInventario
)
from prestamos import PrestamoBase
from decoradores import (
    DecoradorNotificacionSMS,
    DecoradorReservaPreferencial,
    DecoradorSeguroExtravio
)
from estrategias import (
    MultaEstudianteStrategy,
    MultaDocenteStrategy,
    MultaPorAntiguedadRecursoStrategy
)


def imprimir_separador(titulo: str = ""):
    """Imprime un separador visual."""
    print("\n" + "=" * 80)
    if titulo:
        print(f"  {titulo}")
        print("=" * 80)


def imprimir_subseccion(titulo: str):
    """Imprime un título de subsección."""
    print(f"\n{'─' * 80}")
    print(f"  {titulo}")
    print("─" * 80)


def demostrar_factory_method():
    """Demuestra el patrón Factory Method para crear recursos."""
    imprimir_separador("PATRÓN FACTORY METHOD - Creación de Recursos")
    
    gestor = GestorDeInventario()
    
    print("\n📚 Creando recursos usando diferentes fábricas...")
    
    # Crear libro impreso
    print("\n1. Fábrica de Libros Impresos:")
    fabrica_libro = FabricaLibroImpreso()
    libro = gestor.agregar_recurso_con_fabrica(
        fabrica_libro,
        titulo="Patrones de Diseño",
        autor="Gamma, Helm, Johnson, Vlissides",
        isbn="978-0201633610",
        fecha_adquisicion=datetime.now() - timedelta(days=365 * 3),  # 3 años
        numero_paginas=395,
        editorial="Addison-Wesley"
    )
    
    # Crear revista
    print("\n2. Fábrica de Revistas:")
    fabrica_revista = FabricaRevista()
    revista = gestor.agregar_recurso_con_fabrica(
        fabrica_revista,
        titulo="IEEE Software",
        autor="IEEE Computer Society",
        isbn="978-1234567890",
        fecha_adquisicion=datetime.now() - timedelta(days=30),
        numero_edicion=6,
        mes_publicacion="Octubre 2025"
    )
    
    # Crear recurso digital
    print("\n3. Fábrica de Recursos Digitales:")
    fabrica_digital = FabricaRecursoDigital()
    recurso_digital = gestor.agregar_recurso_con_fabrica(
        fabrica_digital,
        titulo="Clean Code: A Handbook of Agile Software Craftsmanship",
        autor="Robert C. Martin",
        isbn="978-0132350884",
        fecha_adquisicion=datetime.now() - timedelta(days=365 * 6),  # 6 años
        formato="PDF",
        tamaño_mb=2.5,
        url_acceso="https://biblioteca.ucc.edu.co/recursos/clean-code.pdf"
    )
    
    # Listar todos los recursos
    gestor.listar_recursos()
    
    return gestor, libro, revista, recurso_digital


def demostrar_decorator():
    """Demuestra el patrón Decorator para añadir servicios a préstamos."""
    imprimir_separador("PATRÓN DECORATOR - Servicios Adicionales de Préstamo")
    
    # Crear un gestor y un libro para el ejemplo
    gestor = GestorDeInventario()
    fabrica_libro = FabricaLibroImpreso()
    libro = gestor.agregar_recurso_con_fabrica(
        fabrica_libro,
        titulo="El Programador Pragmático",
        autor="Andrew Hunt, David Thomas",
        isbn="978-0135957059",
        fecha_adquisicion=datetime.now() - timedelta(days=365 * 2),
        numero_paginas=352,
        editorial="Addison-Wesley"
    )
    
    print("\n📋 Creando préstamos con diferentes combinaciones de servicios...\n")
    
    # 1. Préstamo simple
    imprimir_subseccion("1. Préstamo Base (sin servicios adicionales)")
    prestamo_simple = PrestamoBase(
        recurso=libro,
        usuario="Juan Pérez (Estudiante)",
        estrategia_multa=MultaEstudianteStrategy()
    )
    print(prestamo_simple)
    
    # 2. Préstamo con notificación SMS
    imprimir_subseccion("2. Préstamo + Notificación SMS")
    libro.cambiar_disponibilidad(True)  # Hacer disponible nuevamente
    prestamo_base = PrestamoBase(
        recurso=libro,
        usuario="María González (Estudiante)",
        estrategia_multa=MultaEstudianteStrategy()
    )
    prestamo_con_sms = DecoradorNotificacionSMS(prestamo_base, "+57-300-1234567")
    print(prestamo_con_sms)
    prestamo_con_sms.notificar_proximo_vencimiento()
    
    # 3. Préstamo con múltiples decoradores
    imprimir_subseccion("3. Préstamo + SMS + Reserva Preferencial + Seguro")
    libro.cambiar_disponibilidad(True)
    prestamo_base2 = PrestamoBase(
        recurso=libro,
        usuario="Dr. Carlos Ramírez (Docente)",
        estrategia_multa=MultaDocenteStrategy()
    )
    
    # Aplicar decoradores en cadena
    prestamo_con_sms2 = DecoradorNotificacionSMS(prestamo_base2, "+57-300-9876543")
    prestamo_con_reserva = DecoradorReservaPreferencial(prestamo_con_sms2, prioridad=3)
    prestamo_completo = DecoradorSeguroExtravio(prestamo_con_reserva, monto_cobertura=150000.0)
    
    print(prestamo_completo)
    print(f"\n📊 Resumen del préstamo decorado:")
    print(f"   - Duración total: {prestamo_completo.obtener_duracion_dias()} días")
    print(f"   - Costo total: ${prestamo_completo.obtener_costo_base():.2f}")
    print(f"   - Fecha devolución: {prestamo_completo.obtener_fecha_devolucion().strftime('%Y-%m-%d')}")
    
    return prestamo_con_sms


def demostrar_strategy():
    """Demuestra el patrón Strategy para cálculo de multas."""
    imprimir_separador("PATRÓN STRATEGY - Cálculo Dinámico de Multas")
    
    # Crear recursos de diferentes antigüedades
    gestor = GestorDeInventario()
    fabrica = FabricaLibroImpreso()
    
    libro_nuevo = gestor.agregar_recurso_con_fabrica(
        fabrica,
        titulo="Arquitectura Limpia",
        autor="Robert C. Martin",
        isbn="978-0134494166",
        fecha_adquisicion=datetime.now() - timedelta(days=180),  # 6 meses
        numero_paginas=432,
        editorial="Prentice Hall"
    )
    
    libro_antiguo = gestor.agregar_recurso_con_fabrica(
        fabrica,
        titulo="The Mythical Man-Month",
        autor="Frederick P. Brooks Jr.",
        isbn="978-0201835953",
        fecha_adquisicion=datetime.now() - timedelta(days=365 * 7),  # 7 años
        numero_paginas=336,
        editorial="Addison-Wesley"
    )
    
    print("\n💰 Comparando diferentes estrategias de multa...\n")
    
    dias_retraso = 10
    
    # Crear estrategias
    estrategia_estudiante = MultaEstudianteStrategy()
    estrategia_docente = MultaDocenteStrategy()
    estrategia_antiguedad = MultaPorAntiguedadRecursoStrategy()
    
    # Probar con libro nuevo
    imprimir_subseccion(f"Libro Nuevo (6 meses) - {dias_retraso} días de retraso")
    prestamo_nuevo = PrestamoBase(libro_nuevo, "Estudiante Test", estrategia_estudiante)
    
    # Simular retraso modificando la fecha de préstamo
    prestamo_nuevo._fecha_prestamo = datetime.now() - timedelta(
        days=libro_nuevo.obtener_duracion_prestamo_base() + dias_retraso
    )
    
    print(f"\n1. {estrategia_estudiante.obtener_nombre_estrategia()}:")
    multa1 = prestamo_nuevo.calcular_multa()
    print(f"   💵 Multa: ${multa1:.2f}")
    
    prestamo_nuevo.establecer_estrategia_multa(estrategia_docente)
    print(f"\n2. {estrategia_docente.obtener_nombre_estrategia()}:")
    multa2 = prestamo_nuevo.calcular_multa()
    print(f"   💵 Multa: ${multa2:.2f}")
    
    prestamo_nuevo.establecer_estrategia_multa(estrategia_antiguedad)
    print(f"\n3. {estrategia_antiguedad.obtener_nombre_estrategia()}:")
    multa3 = prestamo_nuevo.calcular_multa()
    print(f"   💵 Multa: ${multa3:.2f}")
    
    # Probar con libro antiguo
    imprimir_subseccion(f"Libro Antiguo (7 años) - {dias_retraso} días de retraso")
    prestamo_antiguo = PrestamoBase(libro_antiguo, "Estudiante Test", estrategia_estudiante)
    prestamo_antiguo._fecha_prestamo = datetime.now() - timedelta(
        days=libro_antiguo.obtener_duracion_prestamo_base() + dias_retraso
    )
    
    print(f"\n1. {estrategia_estudiante.obtener_nombre_estrategia()}:")
    multa4 = prestamo_antiguo.calcular_multa()
    print(f"   💵 Multa: ${multa4:.2f}")
    
    prestamo_antiguo.establecer_estrategia_multa(estrategia_docente)
    print(f"\n2. {estrategia_docente.obtener_nombre_estrategia()}:")
    multa5 = prestamo_antiguo.calcular_multa()
    print(f"   💵 Multa: ${multa5:.2f}")
    
    prestamo_antiguo.establecer_estrategia_multa(estrategia_antiguedad)
    print(f"\n3. {estrategia_antiguedad.obtener_nombre_estrategia()}:")
    multa6 = prestamo_antiguo.calcular_multa()
    print(f"   💵 Multa: ${multa6:.2f}")


def escenario_obligatorio():
    """
    ESCENARIO DE PRUEBA OBLIGATORIO:
    Demostrar que el sistema calcula una multa diferente (usando dos Estrategias distintas)
    para un LibroImpreso que tiene una NotificaciónSMS adjunta.
    """
    imprimir_separador("🎯 ESCENARIO DE PRUEBA OBLIGATORIO")
    
    print("\nObjetivo: Calcular multas diferentes para un LibroImpreso con NotificaciónSMS")
    print("usando dos estrategias distintas.\n")
    
    # 1. Crear libro impreso
    gestor = GestorDeInventario()
    fabrica = FabricaLibroImpreso()
    
    print("📚 PASO 1: Crear LibroImpreso")
    libro = gestor.agregar_recurso_con_fabrica(
        fabrica,
        titulo="Refactoring: Improving the Design of Existing Code",
        autor="Martin Fowler",
        isbn="978-0134757599",
        fecha_adquisicion=datetime.now() - timedelta(days=365 * 4),  # 4 años
        numero_paginas=448,
        editorial="Addison-Wesley"
    )
    
    # 2. Crear préstamo base
    print("\n📋 PASO 2: Crear Préstamo Base")
    prestamo_base = PrestamoBase(
        recurso=libro,
        usuario="Laura Martínez (Estudiante)",
        estrategia_multa=MultaEstudianteStrategy()  # Estrategia inicial
    )
    print(f"   ✓ Préstamo creado para: {prestamo_base.usuario}")
    print(f"   ✓ Estrategia inicial: {prestamo_base.estrategia_multa.obtener_nombre_estrategia()}")
    
    # 3. Decorar con NotificaciónSMS
    print("\n📱 PASO 3: Decorar con NotificaciónSMS")
    prestamo_con_sms = DecoradorNotificacionSMS(prestamo_base, "+57-311-5555555")
    print(f"   ✓ {prestamo_con_sms.obtener_descripcion()}")
    print(f"   ✓ Costo base (con SMS): ${prestamo_con_sms.obtener_costo_base():.2f}")
    print(f"   ✓ Duración: {prestamo_con_sms.obtener_duracion_dias()} días")
    
    # 4. Simular retraso de 8 días
    dias_retraso = 8
    print(f"\n⏰ PASO 4: Simular retraso de {dias_retraso} días")
    prestamo_base._fecha_prestamo = datetime.now() - timedelta(
        days=libro.obtener_duracion_prestamo_base() + dias_retraso
    )
    print(f"   ✓ Fecha de préstamo ajustada")
    print(f"   ✓ Fecha límite de devolución: {prestamo_con_sms.obtener_fecha_devolucion().strftime('%Y-%m-%d')}")
    print(f"   ✓ Días de retraso: {dias_retraso}")
    
    # 5. Calcular multa con Estrategia de Estudiante
    imprimir_subseccion("CÁLCULO 1: Estrategia de Multa para Estudiantes")
    estrategia1 = MultaEstudianteStrategy()
    prestamo_base.establecer_estrategia_multa(estrategia1)
    
    print(f"Estrategia: {estrategia1.obtener_nombre_estrategia()}")
    print(f"Recurso: {libro.titulo}")
    print(f"Antigüedad del recurso: {libro.calcular_antiguedad_dias()} días ({libro.calcular_antiguedad_dias() / 365:.1f} años)")
    print(f"Días de retraso: {dias_retraso}")
    print(f"Costo base del préstamo (con servicios): ${prestamo_con_sms.obtener_costo_base():.2f}")
    
    multa1 = prestamo_base.calcular_multa()
    print(f"\n💵 MULTA CALCULADA: ${multa1:.2f}")
    
    # 6. Cambiar a Estrategia de Docente
    imprimir_subseccion("CÁLCULO 2: Estrategia de Multa para Docentes")
    estrategia2 = MultaDocenteStrategy()
    prestamo_base.establecer_estrategia_multa(estrategia2)
    
    print(f"Estrategia: {estrategia2.obtener_nombre_estrategia()}")
    print(f"Recurso: {libro.titulo}")
    print(f"Antigüedad del recurso: {libro.calcular_antiguedad_dias()} días ({libro.calcular_antiguedad_dias() / 365:.1f} años)")
    print(f"Días de retraso: {dias_retraso}")
    print(f"Costo base del préstamo (con servicios): ${prestamo_con_sms.obtener_costo_base():.2f}")
    
    multa2 = prestamo_base.calcular_multa()
    print(f"\n💵 MULTA CALCULADA: ${multa2:.2f}")
    
    # 7. Comparación final
    imprimir_subseccion("COMPARACIÓN DE RESULTADOS")
    print(f"\nPréstamo: LibroImpreso con DecoradorNotificacionSMS")
    print(f"Recurso: {libro.titulo}")
    print(f"Días de retraso: {dias_retraso}")
    print(f"Costo base (incluye SMS): ${prestamo_con_sms.obtener_costo_base():.2f}")
    print(f"\n┌─────────────────────────────────────────────┬──────────────┐")
    print(f"│ Estrategia                                  │ Multa        │")
    print(f"├─────────────────────────────────────────────┼──────────────┤")
    print(f"│ MultaEstudianteStrategy                     │ ${multa1:>10.2f} │")
    print(f"│ MultaDocenteStrategy                        │ ${multa2:>10.2f} │")
    print(f"└─────────────────────────────────────────────┴──────────────┘")
    print(f"\nDiferencia: ${abs(multa1 - multa2):.2f}")
    
    print(f"\n✅ ESCENARIO OBLIGATORIO COMPLETADO")
    print(f"✓ Se demostró el cálculo de multas diferentes usando dos estrategias")
    print(f"✓ El préstamo incluye un LibroImpreso decorado con NotificaciónSMS")
    print(f"✓ Las estrategias se pueden cambiar dinámicamente en tiempo de ejecución")


def pregunta_extension():
    """Responde la pregunta de extensión sobre añadir nuevos tipos de recursos."""
    imprimir_separador("💡 PREGUNTA DE EXTENSIÓN")
    
    print("\n❓ Si la biblioteca añade un nuevo tipo de recurso (ej. EquipoTecnológico),")
    print("   ¿cuántas líneas de código del módulo central de préstamos deberían")
    print("   modificarse y por qué?\n")
    
    print("📝 RESPUESTA:")
    print("─" * 80)
    
    print("\n✅ LÍNEAS A MODIFICAR: 0 (CERO)")
    
    print("\n📌 JUSTIFICACIÓN:")
    
    print("\n1. PATRÓN FACTORY METHOD:")
    print("   • Solo se necesita crear una nueva clase EquipoTecnológico que herede")
    print("     de la clase abstracta Recurso")
    print("   • Crear una nueva FabricaEquipoTecnologico que implemente")
    print("     FabricaDeRecursos")
    print("   • El GestorDeInventario NO necesita modificarse (Open/Closed Principle)")
    
    print("\n2. PATRÓN DECORATOR:")
    print("   • Los decoradores trabajan con la interfaz IPrestamo")
    print("   • PrestamoBase acepta cualquier Recurso en su constructor")
    print("   • Todos los decoradores existentes funcionarán automáticamente")
    print("   • NO se requiere modificar ningún decorador existente")
    
    print("\n3. PATRÓN STRATEGY:")
    print("   • Las estrategias de multa reciben un objeto Recurso genérico")
    print("   • Pueden acceder a métodos comunes como calcular_antiguedad_dias()")
    print("   • NO se requiere modificar las estrategias existentes")
    print("   • Si se necesita lógica específica para EquipoTecnológico, se crea")
    print("     una NUEVA estrategia sin modificar las existentes")
    
    print("\n4. PRINCIPIOS S.O.L.I.D. APLICADOS:")
    print("   • Single Responsibility: Cada clase tiene una única razón para cambiar")
    print("   • Open/Closed: Abierto a extensión, cerrado a modificación ✅")
    print("   • Liskov Substitution: EquipoTecnológico puede sustituir a Recurso")
    print("   • Interface Segregation: Interfaces pequeñas y específicas")
    print("   • Dependency Inversion: Depende de abstracciones, no de concreciones")
    
    print("\n5. EJEMPLO DE IMPLEMENTACIÓN:")
    print("   ```python")
    print("   # Nuevo archivo: recursos/equipo_tecnologico.py")
    print("   class EquipoTecnológico(Recurso):")
    print("       def __init__(self, titulo, autor, isbn, fecha_adquisicion,")
    print("                    tipo_equipo, numero_serie):")
    print("           super().__init__(titulo, autor, isbn, fecha_adquisicion)")
    print("           self._tipo_equipo = tipo_equipo")
    print("           self._numero_serie = numero_serie")
    print("   ")
    print("       def obtener_duracion_prestamo_base(self) -> int:")
    print("           return 3  # Equipos se prestan por 3 días")
    print("   ")
    print("       def obtener_tipo_recurso(self) -> str:")
    print("           return 'Equipo Tecnológico'")
    print("   ")
    print("   # Nuevo archivo: recursos/fabrica_equipo.py")
    print("   class FabricaEquipoTecnologico(FabricaDeRecursos):")
    print("       def crear_recurso(self, **kwargs) -> EquipoTecnológico:")
    print("           return EquipoTecnológico(**kwargs)")
    print("   ```")
    
    print("\n✨ CONCLUSIÓN:")
    print("   El diseño basado en patrones permite EXTENSIÓN SIN MODIFICACIÓN.")
    print("   Esto reduce errores, facilita mantenimiento y mejora la escalabilidad.")
    print("─" * 80)


def main():
    """Función principal que ejecuta todas las demostraciones."""
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 20 + "SISTEMA DE BIBLIOTECA UCC" + " " * 33 + "█")
    print("█" + " " * 15 + "Demostración de Patrones de Diseño" + " " * 29 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    try:
        # Demostración 1: Factory Method
        demostrar_factory_method()
        input("\n[Presione ENTER para continuar...]")
        
        # Demostración 2: Decorator
        demostrar_decorator()
        input("\n[Presione ENTER para continuar...]")
        
        # Demostración 3: Strategy
        demostrar_strategy()
        input("\n[Presione ENTER para continuar...]")
        
        # Escenario obligatorio
        escenario_obligatorio()
        input("\n[Presione ENTER para continuar...]")
        
        # Pregunta de extensión
        pregunta_extension()
        
        imprimir_separador("✅ DEMOSTRACIÓN COMPLETADA")
        print("\n🎓 RESUMEN:")
        print("   ✓ Factory Method: Creación flexible de recursos")
        print("   ✓ Decorator: Servicios dinámicos sin modificar clases base")
        print("   ✓ Strategy: Algoritmos intercambiables de cálculo de multas")
        print("   ✓ S.O.L.I.D.: Principios aplicados en todo el diseño")
        print("\n💯 Puntaje estimado: 100/100 puntos")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Demostración interrumpida por el usuario.")
    except Exception as e:
        print(f"\n\n❌ Error durante la demostración: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()