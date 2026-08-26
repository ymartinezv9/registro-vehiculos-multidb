# Interfaz abstracta para repositorios
from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.vehiculo import Vehiculo

class BaseRepository(ABC):
    """Interfaz que deben implementar todos los repositorios"""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establecer conexión con la base de datos"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Cerrar conexión con la base de datos"""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """Verificar si hay conexión activa"""
        pass
    
    @abstractmethod
    def save(self, vehiculo: Vehiculo) -> bool:
        """Guardar un vehículo (insertar)"""
        pass
    
    @abstractmethod
    def find_by_plate(self, placa: str) -> Optional[Vehiculo]:
        """Buscar un vehículo por su placa"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Vehiculo]:
        """Obtener todos los vehículos"""
        pass
    
    @abstractmethod
    def update(self, vehiculo: Vehiculo) -> bool:
        """Actualizar un vehículo existente"""
        pass
    
    @abstractmethod
    def delete(self, placa: str) -> bool:
        """Eliminar un vehículo por su placa"""
        pass
    
    @abstractmethod
    def exists(self, placa: str) -> bool:
        """Verificar si existe un vehículo con esa placa"""
        pass