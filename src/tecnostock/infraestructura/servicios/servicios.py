# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

import logging
from decimal import Decimal
from typing import Optional

from tecnostock.aplicacion.puertos.puertos import IServicioNotificaciones, IMonederoDigital
from tecnostock.infraestructura.persistencia_en_memoria.almacen import almacen_global

logger = logging.getLogger(__name__)

class ServicioNotificacionesInfraestructura(IServicioNotificaciones):
    """
    Implementación concreta del puerto IServicioNotificaciones.
    Simula el envío de alertas a los almacenes (para transferencias o eventos del Equipo 5).
    """
    
    def enviar_alerta_almacen(self, sucursal_id: str, mensaje: str) -> None:
        logger.info(f"[ALERTA ALMACÉN] Sucursal [{sucursal_id}]: {mensaje}")
        print(f"🔔 [Notificación Almacén - {sucursal_id}]: {mensaje}")


class MonederoDigitalInfraestructura(IMonederoDigital):
    """
    Implementación concreta del puerto IMonederoDigital.
    Gestiona el abono de saldos a favor (por ejemplo, cuando un apartado vence y se devuelve el anticipo).
    """

    def abonar_saldo(self, cliente_id: str, monto: Decimal, concepto: str) -> None:
        logger.info(f"Abonando ${monto:.2f} al cliente {cliente_id}. Concepto: {concepto}")
        
        # Simulando el almacenamiento en memoria
        saldo_actual = almacen_global.monederos.get(cliente_id, Decimal("0.00"))
        nuevo_saldo = saldo_actual + monto
        almacen_global.monederos[cliente_id] = nuevo_saldo
        
        print(f"💰 [Monedero Digital]: Se abonaron ${monto:.2f} al cliente {cliente_id}. Saldo actual: ${nuevo_saldo:.2f} ({concepto})")