# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from abc import ABC, abstractmethod
from typing import Optional
from tecnostock.dominio.ventas.venta import Venta
from tecnostock.aplicacion.comandos import PeticionRegistrarVenta

class IRepositorioVentas(ABC):
    """Puerto de dominio para la persistencia de ventas directas."""

    @abstractmethod
    def generar_id(self) -> str:
        """Genera un identificador único para una nueva venta."""
        pass

    @abstractmethod
    def guardar(self, venta: Venta) -> None:
        """Persiste una entidad Venta completa."""
        pass

    @abstractmethod
    def guardar_venta(self, venta_id: str, peticion: PeticionRegistrarVenta) -> None:
        """Registra una venta utilizando los datos de la petición de aplicación."""
        pass

    @abstractmethod
    def obtener_por_id(self, venta_id: str) -> Optional[Venta]:
        """Recupera una venta por su identificador."""
        pass
