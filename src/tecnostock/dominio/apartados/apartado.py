from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional
from enum import Enum

class EstadoApartado(Enum):
PENDIENTE = "PENDIENTE"
COMPLETADO = "COMPLETADO"
CANCELADO = "CANCELADO"
VENCIDO = "VENCIDO"

class ReglaNegocioExcepcion(Exception):
"""Excepción base para violaciones de reglas de dominio."""
pass

@dataclass(frozen=True)
def ItemApartado:
articulo_id: str
cantidad: int
precio_unitario: Decimal@property

def subtotal(self) -> Decimal:

    return self.precio_unitario * Decimal(self.cantidad)

@dataclass
class Apartado:
apartado_id: str
cliente_id: str
sucursal_id: str
items: List[ItemApartado] = field(default_factory=list)
anticipo_pagado: Decimal = Decimal("0.00")
estado: EstadoApartado = EstadoApartado.PENDIENTE
fecha_creacion: datetime = field(default_factory=datetime.utcnow)
fecha_limite: Optional[datetime] = NoneLIMITE_MAX_ARTICULOS: int = 5

PORCENTAJE_ANTICIPO_MINIMO: Decimal = Decimal("0.20")

DIAS_VIGENCIA_ESTANDAR: int = 30

def __post_init__(self):

    if not self.fecha_limite:

        self.fecha_limite = self.fecha_creacion + timedelta(days=self.DIAS_VIGENCIA_ESTANDAR)

@property

def monto_total(self) -> Decimal:

    return sum((item.subtotal for item in self.items), Decimal("0.00"))

@property

def anticipo_requerido(self) -> Decimal:

    return self.monto_total * self.PORCENTAJE_ANTICIPO_MINIMO

@property

def saldo_pendiente(self) -> Decimal:

    return self.monto_total - self.anticipo_pagado

def validar_limite_articulos(self, cantidad_adicional: int = 0) -> None:

    total_articulos = sum(item.cantidad for item in self.items) + cantidad_adicional

    if total_articulos > self.LIMITE_MAX_ARTICULOS:

        raise ReglaNegocioExcepcion(

            f"Límite de artículos excedido. Máximo permitido: {self.LIMITE_MAX_ARTICULOS}, "

            f"intentando registrar: {total_articulos}."

        )

def agregar_item(self, articulo_id: str, cantidad: int, precio_unitario: Decimal) -> None:

    if self.estado != EstadoApartado.PENDIENTE:

        raise ReglaNegocioExcepcion("No se pueden agregar ítems a un apartado finalizado o cancelado.")

    

    if cantidad <= 0:

        raise ReglaNegocioExcepcion("La cantidad debe ser mayor a cero.")

        

    self.validar_limite_articulos(cantidad)

    

    item_existente = next((i for i in self.items if i.articulo_id == articulo_id), None)

    if item_existente:

        self.items.remove(item_existente)

        nueva_cantidad = item_existente.cantidad + cantidad

        self.items.append(ItemApartado(articulo_id, nueva_cantidad, precio_unitario))

    else:

        self.items.append(ItemApartado(articulo_id, cantidad, precio_unitario))

def registrar_anticipo_inicial(self, monto: Decimal) -> None:

    if self.estado != EstadoApartado.PENDIENTE:

        raise ReglaNegocioExcepcion("El apartado no está en estado pendiente.")

        

    if not self.items:

        raise ReglaNegocioExcepcion("No se puede registrar un anticipo sin ítems en el apartado.")

        

    monto_minimo = self.anticipo_requerido

    if monto < monto_minimo:

        raise ReglaNegocioExcepcion(

            f"El anticipo de ${monto:.2f} es insuficiente. "

            f"Se requiere al menos el 20% (${monto_minimo:.2f})."

        )

        

    self.anticipo_pagado = monto

def liquidar(self, monto_pago: Decimal) -> None:

    if self.estado != EstadoApartado.PENDIENTE:

        raise ReglaNegocioExcepcion("Solo se pueden liquidar apartados pendientes.")

        

    if datetime.utcnow() > self.fecha_limite:

        self.estado = EstadoApartado.VENCIDO

        raise ReglaNegocioExcepcion("El apartado se encuentra vencido.")

    if monto_pago < self.saldo_pendiente:

        raise ReglaNegocioExcepcion(

            f"Monto insuficiente para liquidar. Saldo restante: ${self.saldo_pendiente:.2f}."

        )

    self.anticipo_pagado += monto_pago

    self.estado = EstadoApartado.COMPLETADO

