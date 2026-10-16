# ==========================================

# Autores: Equipo 5 (Noguera, Pérez, Paez)

# Proyecto: TecnoStock (Caso 05)

# ==========================================

import logging

from typing import Optional

from tecnostock.dominio.apartados.apartado import Apartado, ReglaNegocioExcepcion

from tecnostock.aplicacion.comandos import PeticionCrearApartado, PeticionLiquidarApartado

logger = logging.getLogger(__name__)


class ServicioDeApartados:

    def __init__(self, unidad_trabajo_factory):

        self.unidad_trabajo_factory = unidad_trabajo_factory

    def crear_apartado(self, peticion: PeticionCrearApartado) -> str:

        logger.info(f"Iniciando creación de apartado para cliente: {peticion.cliente_id}")

        

        with self.unidad_trabajo_factory() as unidad_trabajo:

            # Verificar apartados activos concurrentes del cliente

            apartados_activos = unidad_trabajo.apartados.obtener_activos_por_cliente(peticion.cliente_id)

            total_items_activos = sum(

                sum(i.cantidad for i in a.items) for a in apartados_activos

            )

            

            total_nuevos_items = sum(i.cantidad for i in peticion.items)

            if (total_items_activos + total_nuevos_items) > Apartado.LIMITE_MAX_ARTICULOS:

                raise ReglaNegocioExcepcion(

                    f"El cliente ya tiene {total_items_activos} artículos en apartados activos. "

                    f"Superaría el límite global de {Apartado.LIMITE_MAX_ARTICULOS}."

                )

            nuevo_id = unidad_trabajo.apartados.generar_id()

            nuevo_apartado = Apartado(

                apartado_id=nuevo_id,

                cliente_id=peticion.cliente_id,

                sucursal_id=peticion.sucursal_id

            )

            for item in peticion.items:

                # Verificar stock disponible en la sucursal antes de apartar

                stock_disponible = unidad_trabajo.inventario.obtener_stock(

                    peticion.sucursal_id, item.articulo_id

                )

                if stock_disponible < item.cantidad:

                    raise ReglaNegocioExcepcion(

                        f"Stock insuficiente para artículo {item.articulo_id}. Disponible: {stock_disponible}"

                    )

                

                nuevo_apartado.agregar_item(item.articulo_id, item.cantidad, item.precio_unitario)

                unidad_trabajo.inventario.bloquear_stock_reserva(

                    peticion.sucursal_id, item.articulo_id, item.cantidad

                )

            nuevo_apartado.registrar_anticipo_inicial(peticion.monto_anticipo)

            

            unidad_trabajo.apartados.guardar(nuevo_apartado)

            unidad_trabajo.commit()

            

            logger.info(f"Apartado {nuevo_id} creado exitosamente.")

            return nuevo_id

    def liquidar_apartado(self, peticion: PeticionLiquidarApartado) -> None:

        logger.info(f"Procesando liquidación de apartado: {peticion.apartado_id}")

        

        with self.unidad_trabajo_factory() as unidad_trabajo:

            apartado = unidad_trabajo.apartados.obtener_por_id(peticion.apartado_id)

            if not apartado:

                raise ReglaNegocioExcepcion(f"Apartado {peticion.apartado_id} no encontrado.")

            apartado.liquidar(peticion.monto_pago)

            

            # Liberar la reserva del inventario y consolidar la venta

            for item in apartado.items:

                unidad_trabajo.inventario.confirmar_salida_reserva(

                    apartado.sucursal_id, item.articulo_id, item.cantidad

                )

            unidad_trabajo.apartados.guardar(apartado)

            unidad_trabajo.commit()

            logger.info(f"Apartado {peticion.apartado_id} liquidado y cerrado.")
