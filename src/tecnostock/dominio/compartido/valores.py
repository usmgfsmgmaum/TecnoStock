# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class ClienteId:
    valor: str

@dataclass(frozen=True)
class SucursalId:
    valor: str

@dataclass(frozen=True)
class ArticuloId:
    valor: str

@dataclass(frozen=True)
class Folio:
    valor: str

@dataclass(frozen=True)
class Dinero:
    monto: Decimal

    def __post_init__(self):
        if self.monto < Decimal("0.00"):
            raise ValueError("El monto monetario no puede ser negativo.")

    def es_menor_que(self, otro: 'Dinero') -> bool:
        return self.monto < otro.monto

    def restar(self, otro: 'Dinero') -> 'Dinero':
        return Dinero(self.monto - otro.monto)

    def sumar(self, otro: 'Dinero') -> 'Dinero':
        return Dinero(self.monto + otro.monto)