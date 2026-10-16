# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

# ====================================================================
# DTOs (Data Transfer Objects) - Modelos de Lectura Planos
# ====================================================================

@dataclass(frozen=True)
class FichaDisponibilidadDTO:
    """DTO para mostrar el stock al vendedor sin cargar los Aggregates completos."""
    articulo_id: str
    sucursal_id: str
    nombre_articulo: str
    stock_fisico_total: int
    stock_retenido_por_apartados: int
    stock_en_transito: int

    @property
    def stock_real_vendible(self) -> int:
        """Regla de Negocio (Lectura): El stock vendible excluye la mercancía apartada."""
        return self.stock_fisico_total - self.stock_retenido_por_apartados

@dataclass(frozen=True)
class EstadoTransferenciaDTO:
    """DTO exclusivo del Equipo 5 para auditar movimientos entre sucursales."""
    transferencia_id: str
    sucursal_origen: str
    sucursal_destino: str
    estado_actual: str
    fecha_solicitud: datetime
    solicitante_id: str


# ====================================================================
# Puertos (Interfaces) para la Infraestructura de Lectura
# ====================================================================

class ProveedorLecturaInventario(ABC):
    """Puerto que la BD deberá implementar para hacer queries directas (rápidas)."""
    
    @abstractmethod
    def buscar_disponibilidad_local(self, articulo_id: str, sucursal_id: str) -> Optional[FichaDisponibilidadDTO]:
        pass

    @abstractmethod
    def buscar_disponibilidad_global(self, articulo_id: str) -> List[FichaDisponibilidadDTO]:
        pass


class ProveedorLecturaTransferencias(ABC):
    """Puerto para consultar el estatus de las transferencias (CU-06)."""
    
    @abstractmethod
    def obtener_historial_por_sucursal(self, sucursal_id: str) -> List[EstadoTransferenciaDTO]:
        pass


# ====================================================================
# Servicios de Consulta (Query Services)
# ====================================================================

class ServicioConsultasInventario:
    """Servicio que maneja el CU-01: Consulta de disponibilidad global y local."""
    
    def __init__(self, proveedor_lectura: ProveedorLecturaInventario):
        self._proveedor_lectura = proveedor_lectura

    def consultar_stock_en_sucursal(self, articulo_id: str, sucursal_id: str) -> Optional[FichaDisponibilidadDTO]:
        # Retorna datos crudos para la pantalla del Vendedor
        return self._proveedor_lectura.buscar_disponibilidad_local(articulo_id, sucursal_id)

    def consultar_stock_toda_la_cadena(self, articulo_id: str) -> List[FichaDisponibilidadDTO]:
        # US-01, US-02: Consulta multitienda rápida sin bloqueos
        return self._proveedor_lectura.buscar_disponibilidad_global(articulo_id)


class ServicioConsultasTransferencias:
    """Complemento para el CU-06: Permite a Supervisor y Almacén monitorear envíos."""
    
    def __init__(self, proveedor_lectura: ProveedorLecturaTransferencias):
        self._proveedor_lectura = proveedor_lectura

    def ver_transferencias_activas_en_sucursal(self, sucursal_id: str) -> List[EstadoTransferenciaDTO]:
        # Filtra las transferencias para mostrar solo las que están en proceso
        todas = self._proveedor_lectura.obtener_historial_por_sucursal(sucursal_id)
        return [t for t in todas if t.estado_actual not in ("COMPLETADA", "RECHAZADA")]