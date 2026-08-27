# Servicio de vehículos (lógica de negocio)
from typing import List, Optional, Tuple
from app.models.vehiculo import Vehiculo
from app.repositories.base_repository import BaseRepository
from app.validators.vehiculo_validator import VehiculoValidator

class VehiculoService:
    """Servicio que contiene la lógica de negocio para vehículos"""
    
    def __init__(self, repository: BaseRepository):
        """
        Inicializa el servicio con un repositorio específico
        
        Args:
            repository: Instancia de BaseRepository
        """
        self.repository = repository
        self._connected = False
    
    def connect(self) -> bool:
        """Conectar a la base de datos"""
        self._connected = self.repository.connect()
        return self._connected
    
    def disconnect(self) -> None:
        """Desconectar de la base de datos"""
        self.repository.disconnect()
        self._connected = False
    
    def is_connected(self) -> bool:
        """Verificar si hay conexión activa"""
        return self._connected and self.repository.is_connected()
    
    def registrar_vehiculo(self, placa: str, marca: str, modelo: str, 
                          anio: int, color: str) -> Tuple[bool, str]:
        """
        Registrar un nuevo vehículo
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        if not self.is_connected():
            return False, "No hay conexión a la base de datos"
        
        # Crear el vehículo
        vehiculo = Vehiculo(placa, marca, modelo, anio, color)
        
        # Validar datos
        errores = VehiculoValidator.validar_vehiculo(vehiculo)
        if errores:
            return False, "\n".join(errores)
        
        # Verificar si la placa ya existe
        if self.repository.exists(placa):
            return False, f"Ya existe un vehículo con la placa: {placa}"
        
        # Guardar vehículo
        if self.repository.save(vehiculo):
            return True, f"Vehículo {placa} registrado exitosamente"
        else:
            return False, "Error al registrar el vehículo en la base de datos"
    
    def consultar_vehiculo(self, placa: str) -> Tuple[Optional[Vehiculo], str]:
        """
        Consultar un vehículo por su placa
        
        Returns:
            Tuple[Optional[Vehiculo], str]: (vehículo, mensaje)
        """
        if not self.is_connected():
            return None, "No hay conexión a la base de datos"
        
        if not VehiculoValidator.validar_placa(placa):
            return None, "La placa es obligatoria"
        
        vehiculo = self.repository.find_by_plate(placa)
        if vehiculo:
            return vehiculo, f"Vehículo {placa} encontrado"
        else:
            return None, f"No se encontró el vehículo con placa: {placa}"
    
    def listar_vehiculos(self) -> Tuple[List[Vehiculo], str]:
        """
        Listar todos los vehículos
        
        Returns:
            Tuple[List[Vehiculo], str]: (lista de vehículos, mensaje)
        """
        if not self.is_connected():
            return [], "No hay conexión a la base de datos"
        
        vehiculos = self.repository.find_all()
        if vehiculos:
            return vehiculos, f"Se encontraron {len(vehiculos)} vehículos"
        else:
            return [], "No hay vehículos registrados"
    
    def actualizar_vehiculo(self, placa: str, marca: str, modelo: str, 
                           anio: int, color: str) -> Tuple[bool, str]:
        """
        Actualizar un vehículo existente
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        if not self.is_connected():
            return False, "No hay conexión a la base de datos"
        
        # Crear el vehículo con los nuevos datos
        vehiculo = Vehiculo(placa, marca, modelo, anio, color)
        
        # Validar datos
        errores = VehiculoValidator.validar_vehiculo(vehiculo)
        if errores:
            return False, "\n".join(errores)
        
        # Verificar si el vehículo existe
        if not self.repository.exists(placa):
            return False, f"No existe un vehículo con la placa: {placa}"
        
        # Actualizar vehículo
        if self.repository.update(vehiculo):
            return True, f"Vehículo {placa} actualizado exitosamente"
        else:
            return False, "Error al actualizar el vehículo en la base de datos"
    
    def eliminar_vehiculo(self, placa: str) -> Tuple[bool, str]:
        """
        Eliminar un vehículo por su placa
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        if not self.is_connected():
            return False, "No hay conexión a la base de datos"
        
        if not VehiculoValidator.validar_placa(placa):
            return False, "La placa es obligatoria"
        
        # Verificar si el vehículo existe
        if not self.repository.exists(placa):
            return False, f"No existe un vehículo con la placa: {placa}"
        
        # Eliminar vehículo
        if self.repository.delete(placa):
            return True, f"Vehículo {placa} eliminado exitosamente"
        else:
            return False, "Error al eliminar el vehículo de la base de datos"