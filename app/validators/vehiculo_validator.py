# Validaciones para vehículos
import datetime
from typing import List
from app.models.vehiculo import Vehiculo

class VehiculoValidator:
    """Clase para validar datos de vehículos"""
    
    @staticmethod
    def validar_placa(placa: str) -> bool:
        """Validar que la placa no esté vacía"""
        return placa and placa.strip() != ""
    
    @staticmethod
    def validar_marca(marca: str) -> bool:
        """Validar que la marca no esté vacía"""
        return marca and marca.strip() != ""
    
    @staticmethod
    def validar_modelo(modelo: str) -> bool:
        """Validar que el modelo no esté vacío"""
        return modelo and modelo.strip() != ""
    
    @staticmethod
    def validar_año(año) -> bool:
        """Validar que el año sea un número entre 1900 y el año actual"""
        try:
            año_int = int(año)
            año_actual = datetime.datetime.now().year
            return 1900 <= año_int <= año_actual
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validar_color(color: str) -> bool:
        """Validar que el color no esté vacío"""
        return color and color.strip() != ""
    
    @classmethod
    def validar_vehiculo(cls, vehiculo: Vehiculo) -> List[str]:
        """
        Validar todos los campos de un vehículo
        
        Returns:
            List[str]: Lista de errores encontrados (vacía si todo es válido)
        """
        errores = []
        
        if not cls.validar_placa(vehiculo.placa):
            errores.append("La placa es obligatoria")
        
        if not cls.validar_marca(vehiculo.marca):
            errores.append("La marca es obligatoria")
        
        if not cls.validar_modelo(vehiculo.modelo):
            errores.append("El modelo es obligatorio")
        
        if not cls.validar_año(vehiculo.año):
            errores.append("El año debe ser un número entre 1900 y el año actual")
        
        if not cls.validar_color(vehiculo.color):
            errores.append("El color es obligatorio")
        
        return errores