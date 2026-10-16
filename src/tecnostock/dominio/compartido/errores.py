# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from enum import Enum

class MotivoDeRechazo(Enum):
    """Catálogo exclusivo del Equipo 5 para los rechazos de negocio."""
    ANTICIPO_INSUFICIENTE = "ANTICIPO_INSUFICIENTE"
    LIMITE_ARTICULOS_EXCEDIDO = "LIMITE_ARTICULOS_EXCEDIDO"
    STOCK_INSUFICIENTE = "STOCK_INSUFICIENTE"
    APARTADO_VENCIDO = "APARTADO_VENCIDO"
    SUCURSAL_INVALIDA = "SUCURSAL_INVALIDA"


class ReglaDeNegocioViolada(Exception):
    """Excepción lanzada cuando una invariante de dominio es rota."""
    
    def __init__(self, motivo: MotivoDeRechazo, mensaje_de_negocio: str):
        super().__init__(mensaje_de_negocio)
        self.motivo = motivo
        self.mensaje_de_negocio = mensaje_de_negocio