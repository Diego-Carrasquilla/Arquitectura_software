"""
Sistema Interactivo de Gestión de Biblioteca UCC
Interfaz de consola mejorada con menús ASCII
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from datetime import datetime, timedelta
from recursos import FabricaLibroImpreso, FabricaRevista, FabricaRecursoDigital, GestorDeInventario
from prestamos import PrestamoBase
from decoradores import DecoradorNotificacionSMS, DecoradorReservaPreferencial, DecoradorSeguroExtravio
from estrategias import (
    MultaEstudianteStrategy, 
    MultaDocenteStrategy, 
    MultaPorAntiguedadRecursoStrategy,
    MultaRecargadaStrategy
)
from facturacion import GestorFacturacion


class InterfazBiblioteca:
    """Interfaz de usuario para el sistema de biblioteca."""
    
    def __init__(self):
        self.gestor = GestorDeInventario()
        self.prestamos_activos = []
        self.gestor_facturacion = GestorFacturacion()
        
    def limpiar_pantalla(self):
        """Limpia la pantalla (compatible con Windows)."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_encabezado(self):
        """Muestra el encabezado del sistema."""
        print("\n" + "=" * 80)
        print("||" + " " * 76 + "||")
        print("||" + " " * 20 + "SISTEMA DE BIBLIOTECA UCC" + " " * 31 + "||")
        print("||" + " " * 15 + "Gestion de Recursos y Prestamos" + " " * 32 + "||")
        print("||" + " " * 76 + "||")
        print("=" * 80)
    
    def mostrar_linea_separadora(self, caracter="-"):
        """Muestra una línea separadora."""
        print(caracter * 80)
    
    def mostrar_submenu(self, titulo):
        """Muestra un encabezado de submenú."""
        print("\n" + "+" + "-" * 78 + "+")
        print("|" + " " * 78 + "|")
        print("|" + f"{titulo:^78}" + "|")
        print("|" + " " * 78 + "|")
        print("+" + "-" * 78 + "+")
    
    def pausa(self):
        """Pausa la ejecución esperando input del usuario."""
        input("\n>>> Presione ENTER para continuar...")
    
    def leer_opcion(self, mensaje, opciones_validas):
        """Lee una opción del usuario validando que sea válida."""
        while True:
            opcion = input(f"\n{mensaje}: ").strip()
            if opcion in opciones_validas:
                return opcion
            print(f"[ERROR] Opcion invalida. Ingrese una de las siguientes: {', '.join(opciones_validas)}")
    
    def leer_texto(self, mensaje, requerido=True):
        """Lee un texto del usuario."""
        while True:
            texto = input(f"{mensaje}: ").strip()
            if texto or not requerido:
                return texto
            print("[ERROR] Este campo es requerido.")
    
    def leer_numero(self, mensaje, tipo=int, minimo=None, maximo=None):
        """Lee un número del usuario con validación."""
        while True:
            try:
                valor = tipo(input(f"{mensaje}: ").strip())
                if minimo is not None and valor < minimo:
                    print(f"[ERROR] El valor debe ser mayor o igual a {minimo}")
                    continue
                if maximo is not None and valor > maximo:
                    print(f"[ERROR] El valor debe ser menor o igual a {maximo}")
                    continue
                return valor
            except ValueError:
                print(f"[ERROR] Debe ingresar un numero valido.")
    
    def leer_fecha(self, mensaje, fecha_default=None):
        """Lee una fecha del usuario o usa la fecha actual."""
        print(f"\n{mensaje}")
        usar_actual = self.leer_opcion("Usar fecha actual? (s/n)", ["s", "n"])
        
        if usar_actual == "s":
            return fecha_default or datetime.now()
        
        while True:
            try:
                fecha_str = input("Ingrese fecha (YYYY-MM-DD): ").strip()
                return datetime.strptime(fecha_str, "%Y-%m-%d")
            except ValueError:
                print("[ERROR] Formato de fecha invalido. Use YYYY-MM-DD")
    
    def menu_principal(self):
        """Muestra el menú principal."""
        while True:
            self.limpiar_pantalla()
            self.mostrar_encabezado()
            
            print("\n[MENU PRINCIPAL]")
            self.mostrar_linea_separadora()
            print("  1. Gestion de Recursos (Factory Method)")
            print("  2. Gestion de Prestamos (Decorator + Strategy)")
            print("  3. Facturacion y Pagos")
            print("  4. Consultas y Reportes")
            print("  5. Escenario de Prueba Obligatorio")
            print("  6. Demo Automatica")
            print("  0. Salir")
            self.mostrar_linea_separadora()
            
            opcion = self.leer_opcion("Seleccione una opcion", ["0", "1", "2", "3", "4", "5", "6"])
            
            if opcion == "0":
                self.salir()
                break
            elif opcion == "1":
                self.menu_recursos()
            elif opcion == "2":
                self.menu_prestamos()
            elif opcion == "3":
                self.menu_facturacion()
            elif opcion == "4":
                self.menu_consultas()
            elif opcion == "5":
                self.escenario_obligatorio()
            elif opcion == "6":
                self.demo_automatica()
    
    def menu_recursos(self):
        """Menú de gestión de recursos."""
        while True:
            self.limpiar_pantalla()
            self.mostrar_encabezado()
            self.mostrar_submenu("GESTION DE RECURSOS - PATRON FACTORY METHOD")
            
            print("\n[OPCIONES]")
            self.mostrar_linea_separadora()
            print("  1. Agregar Libro Impreso")
            print("  2. Agregar Revista")
            print("  3. Agregar Recurso Digital")
            print("  4. Listar Todos los Recursos")
            print("  0. Volver al Menu Principal")
            self.mostrar_linea_separadora()
            
            opcion = self.leer_opcion("Seleccione una opcion", ["0", "1", "2", "3", "4"])
            
            if opcion == "0":
                break
            elif opcion == "1":
                self.agregar_libro()
            elif opcion == "2":
                self.agregar_revista()
            elif opcion == "3":
                self.agregar_recurso_digital()
            elif opcion == "4":
                self.listar_recursos()
    
    def agregar_libro(self):
        """Agrega un libro impreso usando Factory Method."""
        self.mostrar_submenu("AGREGAR LIBRO IMPRESO")
        print("\nIngrese los datos del libro:")
        self.mostrar_linea_separadora()
        
        titulo = self.leer_texto("Titulo")
        autor = self.leer_texto("Autor")
        isbn = self.leer_texto("ISBN")
        numero_paginas = self.leer_numero("Numero de paginas", int, minimo=1)
        editorial = self.leer_texto("Editorial")
        fecha_adquisicion = self.leer_fecha("Fecha de adquisicion", datetime.now())
        
        fabrica = FabricaLibroImpreso()
        libro = self.gestor.agregar_recurso_con_fabrica(
            fabrica,
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            numero_paginas=numero_paginas,
            editorial=editorial,
            fecha_adquisicion=fecha_adquisicion
        )
        
        print(f"\n[OK] Libro agregado exitosamente!")
        print(f"     Tipo: {libro.obtener_tipo_recurso()}")
        print(f"     ISBN: {libro.isbn}")
        print(f"     Duracion prestamo base: {libro.obtener_duracion_prestamo_base()} dias")
        
        self.pausa()
    
    def agregar_revista(self):
        """Agrega una revista usando Factory Method."""
        self.mostrar_submenu("AGREGAR REVISTA")
        print("\nIngrese los datos de la revista:")
        self.mostrar_linea_separadora()
        
        titulo = self.leer_texto("Titulo")
        autor = self.leer_texto("Editor/Autor")
        isbn = self.leer_texto("ISBN")
        numero_edicion = self.leer_numero("Numero de edicion", int, minimo=1)
        mes_publicacion = self.leer_texto("Mes de publicacion")
        fecha_adquisicion = self.leer_fecha("Fecha de adquisicion", datetime.now())
        
        fabrica = FabricaRevista()
        revista = self.gestor.agregar_recurso_con_fabrica(
            fabrica,
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            numero_edicion=numero_edicion,
            mes_publicacion=mes_publicacion,
            fecha_adquisicion=fecha_adquisicion
        )
        
        print(f"\n[OK] Revista agregada exitosamente!")
        print(f"     Tipo: {revista.obtener_tipo_recurso()}")
        print(f"     ISBN: {revista.isbn}")
        print(f"     Duracion prestamo base: {revista.obtener_duracion_prestamo_base()} dias")
        
        self.pausa()
    
    def agregar_recurso_digital(self):
        """Agrega un recurso digital usando Factory Method."""
        self.mostrar_submenu("AGREGAR RECURSO DIGITAL")
        print("\nIngrese los datos del recurso digital:")
        self.mostrar_linea_separadora()
        
        titulo = self.leer_texto("Titulo")
        autor = self.leer_texto("Autor")
        isbn = self.leer_texto("ISBN")
        formato = self.leer_texto("Formato (PDF, EPUB, etc.)")
        tamaño_mb = self.leer_numero("Tamaño en MB", float, minimo=0.1)
        url_acceso = self.leer_texto("URL de acceso")
        fecha_adquisicion = self.leer_fecha("Fecha de adquisicion", datetime.now())
        
        fabrica = FabricaRecursoDigital()
        recurso = self.gestor.agregar_recurso_con_fabrica(
            fabrica,
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            formato=formato,
            tamaño_mb=tamaño_mb,
            url_acceso=url_acceso,
            fecha_adquisicion=fecha_adquisicion
        )
        
        print(f"\n[OK] Recurso digital agregado exitosamente!")
        print(f"     Tipo: {recurso.obtener_tipo_recurso()}")
        print(f"     ISBN: {recurso.isbn}")
        print(f"     Duracion prestamo base: {recurso.obtener_duracion_prestamo_base()} dias")
        
        self.pausa()
    
    def listar_recursos(self):
        """Lista todos los recursos en el inventario."""
        self.mostrar_submenu("INVENTARIO DE RECURSOS")
        
        if not self.gestor.recursos:
            print("\n[INFO] No hay recursos registrados en el sistema.")
            self.pausa()
            return
        
        print(f"\nTotal de recursos: {len(self.gestor.recursos)}")
        self.mostrar_linea_separadora()
        
        for i, recurso in enumerate(self.gestor.recursos, 1):
            disponibilidad = "DISPONIBLE" if recurso.disponible else "EN PRESTAMO"
            antiguedad = recurso.calcular_antiguedad_dias()
            
            print(f"\n[{i}] {recurso.obtener_tipo_recurso()}")
            print(f"    Titulo: {recurso.titulo}")
            print(f"    Autor: {recurso.autor}")
            print(f"    ISBN: {recurso.isbn}")
            print(f"    Estado: {disponibilidad}")
            print(f"    Antiguedad: {antiguedad} dias ({antiguedad/365:.1f} años)")
            print(f"    Duracion prestamo: {recurso.obtener_duracion_prestamo_base()} dias")
        
        self.mostrar_linea_separadora()
        self.pausa()
    
    def menu_prestamos(self):
        """Menú de gestión de préstamos."""
        while True:
            self.limpiar_pantalla()
            self.mostrar_encabezado()
            self.mostrar_submenu("GESTION DE PRESTAMOS - PATRONES DECORATOR Y STRATEGY")
            
            print("\n[OPCIONES]")
            self.mostrar_linea_separadora()
            print("  1. Crear Nuevo Prestamo")
            print("  2. Calcular Multa de Prestamo")
            print("  3. Listar Prestamos Activos")
            print("  4. Devolver Recurso")
            print("  0. Volver al Menu Principal")
            self.mostrar_linea_separadora()
            
            opcion = self.leer_opcion("Seleccione una opcion", ["0", "1", "2", "3", "4"])
            
            if opcion == "0":
                break
            elif opcion == "1":
                self.crear_prestamo()
            elif opcion == "2":
                self.calcular_multa()
            elif opcion == "3":
                self.listar_prestamos()
            elif opcion == "4":
                self.devolver_recurso()
    
    def crear_prestamo(self):
        """Crea un nuevo préstamo con decoradores y estrategia."""
        self.mostrar_submenu("CREAR NUEVO PRESTAMO")
        
        if not self.gestor.recursos:
            print("\n[ERROR] No hay recursos registrados. Primero agregue recursos.")
            self.pausa()
            return
        
        # Mostrar recursos disponibles
        recursos_disponibles = [r for r in self.gestor.recursos if r.disponible]
        if not recursos_disponibles:
            print("\n[ERROR] No hay recursos disponibles. Todos estan prestados.")
            self.pausa()
            return
        
        print("\n[RECURSOS DISPONIBLES]")
        self.mostrar_linea_separadora()
        for i, recurso in enumerate(recursos_disponibles, 1):
            print(f"  [{i}] {recurso.titulo} - {recurso.obtener_tipo_recurso()}")
        self.mostrar_linea_separadora()
        
        idx = self.leer_numero("Seleccione el numero del recurso", int, minimo=1, 
                              maximo=len(recursos_disponibles)) - 1
        recurso_seleccionado = recursos_disponibles[idx]
        
        # Datos del usuario
        print("\n[DATOS DEL USUARIO]")
        self.mostrar_linea_separadora()
        nombre_usuario = self.leer_texto("Nombre completo")
        
        # Seleccionar estrategia de multa
        print("\n[ESTRATEGIA DE MULTA]")
        self.mostrar_linea_separadora()
        print("  1. Multa para Estudiantes ($2.00/dia, descuento por antiguedad)")
        print("  2. Multa para Docentes ($1.00/dia, 3 dias de gracia)")
        print("  3. Multa por Antiguedad del Recurso (varia segun edad)")
        print("  4. Multa Recargada Progresiva")
        self.mostrar_linea_separadora()
        
        estrategia_opcion = self.leer_opcion("Seleccione estrategia", ["1", "2", "3", "4"])
        estrategias = {
            "1": MultaEstudianteStrategy(),
            "2": MultaDocenteStrategy(),
            "3": MultaPorAntiguedadRecursoStrategy(),
            "4": MultaRecargadaStrategy()
        }
        estrategia = estrategias[estrategia_opcion]
        
        # Crear préstamo base
        prestamo = PrestamoBase(recurso_seleccionado, nombre_usuario, estrategia)
        
        # Agregar servicios (decoradores)
        print("\n[SERVICIOS ADICIONALES (DECORADORES)]")
        self.mostrar_linea_separadora()
        
        agregar_sms = self.leer_opcion("Agregar Notificacion SMS (+$5.00)? (s/n)", ["s", "n"])
        if agregar_sms == "s":
            telefono = self.leer_texto("Numero de telefono")
            prestamo = DecoradorNotificacionSMS(prestamo, telefono)
        
        agregar_reserva = self.leer_opcion("Agregar Reserva Preferencial (+$10.00, +7 dias)? (s/n)", ["s", "n"])
        if agregar_reserva == "s":
            prioridad = self.leer_numero("Nivel de prioridad (1-5)", int, minimo=1, maximo=5)
            prestamo = DecoradorReservaPreferencial(prestamo, prioridad)
        
        agregar_seguro = self.leer_opcion("Agregar Seguro contra Extravio (+$15.00)? (s/n)", ["s", "n"])
        if agregar_seguro == "s":
            cobertura = self.leer_numero("Monto de cobertura", float, minimo=1000)
            prestamo = DecoradorSeguroExtravio(prestamo, cobertura)
        
        # Guardar préstamo
        self.prestamos_activos.append(prestamo)
        
        # Obtener el préstamo base para acceder a fecha_prestamo
        prestamo_base = prestamo
        while hasattr(prestamo_base, 'prestamo_envuelto'):
            prestamo_base = prestamo_base.prestamo_envuelto
        
        # Mostrar resumen
        print("\n[RESUMEN DEL PRESTAMO]")
        self.mostrar_linea_separadora()
        print(f"Recurso: {recurso_seleccionado.titulo}")
        print(f"Usuario: {nombre_usuario}")
        print(f"Estrategia: {estrategia.obtener_nombre_estrategia()}")
        print(f"Duracion: {prestamo.obtener_duracion_dias()} dias")
        print(f"Costo total: ${prestamo.obtener_costo_base():.2f}")
        print(f"Fecha prestamo: {prestamo_base.fecha_prestamo.strftime('%Y-%m-%d %H:%M')}")
        print(f"Fecha devolucion: {prestamo.obtener_fecha_devolucion().strftime('%Y-%m-%d')}")
        self.mostrar_linea_separadora()
        
        print("\n[OK] Prestamo creado exitosamente!")
        self.pausa()
    
    def listar_prestamos(self):
        """Lista todos los préstamos activos."""
        self.mostrar_submenu("PRESTAMOS ACTIVOS")
        
        if not self.prestamos_activos:
            print("\n[INFO] No hay prestamos activos en el sistema.")
            self.pausa()
            return
        
        print(f"\nTotal de prestamos: {len(self.prestamos_activos)}")
        self.mostrar_linea_separadora()
        
        for i, prestamo in enumerate(self.prestamos_activos, 1):
            prestamo_base = prestamo
            while hasattr(prestamo_base, 'prestamo_envuelto'):
                prestamo_base = prestamo_base.prestamo_envuelto
            
            dias_restantes = (prestamo.obtener_fecha_devolucion() - datetime.now()).days
            estado = "A TIEMPO" if dias_restantes >= 0 else f"VENCIDO ({abs(dias_restantes)} dias)"
            
            print(f"\n[{i}] {prestamo.obtener_descripcion()}")
            print(f"    Duracion: {prestamo.obtener_duracion_dias()} dias")
            print(f"    Costo: ${prestamo.obtener_costo_base():.2f}")
            print(f"    Fecha devolucion: {prestamo.obtener_fecha_devolucion().strftime('%Y-%m-%d')}")
            print(f"    Estado: {estado}")
        
        self.mostrar_linea_separadora()
        self.pausa()
    
    def calcular_multa(self):
        """Calcula la multa de un préstamo."""
        self.mostrar_submenu("CALCULAR MULTA")
        
        if not self.prestamos_activos:
            print("\n[INFO] No hay prestamos activos.")
            self.pausa()
            return
        
        print("\n[PRESTAMOS ACTIVOS]")
        self.mostrar_linea_separadora()
        for i, prestamo in enumerate(self.prestamos_activos, 1):
            prestamo_base = prestamo
            while hasattr(prestamo_base, 'prestamo_envuelto'):
                prestamo_base = prestamo_base.prestamo_envuelto
            print(f"  [{i}] {prestamo_base.recurso.titulo} - {prestamo_base.usuario}")
        self.mostrar_linea_separadora()
        
        idx = self.leer_numero("Seleccione el numero del prestamo", int, minimo=1, 
                              maximo=len(self.prestamos_activos)) - 1
        prestamo = self.prestamos_activos[idx]
        
        # Obtener préstamo base para acceder a métodos
        prestamo_base = prestamo
        while hasattr(prestamo_base, 'prestamo_envuelto'):
            prestamo_base = prestamo_base.prestamo_envuelto
        
        # Simular retraso si es necesario
        print("\n[OPCIONES]")
        print("  1. Calcular con fechas actuales")
        print("  2. Simular dias de retraso")
        opcion = self.leer_opcion("Seleccione opcion", ["1", "2"])
        
        if opcion == "2":
            dias_retraso = self.leer_numero("Ingrese dias de retraso a simular", int, minimo=1)
            prestamo_base._fecha_prestamo = datetime.now() - timedelta(
                days=prestamo_base.recurso.obtener_duracion_prestamo_base() + dias_retraso
            )
        
        # Calcular multa
        print("\n[CALCULO DE MULTA]")
        self.mostrar_linea_separadora()
        print(f"Recurso: {prestamo_base.recurso.titulo}")
        print(f"Estrategia: {prestamo_base.estrategia_multa.obtener_nombre_estrategia()}")
        print(f"Fecha devolucion: {prestamo.obtener_fecha_devolucion().strftime('%Y-%m-%d')}")
        print(f"Dias de retraso: {prestamo_base.calcular_dias_retraso()}")
        
        try:
            multa = prestamo_base.calcular_multa()
            print(f"\n>>> MULTA CALCULADA: ${multa:.2f}")
        except Exception as e:
            print(f"\n[ERROR] {str(e)}")
        
        self.mostrar_linea_separadora()
        self.pausa()
    
    def devolver_recurso(self):
        """Devuelve un recurso prestado."""
        self.mostrar_submenu("DEVOLVER RECURSO")
        
        if not self.prestamos_activos:
            print("\n[INFO] No hay prestamos activos.")
            self.pausa()
            return
        
        print("\n[PRESTAMOS ACTIVOS]")
        self.mostrar_linea_separadora()
        for i, prestamo in enumerate(self.prestamos_activos, 1):
            prestamo_base = prestamo
            while hasattr(prestamo_base, 'prestamo_envuelto'):
                prestamo_base = prestamo_base.prestamo_envuelto
            print(f"  [{i}] {prestamo_base.recurso.titulo} - {prestamo_base.usuario}")
        self.mostrar_linea_separadora()
        
        idx = self.leer_numero("Seleccione el numero del prestamo", int, minimo=1, 
                              maximo=len(self.prestamos_activos)) - 1
        prestamo = self.prestamos_activos[idx]
        
        prestamo_base = prestamo
        while hasattr(prestamo_base, 'prestamo_envuelto'):
            prestamo_base = prestamo_base.prestamo_envuelto
        
        # Calcular multa si hay retraso
        multa = 0
        if prestamo_base.calcular_dias_retraso() > 0:
            multa = prestamo_base.calcular_multa()
        
        prestamo_base.devolver_recurso()
        self.prestamos_activos.pop(idx)
        
        print(f"\n[OK] Recurso devuelto exitosamente!")
        if multa > 0:
            print(f"[AVISO] Multa aplicada: ${multa:.2f}")
        
        self.pausa()
    
    def menu_facturacion(self):
        """Menú de facturación y pagos."""
        while True:
            self.limpiar_pantalla()
            self.mostrar_encabezado()
            self.mostrar_submenu("FACTURACION Y PAGOS")
            
            print("\n[OPCIONES]")
            self.mostrar_linea_separadora()
            print("  1. Generar Factura de Prestamo")
            print("  2. Simular Pago de Factura")
            print("  3. Ver Historial de Facturas")
            print("  4. Reporte de Facturacion")
            print("  0. Volver al Menu Principal")
            self.mostrar_linea_separadora()
            
            opcion = self.leer_opcion("Seleccione una opcion", ["0", "1", "2", "3", "4"])
            
            if opcion == "0":
                break
            elif opcion == "1":
                self.generar_factura()
            elif opcion == "2":
                self.simular_pago()
            elif opcion == "3":
                self.ver_historial_facturas()
            elif opcion == "4":
                self.reporte_facturacion()
    
    def generar_factura(self):
        """Genera una factura para un préstamo."""
        self.mostrar_submenu("GENERAR FACTURA")
        
        if not self.prestamos_activos:
            print("\n[INFO] No hay prestamos activos.")
            self.pausa()
            return
        
        print("\n[PRESTAMOS ACTIVOS]")
        self.mostrar_linea_separadora()
        for i, prestamo in enumerate(self.prestamos_activos, 1):
            prestamo_base = prestamo
            while hasattr(prestamo_base, 'prestamo_envuelto'):
                prestamo_base = prestamo_base.prestamo_envuelto
            
            dias_restantes = (prestamo.obtener_fecha_devolucion() - datetime.now()).days
            estado = "A TIEMPO" if dias_restantes >= 0 else f"VENCIDO ({abs(dias_restantes)} dias)"
            
            print(f"  [{i}] {prestamo_base.recurso.titulo} - {prestamo_base.usuario} - {estado}")
        self.mostrar_linea_separadora()
        
        idx = self.leer_numero("Seleccione el numero del prestamo", int, minimo=1, 
                              maximo=len(self.prestamos_activos)) - 1
        prestamo = self.prestamos_activos[idx]
        
        # Obtener préstamo base
        prestamo_base = prestamo
        while hasattr(prestamo_base, 'prestamo_envuelto'):
            prestamo_base = prestamo_base.prestamo_envuelto
        
        # Opciones de factura
        print("\n[OPCIONES DE FACTURA]")
        print("  1. Factura solo por servicios contratados")
        print("  2. Factura incluyendo multas (si aplica)")
        opcion = self.leer_opcion("Seleccione tipo de factura", ["1", "2"])
        
        incluir_multa = (opcion == "2")
        
        # Simular retraso si se desea
        if incluir_multa:
            simular = self.leer_opcion("Desea simular dias de retraso? (s/n)", ["s", "n"])
            if simular == "s":
                dias_retraso = self.leer_numero("Ingrese dias de retraso", int, minimo=1)
                prestamo_base._fecha_prestamo = datetime.now() - timedelta(
                    days=prestamo_base.recurso.obtener_duracion_prestamo_base() + dias_retraso
                )
                print(f"[INFO] Simulados {dias_retraso} dias de retraso")
        
        # Generar factura
        factura = self.gestor_facturacion.crear_factura(prestamo, prestamo_base, incluir_multa)
        
        # Mostrar factura
        self.limpiar_pantalla()
        print(factura.generar_factura_texto(incluir_multa=False))  # Ya se agregó multa en crear_factura
        
        self.pausa()
    
    def simular_pago(self):
        """Simula el proceso de pago de una factura."""
        self.mostrar_submenu("SIMULACION DE PAGO")
        
        if not self.gestor_facturacion.facturas_generadas:
            print("\n[INFO] No hay facturas generadas. Primero genere una factura.")
            self.pausa()
            return
        
        print("\n[FACTURAS PENDIENTES DE PAGO]")
        self.mostrar_linea_separadora()
        for i, factura in enumerate(self.gestor_facturacion.facturas_generadas, 1):
            total = factura.calcular_total()
            print(f"  [{i}] {factura.numero_factura} - Cliente: {factura.prestamo_base.usuario} - Total: ${total:.2f}")
        self.mostrar_linea_separadora()
        
        idx = self.leer_numero("Seleccione el numero de factura", int, minimo=1, 
                              maximo=len(self.gestor_facturacion.facturas_generadas)) - 1
        factura = self.gestor_facturacion.facturas_generadas[idx]
        
        total = factura.calcular_total()
        
        print("\n[DETALLE DEL PAGO]")
        self.mostrar_linea_separadora()
        print(f"Numero de Factura: {factura.numero_factura}")
        print(f"Cliente:           {factura.prestamo_base.usuario}")
        print(f"Total a Pagar:     ${total:.2f}")
        self.mostrar_linea_separadora()
        
        print("\n[METODOS DE PAGO]")
        print("  1. Efectivo")
        print("  2. Tarjeta de Credito/Debito")
        print("  3. Transferencia Bancaria")
        print("  4. PSE - Pagos Seguros en Linea")
        
        metodo = self.leer_opcion("Seleccione metodo de pago", ["1", "2", "3", "4"])
        metodos = {
            "1": "Efectivo",
            "2": "Tarjeta de Credito/Debito",
            "3": "Transferencia Bancaria",
            "4": "PSE - Pagos Seguros en Linea"
        }
        
        print(f"\n[PROCESANDO PAGO...]")
        self.mostrar_linea_separadora()
        print(f"Metodo:            {metodos[metodo]}")
        print(f"Monto:             ${total:.2f}")
        
        if metodo == "1":
            monto_recibido = self.leer_numero("Monto recibido", float, minimo=total)
            cambio = monto_recibido - total
            print(f"Cambio a devolver: ${cambio:.2f}")
        elif metodo == "2":
            numero_tarjeta = self.leer_texto("Ultimos 4 digitos de la tarjeta")
            print(f"Tarjeta:           **** **** **** {numero_tarjeta}")
            print(f"Estado:            APROBADO")
        elif metodo == "3":
            print(f"Banco:             Banco de Colombia")
            print(f"Cuenta:            123-456789-01")
            print(f"Referencia:        {factura.numero_factura}")
            print(f"Estado:            PENDIENTE DE CONFIRMACION")
        elif metodo == "4":
            print(f"Entidad:           PSE Colombia")
            print(f"Estado:            APROBADO")
        
        print("\n" + "=" * 80)
        print("||" + " " * 76 + "||")
        print("||" + " " * 28 + "PAGO EXITOSO" + " " * 36 + "||")
        print("||" + " " * 76 + "||")
        print("=" * 80)
        print(f"\nFecha:             {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Numero Recibo:     REC-{factura.numero_factura}")
        print(f"Total Pagado:      ${total:.2f}")
        print(f"Metodo:            {metodos[metodo]}")
        print("\n[OK] Transaccion completada exitosamente")
        print("     Conserve este recibo como comprobante de pago")
        self.mostrar_linea_separadora()
        
        self.pausa()
    
    def ver_historial_facturas(self):
        """Muestra el historial de facturas generadas."""
        self.mostrar_submenu("HISTORIAL DE FACTURAS")
        
        if not self.gestor_facturacion.facturas_generadas:
            print("\n[INFO] No hay facturas en el historial.")
            self.pausa()
            return
        
        print(f"\nTotal de facturas generadas: {len(self.gestor_facturacion.facturas_generadas)}")
        self.mostrar_linea_separadora()
        
        print("\n+--------+------------------+-------------------------+----------+")
        print("| Numero | Fecha            | Cliente                 | Total    |")
        print("+--------+------------------+-------------------------+----------+")
        
        for factura in self.gestor_facturacion.facturas_generadas:
            numero = factura.numero_factura[-8:]
            fecha = factura.fecha_emision.strftime('%Y-%m-%d %H:%M')
            cliente = factura.prestamo_base.usuario[:25].ljust(25)
            total = factura.calcular_total()
            print(f"| {numero} | {fecha} | {cliente} | ${total:>7.2f} |")
        
        print("+--------+------------------+-------------------------+----------+")
        
        total_facturado = self.gestor_facturacion.obtener_total_facturado()
        print(f"\nTotal Facturado: ${total_facturado:.2f}")
        self.mostrar_linea_separadora()
        
        # Opción de ver detalle
        ver_detalle = self.leer_opcion("\nVer detalle de alguna factura? (s/n)", ["s", "n"])
        if ver_detalle == "s":
            idx = self.leer_numero("Ingrese el numero de factura (1-N)", int, minimo=1,
                                  maximo=len(self.gestor_facturacion.facturas_generadas)) - 1
            factura = self.gestor_facturacion.facturas_generadas[idx]
            self.limpiar_pantalla()
            print(factura.generar_factura_texto(incluir_multa=False))
        
        self.pausa()
    
    def reporte_facturacion(self):
        """Genera un reporte de facturación."""
        self.mostrar_submenu("REPORTE DE FACTURACION")
        
        if not self.gestor_facturacion.facturas_generadas:
            print("\n[INFO] No hay datos de facturacion.")
            self.pausa()
            return
        
        total_facturas = len(self.gestor_facturacion.facturas_generadas)
        total_facturado = self.gestor_facturacion.obtener_total_facturado()
        
        # Calcular estadísticas
        total_servicios = 0
        total_multas = 0
        
        for factura in self.gestor_facturacion.facturas_generadas:
            for item in factura.items:
                if item.tipo == "MULTA":
                    total_multas += item.subtotal
                else:
                    total_servicios += item.subtotal
        
        promedio_factura = total_facturado / total_facturas if total_facturas > 0 else 0
        
        print("\n[RESUMEN FINANCIERO]")
        self.mostrar_linea_separadora()
        print(f"Total de Facturas:        {total_facturas}")
        print(f"Total Facturado:          ${total_facturado:.2f}")
        print(f"Promedio por Factura:     ${promedio_factura:.2f}")
        print(f"Total por Servicios:      ${total_servicios:.2f}")
        print(f"Total por Multas:         ${total_multas:.2f}")
        self.mostrar_linea_separadora()
        
        # Gráfico ASCII simple
        if total_facturado > 0:
            print("\n[DISTRIBUCION DE INGRESOS]")
            porcentaje_servicios = (total_servicios / total_facturado) * 100
            porcentaje_multas = (total_multas / total_facturado) * 100
            
            barras_servicios = int(porcentaje_servicios / 2)
            barras_multas = int(porcentaje_multas / 2)
            
            print(f"Servicios: {'#' * barras_servicios} {porcentaje_servicios:.1f}%")
            print(f"Multas:    {'#' * barras_multas} {porcentaje_multas:.1f}%")
        
        self.mostrar_linea_separadora()
        self.pausa()
    
    def menu_consultas(self):
        """Menú de consultas y reportes."""
        self.mostrar_submenu("CONSULTAS Y REPORTES")
        
        print("\n[ESTADISTICAS]")
        self.mostrar_linea_separadora()
        print(f"Total recursos registrados: {len(self.gestor.recursos)}")
        recursos_disponibles = len([r for r in self.gestor.recursos if r.disponible])
        print(f"Recursos disponibles: {recursos_disponibles}")
        print(f"Recursos en prestamo: {len(self.gestor.recursos) - recursos_disponibles}")
        print(f"Prestamos activos: {len(self.prestamos_activos)}")
        self.mostrar_linea_separadora()
        
        self.pausa()
    
    def escenario_obligatorio(self):
        """Ejecuta el escenario de prueba obligatorio."""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        self.mostrar_submenu("ESCENARIO DE PRUEBA OBLIGATORIO")
        
        print("\n[DESCRIPCION]")
        print("Demostrar que el sistema calcula una multa diferente usando dos")
        print("Estrategias distintas para un LibroImpreso con NotificacionSMS adjunta.")
        self.mostrar_linea_separadora()
        
        # 1. Crear libro
        print("\n[PASO 1] Creando LibroImpreso...")
        fabrica = FabricaLibroImpreso()
        libro = self.gestor.agregar_recurso_con_fabrica(
            fabrica,
            titulo="Refactoring: Improving the Design of Existing Code",
            autor="Martin Fowler",
            isbn="978-0134757599",
            fecha_adquisicion=datetime.now() - timedelta(days=365 * 4),
            numero_paginas=448,
            editorial="Addison-Wesley"
        )
        print(f"    Creado: {libro.titulo}")
        print(f"    Antiguedad: {libro.calcular_antiguedad_dias()} dias")
        
        # 2. Crear préstamo base
        print("\n[PASO 2] Creando Prestamo Base...")
        prestamo_base = PrestamoBase(
            recurso=libro,
            usuario="Laura Martinez (Estudiante)",
            estrategia_multa=MultaEstudianteStrategy()
        )
        print(f"    Usuario: {prestamo_base.usuario}")
        print(f"    Estrategia: {prestamo_base.estrategia_multa.obtener_nombre_estrategia()}")
        
        # 3. Decorar con SMS
        print("\n[PASO 3] Decorando con NotificacionSMS...")
        prestamo_sms = DecoradorNotificacionSMS(prestamo_base, "+57-311-5555555")
        print(f"    Telefono: +57-311-5555555")
        print(f"    Costo base (sin SMS): ${prestamo_base.obtener_costo_base():.2f}")
        print(f"    Costo total (con SMS): ${prestamo_sms.obtener_costo_base():.2f}")
        
        # 4. Simular retraso
        dias_retraso = 8
        print(f"\n[PASO 4] Simulando retraso de {dias_retraso} dias...")
        prestamo_base._fecha_prestamo = datetime.now() - timedelta(
            days=libro.obtener_duracion_prestamo_base() + dias_retraso
        )
        print(f"    Fecha devolucion: {prestamo_sms.obtener_fecha_devolucion().strftime('%Y-%m-%d')}")
        print(f"    Dias de retraso: {prestamo_base.calcular_dias_retraso()}")
        
        # 5. Calcular con estrategia 1
        print("\n[PASO 5] Calculando multa con MultaEstudianteStrategy...")
        self.mostrar_linea_separadora("-")
        estrategia1 = MultaEstudianteStrategy()
        prestamo_base.establecer_estrategia_multa(estrategia1)
        multa1 = prestamo_base.calcular_multa()
        print(f"    MULTA: ${multa1:.2f}")
        
        # 6. Calcular con estrategia 2
        print("\n[PASO 6] Calculando multa con MultaDocenteStrategy...")
        self.mostrar_linea_separadora("-")
        estrategia2 = MultaDocenteStrategy()
        prestamo_base.establecer_estrategia_multa(estrategia2)
        multa2 = prestamo_base.calcular_multa()
        print(f"    MULTA: ${multa2:.2f}")
        
        # 7. Comparación
        print("\n[COMPARACION DE RESULTADOS]")
        self.mostrar_linea_separadora("=")
        print(f"Prestamo: LibroImpreso + DecoradorNotificacionSMS")
        print(f"Recurso: {libro.titulo}")
        print(f"Dias de retraso: {dias_retraso}")
        print(f"Costo base (incluye SMS): ${prestamo_sms.obtener_costo_base():.2f}")
        print()
        print("+-----------------------------------------------+--------------+")
        print("| Estrategia                                    | Multa        |")
        print("+-----------------------------------------------+--------------+")
        print(f"| MultaEstudianteStrategy                       | ${multa1:>10.2f} |")
        print(f"| MultaDocenteStrategy                          | ${multa2:>10.2f} |")
        print("+-----------------------------------------------+--------------+")
        print(f"Diferencia: ${abs(multa1 - multa2):.2f}")
        print()
        print("[OK] ESCENARIO OBLIGATORIO COMPLETADO")
        print("     Se demostro el calculo de multas diferentes usando dos estrategias")
        print("     El prestamo incluye LibroImpreso decorado con NotificacionSMS")
        self.mostrar_linea_separadora("=")
        
        self.pausa()
    
    def demo_automatica(self):
        """Ejecuta una demostración automática del sistema."""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        self.mostrar_submenu("DEMOSTRACION AUTOMATICA DEL SISTEMA")
        
        print("\n[DEMOSTRACION] Factory Method - Decorator - Strategy")
        self.mostrar_linea_separadora()
        
        print("\nCreando recursos de ejemplo...")
        # Crear algunos recursos
        fabrica_libro = FabricaLibroImpreso()
        libro = self.gestor.agregar_recurso_con_fabrica(
            fabrica_libro,
            titulo="Clean Code",
            autor="Robert C. Martin",
            isbn="978-0132350884",
            fecha_adquisicion=datetime.now() - timedelta(days=365 * 3),
            numero_paginas=464,
            editorial="Prentice Hall"
        )
        
        print("\nCreando prestamo con decoradores...")
        prestamo = PrestamoBase(libro, "Juan Perez", MultaEstudianteStrategy())
        prestamo = DecoradorNotificacionSMS(prestamo, "+57-300-1234567")
        prestamo = DecoradorReservaPreferencial(prestamo, prioridad=2)
        
        print(f"\nDescripcion: {prestamo.obtener_descripcion()}")
        print(f"Duracion: {prestamo.obtener_duracion_dias()} dias")
        print(f"Costo: ${prestamo.obtener_costo_base():.2f}")
        
        print("\n[OK] Demostracion completada!")
        self.mostrar_linea_separadora()
        
        self.pausa()
    
    def salir(self):
        """Sale del sistema."""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        print("\n")
        print("  Gracias por usar el Sistema de Biblioteca UCC")
        print("  Desarrollo: Arquitectura de Software - UCC")
        print("\n")
        self.mostrar_linea_separadora("=")


def main():
    """Función principal."""
    interfaz = InterfazBiblioteca()
    interfaz.menu_principal()


if __name__ == "__main__":
    main()