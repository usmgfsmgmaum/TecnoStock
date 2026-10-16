# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from abc import ABC, abstractmethod
from typing import Optional
from tecnostock.dominio.inventario.unidad_inventario import UnidadInventario

class IRepositorioInventarioDominio(ABC):
    """Puerto de dominio para la persistencia y consulta del inventario por sucursal."""

    @abstractmethod
    def obtener_unidad(self, sucursal_id: str, articulo_id: str) -> Optional[UnidadInventario]:
        """Recupera el registro de inventario para un artículo en una sucursal específica."""
        pass

    @abstractmethod
    def guardar(self, unidad: UnidadInventario) -> None:
        """Persiste los cambios del inventario."""
        pass