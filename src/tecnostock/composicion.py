# ==========================================

# Autores: Equipo 5 (Noguera, Pérez, Paez)

# Proyecto: TecnoStock (Caso 05)

# ==========================================

from functools import lru_cache

import os

from tecnostock.aplicacion.servicios.servicio_de_apartados import ServicioDeApartados

from tecnostock.aplicacion.servicios.servicio_de_transferencias import ServicioDeTransferencias


class GestorBaseDatosSQLAlchemy:

    """Simulación del motor de persistencia y fábrica de sesiones."""

    def __init__(self, connection_string: str):

        self.connection_string = connection_string

    def crear_unidad_trabajo(self):

        # Devuelve un objeto UnidadDeTrabajo compatible con el context manager 'with'

        from tecnostock.infraestructura.unidad_de_trabajo import UnidadDeTrabajoSQLAlchemy

        return UnidadDeTrabajoSQLAlchemy(self)


class ContenedorInyeccion:

    """

    Contenedor de Inyección de Dependencias centralizado.

    NOTA: Se excluyen repositorios/servicios de Devoluciones por definición de alcance.

    """

    def __init__(self):

        db_uri = os.getenv("DATABASE_URL", "sqlite:///tecnostock.db")

        self.gestor_bd = GestorBaseDatosSQLAlchemy(db_uri)

    def fabricar_unidad_de_trabajo(self):

        return self.gestor_bd.crear_unidad_trabajo()

    def resolver_servicio_apartados(self) -> ServicioDeApartados:

        return ServicioDeApartados(

            unidad_trabajo_factory=self.fabricar_unidad_de_trabajo

        )

    def resolver_servicio_transferencias(self) -> ServicioDeTransferencias:

        """Exclusivo Equipo 5."""

        return ServicioDeTransferencias(

            unidad_trabajo_factory=self.fabricar_unidad_de_trabajo

        )


@lru_cache(maxsize=1)

def obtener_contenedor() -> ContenedorInyeccion:

    """Provee un singleton thread-safe del contenedor principal."""

    return ContenedorInyeccion()
