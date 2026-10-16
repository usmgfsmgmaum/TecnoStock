# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from typing import List

class RaizDeAgregado:
    """Clase base para todos los Aggregate Roots que emiten eventos de dominio."""
    
    def __init__(self):
        self._eventos_pendientes: List = []

    def _registrar(self, evento) -> None:
        self._eventos_pendientes.append(evento)

    def recoger_eventos(self) -> List:
        eventos = list(self._eventos_pendientes)
        self._eventos_pendientes.clear()
        return eventos