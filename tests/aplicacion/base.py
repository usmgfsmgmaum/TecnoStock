# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

import unittest
from decimal import Decimal
from tecnostock.infraestructura.persistencia_en_memoria.almacen import almacen_global

class BasePruebasAplicacion(unittest.TestCase):
    """Clase base para configurar el entorno de pruebas de la aplicación."""

    def setUp(self):
        # Limpiamos el almacén global en memoria antes de cada prueba individual
        almacen_global.limpiar()
        
        # Datos de prueba estándar para el Equipo 5
        self.cliente_prueba = "CLI-999"
        self.sucursal_origen = "SUC-01"
        self.sucursal_destino = "SUC-02"
        self.articulo_prueba = "ART-001"
        self.precio_unitario = Decimal("100.00")