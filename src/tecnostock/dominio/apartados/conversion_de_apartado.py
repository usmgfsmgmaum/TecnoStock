# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from datetime import datetime
from decimal import Decimal
from tecnostock.dominio.apartados.apartado import Apartado, EstadoApartado, ReglaNegocioExcepcion

class ConversionDeApartado:
    """Servicio de Dominio para orquestar la conversión de un apartado en venta al liquidarlo."""

    @staticmethod
    def convertir_a_venta(apartado: Apartado, monto_pago: Decimal, fecha_actual: datetime = None) -> None:
        if fecha_actual is None:
            fecha_actual = datetime.utcnow()

        # 1. Validar si el tiempo ya pasó
        if apartado.fecha_limite and fecha_actual > apartado.fecha_limite:
            apartado.estado = EstadoApartado.VENCIDO
            raise ReglaNegocioExcepcion("No se puede convertir el apartado porque se encuentra vencido.")

        # 2. Validar que el cliente traiga el dinero completo para liquidar
        if monto_pago < apartado.saldo_pendiente:
            raise ReglaNegocioExcepcion(
                f"Monto insuficiente para liquidar y convertir a venta. Saldo pendiente: ${apartado.saldo_pendiente:.2f}."
            )

        # 3. Marcar como completado
        apartado.liquidar(monto_pago)