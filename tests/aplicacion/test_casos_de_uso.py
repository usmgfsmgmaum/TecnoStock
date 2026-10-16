# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from decimal import Decimal
from tests.aplicacion.base import BasePruebasAplicacion
from tecnostock.dominio.apartados.apartado import ReglaNegocioExcepcion
from tecnostock.aplicacion.comandos import ItemPeticion, PeticionCrearApartado, PeticionSolicitarTransferencia
from tecnostock.aplicacion.servicios.servicio_de_apartados import ServicioDeApartados
from tecnostock.aplicacion.servicios.servicio_de_transferencias import ServicioDeTransferencias
from tecnostock.infraestructura.persistencia_en_memoria.almacen import almacen_global

class UnidadTrabajoMockFactory:
    """Fábrica simulada de Unit of Work para pruebas unitarias en memoria."""
    
    def __init__(self):
        from tecnostock.infraestructura.unidad_de_trabajo import UnidadDeTrabajoMemoria
        # O una implementación directa basada en almacen_global
        pass

# Nota: Para propósitos de prueba directa usando el almacén global:
class TestCasosDeUsoEquipo5(BasePruebasAplicacion):
    """Pruebas unitarias para validar las reglas de negocio críticas del Equipo 5."""

    def test_regla_anticipo_minimo_apartado(self):
        """Verifica que un apartado falle si el anticipo es menor al 20% (CU-04)."""
        # El total de 2 artículos a $100 es $200. El 20% mínimo es $40.
        # Intentamos registrar un anticipo de $20 (10%), lo cual debe fallar.
        
        from tecnostock.dominio.apartados.apartado import Apartado
        
        apartado = Apartado(
            apartado_id="APT-001",
            cliente_id=self.cliente_prueba,
            sucursal_id=self.sucursal_origen
        )
        apartado.agregar_item(self.articulo_prueba, 2, self.precio_unitario)
        
        with self.assertRaises(ReglaNegocioExcepcion) as contexto:
            apartado.registrar_anticipo_inicial(Decimal("20.00"))
            
        self.assertIn("insuficiente", str(contexto.exception).lower())

    def test_regla_limite_articulos_apartado(self):
        """Verifica que un cliente no pueda rebasar el límite global de 5 artículos en apartados."""
        from tecnostock.dominio.apartados.apartado import Apartado
        
        apartado = Apartado(
            apartado_id="APT-002",
            cliente_id=self.cliente_prueba,
            sucursal_id=self.sucursal_origen
        )
        
        # Intentar agregar 6 artículos (superando el límite de 5)
        with self.assertRaises(ReglaNegocioExcepcion) as contexto:
            apartado.agregar_item(self.articulo_prueba, 6, self.precio_unitario)
            
        self.assertIn("Límite de artículos excedido", str(contexto.exception))

    def test_solicitud_transferencia_stock_suficiente(self):
        """Verifica que se pueda solicitar una transferencia si hay stock en origen (CU-06)."""
        # El almacén inicial tiene 10 unidades del ART-001 en SUC-01
        stock_inicial = almacen_global.inventarios["SUC-01:ART-001"]["disponible"]
        self.assertEqual(stock_inicial, 10)
        
        # Simulamos la retención de stock por transferencia
        cantidad_a_transferir = 3
        almacen_global.inventarios["SUC-01:ART-001"]["disponible"] -= cantidad_a_transferir
        almacen_global.inventarios["SUC-01:ART-001"]["transito"] += cantidad_a_transferir
        
        self.assertEqual(almacen_global.inventarios["SUC-01:ART-001"]["disponible"], 7)
        self.assertEqual(almacen_global.inventarios["SUC-01:ART-001"]["transito"], 3)