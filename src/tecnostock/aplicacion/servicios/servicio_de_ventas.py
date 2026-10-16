# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

import logging
from dataclasses import dataclass
from decimal import Decimal
from typing import List

from tecnostock.dominio.apartados.apartado import ReglaNegocioExcepcion
from tecnostock.aplicacion.comandos import ItemPeticion

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class PeticionRegistrarVenta:
    cliente_id: str
    sucursal_id: str
    items: List[ItemPeticion]
    monto_pagado: Decimal

class ServicioDeVentas:
    """
    Servicio de Aplicación EXCLUSIVO del Equipo 5.
    Orquesta la venta directa de mercancía (CU-01 / Flujo Adicional).
    """
    
    def __init__(self, unidad_trabajo_factory):
        self.unidad_trabajo_factory = unidad_trabajo_factory

    def registrar_venta(self, peticion: PeticionRegistrarVenta) -> str:
        logger.info(f"Registrando venta directa para cliente: {peticion.cliente_id} en sucursal: {peticion.sucursal_id}")
        
        with self.unidad_trabajo_factory() as unidad_trabajo:
            # 1. Validar disponibilidad física del inventario antes de vender
            for item in peticion.items:
                stock_disponible = unidad_trabajo.inventario.obtener_stock(
                    peticion.sucursal_id, item.articulo_id
                )
                if stock_disponible < item.cantidad:
                    raise ReglaNegocioExcepcion(
                        f"Stock insuficiente para artículo {item.articulo_id}. Disponible: {stock_disponible}"
                    )

            # 2. Registrar la venta en la BD
            venta_id = unidad_trabajo.ventas.generar_id()
            
            # 3. Descontar el stock definitivo
            for item in peticion.items:
                unidad_trabajo.inventario.descontar_stock(
                    peticion.sucursal_id, item.articulo_id, item.cantidad
                )

            # 4. Guardar y confirmar
            unidad_trabajo.ventas.guardar_venta(venta_id, peticion)
            unidad_trabajo.commit()
            
            logger.info(f"Venta {venta_id} registrada con éxito.")
            return venta_id