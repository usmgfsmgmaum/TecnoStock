# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from dataclasses import dataclass
from decimal import Decimal
from tecnostock.dominio.apartados.apartado import ReglaNegocioExcepcion

@dataclass
class Producto:
    """Entidad principal del catálogo de mercancía."""
    articulo_id: str
    sku: str
    nombre: str
    descripcion: str
    precio_lista: Decimal
    categoria: str

    def __post_init__(self):
        # Regla de Negocio básica: Nada es gratis en TecnoStock
        if self.precio_lista <= Decimal("0.00"):
            raise ReglaNegocioExcepcion("El precio de lista de un producto debe ser mayor a cero.")