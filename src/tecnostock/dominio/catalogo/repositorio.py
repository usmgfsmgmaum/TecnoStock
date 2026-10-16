# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from abc import ABC, abstractmethod
from typing import Optional
from tecnostock.dominio.catalogo.producto import Producto

class IRepositorioCatalogo(ABC):
    """Puerto de salida para obtener información estática de los productos."""
    
    @abstractmethod
    def obtener_por_id(self, articulo_id: str) -> Optional[Producto]:
        pass

    @abstractmethod
    def buscar_por_sku(self, sku: str) -> Optional[Producto]:
        pass