
# ==========================================

# Autores: Equipo 5 (Noguera, Pérez, Paez)

# Proyecto: TecnoStock (Caso 05)

# ==========================================

from dataclasses import dataclass

from decimal import Decimal

from typing import List, Optional


@dataclass(frozen=True)

class ItemPeticion:

    articulo_id: str

    cantidad: int

    precio_unitario: Decimal


@dataclass(frozen=True)

class PeticionCrearApartado:

    cliente_id: str

    sucursal_id: str

    items: List[ItemPeticion]

    monto_anticipo: Decimal


@dataclass(frozen=True)

class PeticionLiquidarApartado:

    apartado_id: str

    monto_pago: Decimal


@dataclass(frozen=True)

class PeticionSolicitarTransferencia:

    sucursal_origen_id: str

    sucursal_destino_id: str

    articulo_id: str

    cantidad: int

    solicitante_id: str


@dataclass(frozen=True)

class PeticionAutorizarTransferencia:

    transferencia_id: str

    autorizador_id: str

    aprobado: bool

    observaciones: Optional[str] = None

