# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional

# Importamos las entidades de dominio que los puertos van a manejar
from tecnostock.dominio.apartados.apartado import Apartado
from tecnostock.aplicacion.servicios.servicio_de_transferencias import RegistroTransferencia

# ====================================================================
# Puertos de Repositorios (Acceso a Datos)
# ====================================================================

class IRepositorioApartados(ABC):
    @abstractmethod
    def generar_id(self) -> str:
        pass

    @abstractmethod
    def guardar(self, apartado: Apartado) -> None:
        pass

    @abstractmethod
    def obtener_por_id(self, apartado_id: str) -> Optional[Apartado]:
        pass

    @abstractmethod
    def obtener_activos_por_cliente(self, cliente_id: str) -> List[Apartado]:
        pass


class IRepositorioInventario(ABC):
    """Puerto complejo que maneja los 3 estados del inventario: físico, reservado y en tránsito."""
    
    @abstractmethod
    def obtener_stock(self, sucursal_id: str, articulo_id: str) -> int:
        pass

    # Operaciones para Apartados (CU-04)
    @abstractmethod
    def bloquear_stock_reserva(self, sucursal_id: str, articulo_id: str, cantidad: int) -> None:
        pass

    @abstractmethod
    def liberar_stock_reserva(self, sucursal_id: str, articulo_id: str, cantidad: int) -> None:
        pass

    @abstractmethod
    def confirmar_salida_reserva(self, sucursal_id: str, articulo_id: str, cantidad: int) -> None:
        pass

    # Operaciones para Transferencias (CU-06 - Exclusivo Equipo 5)
    @abstractmethod
    def bloquear_stock_transito(self, sucursal_id: str, articulo_id: str, cantidad: int) -> None:
        pass

    @abstractmethod
    def desbloquear_stock_transito(self, sucursal_id: str, articulo_id: str, cantidad: int) -> None:
        pass

    @abstractmethod
    def descontar_stock(self, sucursal_id: str, articulo_id: str, cantidad: int) -> None:
        pass

    @abstractmethod
    def incrementar_stock(self, sucursal_id: str, articulo_id: str, cantidad: int) -> None:
        pass


class IRepositorioTransferencias(ABC):
    @abstractmethod
    def generar_id(self) -> str:
        pass

    @abstractmethod
    def guardar(self, transferencia: RegistroTransferencia) -> None:
        pass

    @abstractmethod
    def obtener_por_id(self, transferencia_id: str) -> Optional[RegistroTransferencia]:
        pass


# ====================================================================
# Puertos de Servicios Externos
# ====================================================================

class IMonederoDigital(ABC):
    @abstractmethod
    def abonar_saldo(self, cliente_id: str, monto: Decimal, concepto: str) -> None:
        pass


class IServicioNotificaciones(ABC):
    @abstractmethod
    def enviar_alerta_almacen(self, sucursal_id: str, mensaje: str) -> None:
        pass


# ====================================================================
# Puerto del Patrón Unit of Work
# ====================================================================

class IUnidadDeTrabajo(ABC):
    """
    Abstracción de la transacción de base de datos.
    Agrupa los repositorios para garantizar atomicidad.
    """
    
    @property
    @abstractmethod
    def apartados(self) -> IRepositorioApartados:
        pass

    @property
    @abstractmethod
    def inventario(self) -> IRepositorioInventario:
        pass

    @property
    @abstractmethod
    def transferencias(self) -> IRepositorioTransferencias:
        pass

    @property
    @abstractmethod
    def monedero(self) -> IMonederoDigital:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

    @abstractmethod
    def __enter__(self) -> "IUnidadDeTrabajo":
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass