# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

import logging
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

logger = logging.getLogger(__name__)

# ====================================================================
# Definición de Eventos de Dominio
# ====================================================================

@dataclass(frozen=True)
class EventoDominio:
    ocurrido_en: datetime = datetime.utcnow()

@dataclass(frozen=True)
class ApartadoVencido(EventoDominio):
    apartado_id: str
    cliente_id: str
    sucursal_id: str
    monto_anticipo: Decimal

@dataclass(frozen=True)
class TransferenciaAutorizada(EventoDominio):
    transferencia_id: str
    sucursal_origen_id: str
    sucursal_destino_id: str
    articulo_id: str
    cantidad: int

@dataclass(frozen=True)
class TransferenciaRechazada(EventoDominio):
    transferencia_id: str
    sucursal_origen_id: str
    motivo: Optional[str] = None


# ====================================================================
# Manejadores (Efectos Secundarios)
# ====================================================================

class ManejadorDeVencimientos:
    """Maneja los eventos derivados del vencimiento de apartados (Consistencia Eventual)."""
    
    def __init__(self, unidad_trabajo_factory):
        self.unidad_trabajo_factory = unidad_trabajo_factory

    def manejar_apartado_vencido(self, evento: ApartadoVencido) -> None:
        logger.info(f"Procesando vencimiento del apartado {evento.apartado_id}")
        
        with self.unidad_trabajo_factory() as unidad_trabajo:
            apartado = unidad_trabajo.apartados.obtener_por_id(evento.apartado_id)
            if apartado:
                # 1. Liberar stock reservado en el inventario
                for item in apartado.items:
                    unidad_trabajo.inventario.liberar_stock_reserva(
                        evento.sucursal_id, item.articulo_id, item.cantidad
                    )
                
                # 2. Acreditar saldo a favor en monedero digital del cliente
                unidad_trabajo.monedero.abonar_saldo(
                    cliente_id=evento.cliente_id,
                    monto=evento.monto_anticipo,
                    concepto=f"Abono por vencimiento de apartado {evento.apartado_id}"
                )
                
                unidad_trabajo.commit()
                logger.info(f"Stock liberado y saldo de ${evento.monto_anticipo:.2f} abonado a monedero del cliente {evento.cliente_id}.")


class ManejadorDeNotificacionesTransferencia:
    """
    Manejador exclusivo del Equipo 5 (CU-06).
    Envía alertas a los almacenes según la resolución de transferencias por el Supervisor.
    """
    
    def __init__(self, servicio_notificaciones):
        self.servicio_notificaciones = servicio_notificaciones

    def manejar_transferencia_autorizada(self, evento: TransferenciaAutorizada) -> None:
        logger.info(f"Notificando autorización de transferencia {evento.transferencia_id}")
        
        # Alerta a Sucursal Origen para que prepare el envío
        self.servicio_notificaciones.enviar_alerta_almacen(
            sucursal_id=evento.sucursal_origen_id,
            mensaje=f"Preparar despachar {evento.cantidad} unidades de {evento.articulo_id} hacia {evento.sucursal_destino_id}."
        )
        
        # Alerta a Sucursal Destino para que espere la mercancía
        self.servicio_notificaciones.enviar_alerta_almacen(
            sucursal_id=evento.sucursal_destino_id,
            mensaje=f"Transferencia {evento.transferencia_id} autorizada. Pendiente recepción de {evento.cantidad} unidades de {evento.articulo_id}."
        )

    def manejar_transferencia_rechazada(self, evento: TransferenciaRechazada) -> None:
        logger.info(f"Notificando rechazo de transferencia {evento.transferencia_id}")
        
        self.servicio_notificaciones.enviar_alerta_almacen(
            sucursal_id=evento.sucursal_origen_id,
            mensaje=f"Transferencia {evento.transferencia_id} rechazada. Motivo: {evento.motivo or 'No especificado'}. Stock en tránsito liberado."
        )