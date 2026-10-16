# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from decimal import Decimal
from typing import List
from tecnostock.dominio.apartados.apartado import Apartado, ReglaNegocioExcepcion

class PoliticaComercialApartados:
    """
    Política de Dominio para validar las reglas comerciales del Equipo 5 (CU-04).
    Centraliza los límites y restricciones del negocio de TecnoStock.
    """

    LIMITE_GLOBAL_ARTICULOS: int = 5
    PORCENTAJE_MINIMO_ANTICIPO: Decimal = Decimal("0.20")
    DIAS_MAXIMOS_VIGENCIA: int = 30

    @classmethod
    def validar_nuevo_apartado(cls, items_existentes_cliente: List[Apartado], nuevos_items_cantidad: int, monto_anticipo: Decimal, monto_total: Decimal) -> None:
        """Valida de forma integral las reglas de negocio antes de permitir un apartado."""
        
        # 1. Validación del límite global de artículos activos por cliente
        total_articulos_activos = sum(
            sum(item.cantidad for item in apartado.items) 
            for apartado in items_existentes_cliente
        )
        
        if (total_articulos_activos + nuevos_items_cantidad) > cls.LIMITE_GLOBAL_ARTICULOS:
            raise ReglaNegocioExcepcion(
                f"Límite de artículos excedido. El cliente ya cuenta con {total_articulos_activos} "
                f"artículos en apartados activos y excede el máximo permitido de {cls.LIMITE_GLOBAL_ARTICULOS}."
            )

        # 2. Validación estricta del anticipo mínimo del 20%
        anticipo_requerido = monto_total * cls.PORCENTAJE_MINIMO_ANTICIPO
        if monto_anticipo < anticipo_requerido:
            raise ReglaNegocioExcepcion(
                f"Anticipo insuficiente. Se requiere al menos el 20% (${anticipo_requerido:.2f}) "
                f"del total de la compra (${monto_total:.2f})."
            )