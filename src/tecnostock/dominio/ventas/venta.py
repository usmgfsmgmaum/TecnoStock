# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List
from tecnostock.dominio.apartados.apartado import ReglaNegocioExcepcion

@dataclass(frozen=True)
class ItemVenta:
    articulo_id: str
    cantidad: int
    precio_unitario: Decimal

    @property
    def subtotal(self) -> Decimal:
        return self.precio_unitario * Decimal(self.cantidad)

@dataclass
class Venta:
    """Entidad de Dominio que modela una venta directa de mercancía (CU-01)."""
    venta_id: str
    cliente_id: str
    sucursal_id: str
    items: List[ItemVenta] = field(default_factory=list)
    monto_pagado: Decimal = Decimal("0.00")
    fecha_venta: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not self.items:
            raise ReglaNegocioExcepcion("Una venta debe contener al menos un ítem.")
        if self.monto_pagado < self.monto_total:
            raise ReglaNegocioExcepcion(
                f"El monto pagado (${self.monto_pagado:.2f}) es menor al total de la venta (${self.monto_total:.2f})."
            )

    @property
    def monto_total(self) -> Decimal:
        """Calcula el costo total de la venta sumando los subtotales de sus ítems."""
        return sum((item.subtotal for item in self.items), Decimal("0.00"))