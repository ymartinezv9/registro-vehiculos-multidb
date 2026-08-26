# Modelo Vehículo (DTO - Data Transfer Object)
from dataclasses import dataclass

@dataclass
class Vehiculo:
    """Modelo que representa un vehículo"""
    placa: str
    marca: str
    modelo: str
    año: int
    color: str
    
    def to_dict(self) -> dict:
        """Convertir a diccionario"""
        return {
            'placa': self.placa,
            'marca': self.marca,
            'modelo': self.modelo,
            'año': self.año,
            'color': self.color
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Vehiculo':
        """Crear desde diccionario"""
        return cls(
            placa=data['placa'],
            marca=data['marca'],
            modelo=data['modelo'],
            año=data['año'],
            color=data['color']
        )
    
    def __str__(self) -> str:
        return f"{self.placa} - {self.marca} {self.modelo} ({self.año})"