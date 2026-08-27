# Implementacion para Oracle usando python-oracledb
from typing import List, Optional
import oracledb

from app.repositories.base_repository import BaseRepository
from app.models.vehiculo import Vehiculo
from app.config.database import DatabaseConfig

class OracleRepository(BaseRepository):
    """Repositorio para Oracle usando python-oracledb"""
    
    def __init__(self):
        self.config = DatabaseConfig.get_oracle_config()
        self.connection = None
        self.cursor = None
        self._connected = False
    
    def connect(self) -> bool:
        """Establecer conexion con Oracle"""
        try:
            self.connection = oracledb.connect(
                user=self.config['user'],
                password=self.config['password'],
                host=self.config['host'],
                port=self.config['port'],
                service_name=self.config['service_name']
            )
            self.cursor = self.connection.cursor()
            self._connected = True
            return True
        except Exception as e:
            print(f"Error al conectar a Oracle: {e}")
            self._connected = False
            return False
    
    def disconnect(self) -> None:
        """Cerrar conexion"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self._connected = False
    
    def is_connected(self) -> bool:
        return self._connected and self.connection is not None
    
    def save(self, vehiculo: Vehiculo) -> bool:
        """Guardar un vehiculo"""
        if not self.is_connected():
            return False
        
        query = """INSERT INTO vehiculos (placa, marca, modelo, anio, color) 
                   VALUES (:1, :2, :3, :4, :5)"""
        values = (vehiculo.placa, vehiculo.marca, vehiculo.modelo, 
                  vehiculo.año, vehiculo.color)
        
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error al insertar en Oracle: {e}")
            return False
    
    def find_by_plate(self, placa: str) -> Optional[Vehiculo]:
        """Buscar un vehiculo por placa"""
        if not self.is_connected():
            return None
        
        query = "SELECT placa, marca, modelo, anio, color FROM vehiculos WHERE placa = :1"
        
        try:
            self.cursor.execute(query, (placa,))
            result = self.cursor.fetchone()
            if result:
                return Vehiculo(
                    placa=result[0],
                    marca=result[1],
                    modelo=result[2],
                    año=result[3],
                    color=result[4]
                )
            return None
        except Exception as e:
            print(f"Error al consultar en Oracle: {e}")
            return None
    
    def find_all(self) -> List[Vehiculo]:
        """Obtener todos los vehiculos"""
        if not self.is_connected():
            return []
        
        query = "SELECT placa, marca, modelo, anio, color FROM vehiculos ORDER BY placa"
        
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return [
                Vehiculo(
                    placa=r[0],
                    marca=r[1],
                    modelo=r[2],
                    año=r[3],
                    color=r[4]
                )
                for r in results
            ]
        except Exception as e:
            print(f"Error al consultar en Oracle: {e}")
            return []
    
    def update(self, vehiculo: Vehiculo) -> bool:
        """Actualizar un vehiculo"""
        if not self.is_connected():
            return False
        
        query = """UPDATE vehiculos 
                   SET marca = :1, modelo = :2, anio = :3, color = :4 
                   WHERE placa = :5"""
        values = (vehiculo.marca, vehiculo.modelo, vehiculo.año, 
                  vehiculo.color, vehiculo.placa)
        
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar en Oracle: {e}")
            return False
    
    def delete(self, placa: str) -> bool:
        """Eliminar un vehiculo"""
        if not self.is_connected():
            return False
        
        query = "DELETE FROM vehiculos WHERE placa = :1"
        
        try:
            self.cursor.execute(query, (placa,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar en Oracle: {e}")
            return False
    
    def exists(self, placa: str) -> bool:
        """Verificar si existe un vehiculo con esa placa"""
        if not self.is_connected():
            return False
        
        query = "SELECT COUNT(*) FROM vehiculos WHERE placa = :1"
        
        try:
            self.cursor.execute(query, (placa,))
            count = self.cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"Error al verificar existencia en Oracle: {e}")
            return False