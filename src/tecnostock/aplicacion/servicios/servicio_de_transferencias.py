==========================================
Autores: Equipo 5 (Noguera, Pérez, Paez)
Proyecto: TecnoStock (Caso 05)
==========================================
import logging
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from tecnostock.dominio.apartados.apartado import ReglaNegocioExcepcion
from tecnostock.aplicacion.comandos import (
PeticionSolicitarTransferencia,
PeticionAutorizarTransferencia
)

logger = logging.getLogger(name)

class EstadoTransferencia(Enum):
SOLICITADA = "SOLICITADA"
AUTORIZADA = "AUTORIZADA"
RECHAZADA = "RECHAZADA"
EN_TRANSITO = "EN_TRANSITO"
COMPLETADA = "COMPLETADA"

@dataclass
class RegistroTransferencia:
transferencia_id: str
sucursal_origen_id: str
sucursal_destino_id: str
articulo_id: str
cantidad: int
solicitante_id: str
estado: EstadoTransferencia = EstadoTransferencia.SOLICITADA
autorizador_id: Optional[str] = None
fecha_solicitud: datetime = datetime.utcnow()
observaciones: Optional[str] = None

class ServicioDeTransferencias:
"""
Servicio de Aplicación EXCLUSIVO del Equipo 5.
Gestiona la orquestación y autorizaciones de transferencias (CU-06).
"""def __init__(self, unidad_trabajo_factory):

    self.unidad_trabajo_factory = unidad_trabajo_factory

def solicitar_transferencia(self, peticion: PeticionSolicitarTransferencia) -> str:

    logger.info(

        f"Solicitando transferencia de {peticion.cantidad} unidades "

        f"del artículo {peticion.articulo_id} de {peticion.sucursal_origen_id} "

        f"a {peticion.sucursal_destino_id}"

    )

    if peticion.sucursal_origen_id == peticion.sucursal_destino_id:

        raise ReglaNegocioExcepcion("La sucursal origen y destino no pueden ser la misma.")

    with self.unidad_trabajo_factory() as unidad_trabajo:

        stock_origen = unidad_trabajo.inventario.obtener_stock(

            peticion.sucursal_origen_id, peticion.articulo_id

        )

        if stock_origen < peticion.cantidad:

            raise ReglaNegocioExcepcion(

                f"La sucursal origen no tiene stock suficiente. Disponible: {stock_origen}"

            )

        transferencia_id = unidad_trabajo.transferencias.generar_id()

        registro = RegistroTransferencia(

            transferencia_id=transferencia_id,

            sucursal_origen_id=peticion.sucursal_origen_id,

            sucursal_destino_id=peticion.sucursal_destino_id,

            articulo_id=peticion.articulo_id,

            cantidad=peticion.cantidad,

            solicitante_id=peticion.solicitante_id

        )

        # Retener stock en tránsito preliminar

        unidad_trabajo.inventario.bloquear_stock_transito(

            peticion.sucursal_origen_id, peticion.articulo_id, peticion.cantidad

        )

        

        unidad_trabajo.transferencias.guardar(registro)

        unidad_trabajo.commit()

        

        return transferencia_id

def procesar_autorizacion(self, peticion: PeticionAutorizarTransferencia) -> None:

    logger.info(f"Procesando autorización para transferencia: {peticion.transferencia_id}")

    

    with self.unidad_trabajo_factory() as unidad_trabajo:

        transferencia = unidad_trabajo.transferencias.obtener_por_id(peticion.transferencia_id)

        if not transferencia:

            raise ReglaNegocioExcepcion(f"Transferencia {peticion.transferencia_id} no existe.")

        if transferencia.estado != EstadoTransferencia.SOLICITADA:

            raise ReglaNegocioExcepcion("La transferencia ya ha sido procesada previamente.")

        transferencia.autorizador_id = peticion.autorizador_id

        transferencia.observaciones = peticion.observaciones

        if peticion.aprobado:

            transferencia.estado = EstadoTransferencia.AUTORIZADA

            # Ejecutar movimiento efectivo entre almacenes

            unidad_trabajo.inventario.descontar_stock(

                transferencia.sucursal_origen_id, transferencia.articulo_id, transferencia.cantidad

            )

            unidad_trabajo.inventario.incrementar_stock(

                transferencia.sucursal_destino_id, transferencia.articulo_id, transferencia.cantidad

            )

            transferencia.estado = EstadoTransferencia.COMPLETADA

            logger.info(f"Transferencia {peticion.transferencia_id} aprobada y ejecutada.")

        else:

            transferencia.estado = EstadoTransferencia.RECHAZADA

            # Liberar stock retenido

            unidad_trabajo.inventario.desbloquear_stock_transito(

                transferencia.sucursal_origen_id, transferencia.articulo_id, transferencia.cantidad

            )

            logger.info(f"Transferencia {peticion.transferencia_id} rechazada.")

        unidad_trabajo.transferencias.guardar(transferencia)

        unidad_trabajo.commit()

