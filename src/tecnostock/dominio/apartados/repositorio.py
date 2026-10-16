# ==========================================
# Autores: Equipo 5 (Noguera, Pérez, Paez)
# Proyecto: TecnoStock (Caso 05)
# ==========================================

from abc import ABC, abstractmethod
from typing import List, Optional
from tecnostock.dominio.apartados.apartado import Apartado

class IRepositorioApartados(ABC):
    """
    Contrato (Interface) del repositorio de Apartados.
    La implementación de Base de Datos irá en Infraestructura.
    """
    
    @abstractmethod
    def generar_id(self) -> str:
        """Genera un identificador único para un nuevo apartado."""
        pass

    @abstractmethod
    def guardar(self, apartado: Apartado) -> None:
        """Inserta o actualiza el agregado Apartado en la base de datos."""
        pass

    @abstractmethod
    def obtener_por_id(self, apartado_id: str) -> Optional[Apartado]:
        """Recupera un Apartado por su ID. Retorna None si no existe."""
        pass

    @abstractmethod
    def obtener_activos_por_cliente(self, cliente_id: str) -> List[Apartado]:
        """
        Recupera todos los apartados PENDIENTES de un cliente.
        Esencial para validar el límite de 5 artículos del negocio (CU-04).
        """
        pass