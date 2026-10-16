# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from tecnostock.dominio.apartados.apartado import ReglaNegocioExcepcion

class AlternativaDeNegocio(Enum):
    """Alternativas o acciones sugeridas al operador cuando falla una regla."""
    NINGUNA = "Ninguna"
    VERIFICAR_INVENTARIO_GLOBAL = "VerificarInventarioGlobal"
    SOLICITAR_TRANSFERENCIA = "SolicitarTransferencia"         # Exclusivo Equipo 5 (CU-06)
    REDUCIR_CANTIDAD_ARTICULOS = "ReducirCantidadArticulos"    # Regla: Límite de 5 artículos
    AUMENTAR_ANTICIPO = "AumentarAnticipo"                     # Regla: Mínimo 20%

@dataclass(frozen=True)
class DetalleDeFallo:
    """Encapsula el porqué falló una operación y qué se puede hacer."""
    mensaje_tecnico: str
    sugerencia: AlternativaDeNegocio = AlternativaDeNegocio.NINGUNA

@dataclass(frozen=True)
class ResultadoOperacion:
    """Patrón Result para evitar el uso excesivo de bloques try/catch en los controladores (API/UI)."""
    exitoso: bool
    valor: Any = None
    fallo: Optional[DetalleDeFallo] = None

    @staticmethod
    def exito(valor=None) -> "ResultadoOperacion":
        return ResultadoOperacion(True, valor, None)

    @staticmethod
    def rechazar(fallo: DetalleDeFallo) -> "ResultadoOperacion":
        return ResultadoOperacion(False, None, fallo)

class InterpretadorDeExcepciones:
    """
    Traduce las excepciones puras de Dominio en fallos amigables para la capa de Presentación.
    Exclusivo del Equipo 5: Mapea a opciones de transferencia o ajuste de apartados.
    """
    
    @staticmethod
    def interpretar(ex: ReglaNegocioExcepcion) -> DetalleDeFallo:
        mensaje = str(ex)
        sugerencia = AlternativaDeNegocio.NINGUNA

        # Análisis del mensaje de la regla de dominio violada
        if "Stock insuficiente" in mensaje or "Disponible:" in mensaje:
            sugerencia = AlternativaDeNegocio.SOLICITAR_TRANSFERENCIA
        elif "Límite de artículos" in mensaje or "Máximo permitido" in mensaje:
            sugerencia = AlternativaDeNegocio.REDUCIR_CANTIDAD_ARTICULOS
        elif "anticipo" in mensaje.lower() or "insuficiente" in mensaje:
            sugerencia = AlternativaDeNegocio.AUMENTAR_ANTICIPO

        return DetalleDeFallo(mensaje_tecnico=mensaje, sugerencia=sugerencia)