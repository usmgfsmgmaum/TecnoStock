# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from dataclasses import dataclass
from tecnostock.dominio.apartados.apartado import ReglaNegocioExcepcion

@dataclass
class UnidadInventario:
    """
    Entidad de Dominio que modela la existencia de un artículo 
    dentro de una sucursal específica de TecnoStock.
    """
    sucursal_id: str
    articulo_id: str
    stock_disponible: int
    stock_reservado: int = 0
    stock_transito: int = 0

    def __post_init__(self):
        if self.stock_disponible < 0 or self.stock_reservado < 0 or self.stock_transito < 0:
            raise ReglaNegocioExcepcion("Las cantidades de inventario no pueden ser negativas.")

    @property
    def stock_total_fisico(self) -> int:
        """Stock físico real en el almacén de la sucursal."""
        return self.stock_disponible + self.stock_reservado

    def bloquear_para_reserva(self, cantidad: int) -> None:
        """Mueve stock disponible a stock reservado (usado al crear apartados)."""
        if self.stock_disponible < cantidad:
            raise ReglaNegocioExcepcion(
                f"Stock insuficiente para reservar. Disponible: {self.stock_disponible}, solicitado: {cantidad}"
            )
        self.stock_disponible -= cantidad
        self.stock_reservado += cantidad

    def liberar_reserva(self, cantidad: int) -> None:
        """Regresa el stock reservado a disponible (si el apartado vence o se cancela)."""
        if self.stock_reservado < cantidad:
            raise ReglaNegocioExcepcion("No se puede liberar más stock del que se encuentra reservado.")
        self.stock_reservado -= cantidad
        self.stock_disponible += cantidad

    def confirmar_salida_reserva(self, cantidad: int) -> None:
        """Descuenta definitivamente el stock reservado (cuando el apartado se liquida o vende)."""
        if self.stock_reservado < cantidad:
            raise ReglaNegocioExcepcion("Error de consistencia: Intentando liquidar más stock reservado del existente.")
        self.stock_reservado -= cantidad

    def bloquear_para_transito(self, cantidad: int) -> None:
        """Retiene stock disponible para enviarlo a otra sucursal (CU-06)."""
        if self.stock_disponible < cantidad:
            raise ReglaNegocioExcepcion(
                f"Stock insuficiente para transferir. Disponible: {self.stock_disponible}"
            )
        self.stock_disponible -= cantidad
        self.stock_transito += cantidad

    def desbloquear_transito(self, cantidad: int) -> None:
        """Regresa el stock a disponible si una transferencia es rechazada."""
        if self.stock_transito < cantidad:
            raise ReglaNegocioExcepcion("No se puede liberar más stock en tránsito del registrado.")
        self.stock_transito -= cantidad
        self.stock_disponible += cantidad

    def descontar_definitivo(self, cantidad: int) -> None:
        """Descuenta stock por venta directa o salida de almacén."""
        if self.stock_disponible < cantidad:
            raise ReglaNegocioExcepcion(f"Stock insuficiente para venta. Disponible: {self.stock_disponible}")
        self.stock_disponible -= cantidad

    def incrementar(self, cantidad: int) -> None:
        """Incrementa el stock disponible (recepción de compras o llegada de transferencias)."""
        if cantidad <= 0:
            raise ReglaNegocioExcepcion("La cantidad a incrementar debe ser mayor a cero.")
        self.stock_disponible += cantidad