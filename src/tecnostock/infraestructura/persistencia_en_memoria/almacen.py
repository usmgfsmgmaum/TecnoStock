# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from typing import Dict, List, Optional
from decimal import Decimal

from tecnostock.dominio.apartados.apartado import Apartado
from tecnostock.aplicacion.servicios.servicio_de_transferencias import RegistroTransferencia
from tecnostock.dominio.ventas.venta import Venta
from tecnostock.aplicacion.comandos import PeticionRegistrarVenta

class AlmacenEnMemoria:
    """
    Base de datos simulada en memoria RAM para pruebas y ejecución local.
    Mantiene diccionarios centralizados para cada entidad del sistema del Equipo 5.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(AlmacenEnMemoria, cls).__new__(cls)
            cls._instancia._inicializar_almacenes()
        return cls._instancia

    def _inicializar_almacenes(self):
        # Diccionarios de almacenamiento simulado
        self.apartados: Dict[str, Apartado] = {}
        self.transferencias: Dict[str, RegistroTransferencia] = {}
        self.ventas: Dict[str, Venta] = {}
        
        # Inventario estructurado por clave compuesta: "sucursal_id:articulo_id" -> dict con estados
        # Estados: 'disponible', 'reservado', 'transito'
        self.inventarios: Dict[str, Dict[str, int]] = {
            "SUC-01:ART-001": {"disponible": 10, "reservado": 0, "transito": 0},
            "SUC-01:ART-002": {"disponible": 5, "reservado": 0, "transito": 0},
            "SUC-02:ART-001": {"disponible": 8, "reservado": 0, "transito": 0},
        }
        
        # Monedero digital simulado: cliente_id -> saldo Decimal
        self.monederos: Dict[str, Decimal] = {}

    def limpiar(self):
        """Reinicia todos los almacenes a su estado inicial (útil para pruebas unitarias)."""
        self.apartados.clear()
        self.transferencias.clear()
        self.ventas.clear()
        self.inventarios.clear()
        self.monederos.clear()
        self._inicializar_almacenes()


# Instancia global compartida para la simulación
almacen_global = AlmacenEnMemoria()