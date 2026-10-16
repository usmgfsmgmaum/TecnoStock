# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

import unittest
from decimal import Decimal
from tecnostock.dominio.apartados.apartado import Apartado, ReglaNegocioExcepcion
from tecnostock.dominio.inventario.unidad_inventario import UnidadInventario
from tecnostock.dominio.catalogo.producto import Producto

class TestInvariantesDominioEquipo5(unittest.TestCase):
    """Pruebas unitarias para blindar las reglas puras del Modelo de Dominio (Equipo 5)."""

    def test_invariante_producto_precio_valido(self):
        """Verifica que no se pueda crear un producto con precio cero o negativo."""
        with self.assertRaises(ReglaNegocioExcepcion):
            Producto(
                articulo_id="ART-999",
                sku="SKU-TEST",
                nombre="Producto Inválido",
                descripcion="Prueba",
                precio_lista=Decimal("0.00"),
                categoria="General"
            )

    def test_invariante_inventario_no_negativo(self):
        """Verifica que el inventario por sucursal lance excepción si maneja stocks negativos."""
        with self.assertRaises(ReglaNegocioExcepcion):
            UnidadInventario(
                sucursal_id="SUC-01",
                articulo_id="ART-001",
                stock_disponible=-5  # Inválido
            )

    def test_invariante_apartado_calculo_anticipo_requerido(self):
        """Verifica que el cálculo matemático del 20% de anticipo sea exacto según las reglas del CU-04."""
        apartado = Apartado(
            apartado_id="APT-TEST",
            cliente_id="CLI-001",
            sucursal_id="SUC-01"
        )
        # Agregamos 2 artículos a $250 c/u -> Total = $500.00
        apartado.agregar_item("ART-001", 2, Decimal("250.00"))
        
        # El anticipo requerido debe ser exactamente el 20% de $500, es decir, $100.00
        self.assertEqual(apartado.anticipo_requerido, Decimal("100.00"))
        self.assertEqual(apartado.saldo_pendiente, Decimal("500.00"))

    def test_invariante_agregar_item_cantidad_cero_o_negativa(self):
        """Verifica que no se puedan agregar cantidades nulas o negativas a un apartado."""
        apartado = Apartado(
            apartado_id="APT-TEST-2",
            cliente_id="CLI-001",
            sucursal_id="SUC-01"
        )
        with self.assertRaises(ReglaNegocioExcepcion):
            apartado.agregar_item("ART-001", 0, Decimal("100.00"))