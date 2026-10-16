# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass(frozen=True)
class EventoDominioBase:
    ocurrido_en: datetime = datetime.utcnow()

@dataclass(frozen=True)
class ApartadoCreado(EventoDominioBase):
    folio: str
    fecha_limite: datetime

@dataclass(frozen=True)
class ApartadoVencido(EventoDominioBase):
    apartado_id: str
    cliente_id: str
    sucursal_id: str
    monto_anticipo: Decimal

@dataclass(frozen=True)
class TransferenciaAutorizada(EventoDominioBase):
    transferencia_id: str
    sucursal_origen_id: str
    sucursal_destino_id: str
    articulo_id: str
    cantidad: int