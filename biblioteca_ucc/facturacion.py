"""
Módulo de facturación para préstamos de la biblioteca.
Genera facturas detalladas con servicios y multas aplicadas.
"""
from datetime import datetime
from typing import List, Tuple


class ItemFactura:
    """Representa un item individual en la factura."""
    
    def __init__(self, descripcion: str, cantidad: int, valor_unitario: float, 
                 tipo: str = "SERVICIO"):
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.valor_unitario = valor_unitario
        self.tipo = tipo  # SERVICIO, MULTA, RECURSO
    
    @property
    def subtotal(self) -> float:
        """Calcula el subtotal del item."""
        return self.cantidad * self.valor_unitario


class Factura:
    """Genera y muestra facturas de préstamos."""
    
    def __init__(self, numero_factura: str, prestamo, prestamo_base):
        self.numero_factura = numero_factura
        self.prestamo = prestamo
        self.prestamo_base = prestamo_base
        self.items = []
        self.fecha_emision = datetime.now()
        self._generar_items()
    
    def _generar_items(self):
        """Genera los items de la factura basándose en el préstamo."""
        # Item 1: Costo base del préstamo (siempre $0 en este sistema)
        if self.prestamo_base.obtener_costo_base() > 0:
            self.items.append(ItemFactura(
                "Prestamo Base del Recurso",
                1,
                self.prestamo_base.obtener_costo_base(),
                "RECURSO"
            ))
        
        # Identificar decoradores aplicados
        prestamo_actual = self.prestamo
        while hasattr(prestamo_actual, 'prestamo_envuelto'):
            if hasattr(prestamo_actual, 'COSTO_SERVICIO_SMS'):
                self.items.append(ItemFactura(
                    f"Servicio de Notificacion SMS a {prestamo_actual.numero_telefono}",
                    1,
                    prestamo_actual.COSTO_SERVICIO_SMS,
                    "SERVICIO"
                ))
            elif hasattr(prestamo_actual, 'COSTO_RESERVA_PREFERENCIAL'):
                self.items.append(ItemFactura(
                    f"Reserva Preferencial (Prioridad {prestamo_actual.prioridad})",
                    1,
                    prestamo_actual.COSTO_RESERVA_PREFERENCIAL,
                    "SERVICIO"
                ))
            elif hasattr(prestamo_actual, 'COSTO_SEGURO'):
                self.items.append(ItemFactura(
                    f"Seguro contra Extravio (Cobertura ${prestamo_actual.monto_cobertura:.2f})",
                    1,
                    prestamo_actual.COSTO_SEGURO,
                    "SERVICIO"
                ))
            prestamo_actual = prestamo_actual.prestamo_envuelto
    
    def agregar_multa(self):
        """Agrega la multa a la factura si existe."""
        dias_retraso = self.prestamo_base.calcular_dias_retraso()
        if dias_retraso > 0:
            multa = self.prestamo_base.calcular_multa()
            estrategia = self.prestamo_base.estrategia_multa.obtener_nombre_estrategia()
            self.items.append(ItemFactura(
                f"Multa por {dias_retraso} dias de retraso ({estrategia})",
                1,
                multa,
                "MULTA"
            ))
            return multa
        return 0.0
    
    def calcular_subtotal(self) -> float:
        """Calcula el subtotal de la factura."""
        return sum(item.subtotal for item in self.items)
    
    def calcular_iva(self, porcentaje: float = 0.0) -> float:
        """Calcula el IVA (por defecto 0% para servicios educativos)."""
        return self.calcular_subtotal() * porcentaje
    
    def calcular_total(self, porcentaje_iva: float = 0.0) -> float:
        """Calcula el total de la factura."""
        return self.calcular_subtotal() + self.calcular_iva(porcentaje_iva)
    
    def generar_factura_texto(self, incluir_multa: bool = True) -> str:
        """Genera la factura en formato texto ASCII."""
        if incluir_multa:
            self.agregar_multa()
        
        lineas = []
        lineas.append("=" * 80)
        lineas.append("||" + " " * 76 + "||")
        lineas.append("||" + " " * 25 + "FACTURA DE PAGO" + " " * 36 + "||")
        lineas.append("||" + " " * 20 + "BIBLIOTECA UCC - COLOMBIA" + " " * 31 + "||")
        lineas.append("||" + " " * 76 + "||")
        lineas.append("=" * 80)
        
        # Información de la factura
        lineas.append("")
        lineas.append(f"Numero de Factura: {self.numero_factura}")
        lineas.append(f"Fecha de Emision:  {self.fecha_emision.strftime('%Y-%m-%d %H:%M:%S')}")
        lineas.append(f"Cliente:           {self.prestamo_base.usuario}")
        lineas.append("")
        lineas.append("-" * 80)
        
        # Información del recurso
        lineas.append("")
        lineas.append("[DETALLE DEL PRESTAMO]")
        lineas.append(f"Recurso:           {self.prestamo_base.recurso.titulo}")
        lineas.append(f"Autor:             {self.prestamo_base.recurso.autor}")
        lineas.append(f"ISBN:              {self.prestamo_base.recurso.isbn}")
        lineas.append(f"Tipo:              {self.prestamo_base.recurso.obtener_tipo_recurso()}")
        lineas.append(f"Fecha Prestamo:    {self.prestamo_base.fecha_prestamo.strftime('%Y-%m-%d')}")
        lineas.append(f"Fecha Devolucion:  {self.prestamo.obtener_fecha_devolucion().strftime('%Y-%m-%d')}")
        lineas.append(f"Duracion:          {self.prestamo.obtener_duracion_dias()} dias")
        
        dias_retraso = self.prestamo_base.calcular_dias_retraso()
        if dias_retraso > 0:
            lineas.append(f"Dias de Retraso:   {dias_retraso} dias [MORA]")
        
        lineas.append("")
        lineas.append("-" * 80)
        
        # Items de la factura
        lineas.append("")
        lineas.append("[DETALLE DE COBRO]")
        lineas.append("")
        lineas.append("+----+------------------------------------------+-----+----------+-----------+")
        lineas.append("| #  | Descripcion                              | Qty | Unitario | Subtotal  |")
        lineas.append("+----+------------------------------------------+-----+----------+-----------+")
        
        for i, item in enumerate(self.items, 1):
            desc = item.descripcion[:40].ljust(40)
            lineas.append(f"| {i:<2} | {desc} | {item.cantidad:>3} | ${item.valor_unitario:>7.2f} | ${item.subtotal:>8.2f} |")
        
        lineas.append("+----+------------------------------------------+-----+----------+-----------+")
        
        # Totales
        subtotal = self.calcular_subtotal()
        iva = self.calcular_iva(0.0)
        total = self.calcular_total(0.0)
        
        lineas.append("")
        lineas.append(f"{'':>60} SUBTOTAL: ${subtotal:>10.2f}")
        lineas.append(f"{'':>60} IVA (0%): ${iva:>10.2f}")
        lineas.append(f"{'':>60} {'=' * 24}")
        lineas.append(f"{'':>60} TOTAL A PAGAR: ${total:>10.2f}")
        lineas.append("")
        lineas.append("-" * 80)
        
        # Pie de factura
        lineas.append("")
        lineas.append("[METODOS DE PAGO ACEPTADOS]")
        lineas.append("  - Efectivo en caja")
        lineas.append("  - Tarjeta de credito/debito")
        lineas.append("  - Transferencia bancaria")
        lineas.append("  - PSE - Pagos Seguros en Linea")
        lineas.append("")
        lineas.append("[INFORMACION ADICIONAL]")
        lineas.append(f"  Estrategia de Multa: {self.prestamo_base.estrategia_multa.obtener_nombre_estrategia()}")
        lineas.append("  Los servicios educativos estan exentos de IVA segun normativa colombiana")
        lineas.append("")
        lineas.append("=" * 80)
        lineas.append("||" + " " * 76 + "||")
        lineas.append("||" + " " * 22 + "GRACIAS POR SU PAGO" + " " * 35 + "||")
        lineas.append("||" + " " * 15 + "Universidad Cooperativa de Colombia" + " " * 26 + "||")
        lineas.append("||" + " " * 76 + "||")
        lineas.append("=" * 80)
        
        return "\n".join(lineas)
    
    def obtener_resumen(self) -> Tuple[int, float, float]:
        """Retorna un resumen: (cantidad_items, subtotal, total)."""
        return len(self.items), self.calcular_subtotal(), self.calcular_total()


class GestorFacturacion:
    """Gestiona la generación de facturas."""
    
    def __init__(self):
        self.contador_facturas = 1
        self.facturas_generadas = []
    
    def generar_numero_factura(self) -> str:
        """Genera un número único de factura."""
        numero = f"FACT-UCC-{self.contador_facturas:06d}"
        self.contador_facturas += 1
        return numero
    
    def crear_factura(self, prestamo, prestamo_base, incluir_multa: bool = True) -> Factura:
        """Crea una nueva factura."""
        numero = self.generar_numero_factura()
        factura = Factura(numero, prestamo, prestamo_base)
        
        if incluir_multa:
            factura.agregar_multa()
        
        self.facturas_generadas.append(factura)
        return factura
    
    def obtener_total_facturado(self) -> float:
        """Retorna el total facturado."""
        return sum(f.calcular_total() for f in self.facturas_generadas)
    
    def obtener_cantidad_facturas(self) -> int:
        """Retorna la cantidad de facturas generadas."""
        return len(self.facturas_generadas)