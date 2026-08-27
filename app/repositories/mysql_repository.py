# Implementación para MySQL
from typing import List, Optional
import mysql.connector
from mysql.connector import Error

from app.repositories.base_repository import BaseRepository
from app.models.vehiculo import Vehiculo
from app.config.database import DatabaseConfig

class MySQLRepository(BaseRepository):
    """Repositorio para MySQL"""
    
    def __init__(self):
        self.config = DatabaseConfig.get_mysql_config()
        self.connection = None
        self.cursor = None
        self._connected = False
    
    def connect(self) -> bool:
        """Establecer conexión con MySQL"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
            self._connected = True
            return True
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            self._connected = False
            return False
    
    def disconnect(self) -> None:
        """Cerrar conexión"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self._connected = False
    
    def is_connected(self) -> bool:
        return self._connected and self.connection is not None
    
    def save(self, vehiculo: Vehiculo) -> bool:
        """Guardar un vehículo"""
        if not self.is_connected():
            return False
        
        query = """INSERT INTO vehiculos (placa, marca, modelo, año, color) 
                   VALUES (%s, %s, %s, %s, %s)"""
        values = (vehiculo.placa, vehiculo.marca, vehiculo.modelo, 
                  vehiculo.año, vehiculo.color)
        
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error al insertar en MySQL: {e}")
            return False
    
    def find_by_plate(self, placa: str) -> Optional[Vehiculo]:
        """Buscar un vehículo por placa"""
        if not self.is_connected():
            return None
        
        query = "SELECT placa, marca, modelo, año, color FROM vehiculos WHERE placa = %s"
        
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
        except Error as e:
            print(f"Error al consultar en MySQL: {e}")
            return None
    
    def find_all(self) -> List[Vehiculo]:
        """Obtener todos los vehículos"""
        if not self.is_connected():
            return []
        
        query = "SELECT placa, marca, modelo, año, color FROM vehiculos ORDER BY placa"
        
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
        except Error as e:
            print(f"Error al consultar en MySQL: {e}")
            return []
    
    def update(self, vehiculo: Vehiculo) -> bool:
        """Actualizar un vehículo"""
        if not self.is_connected():
            return False
        
        query = """UPDATE vehiculos 
                   SET marca = %s, modelo = %s, año = %s, color = %s 
                   WHERE placa = %s"""
        values = (vehiculo.marca, vehiculo.modelo, vehiculo.año, 
                  vehiculo.color, vehiculo.placa)
        
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error al actualizar en MySQL: {e}")
            return False
    
    def delete(self, placa: str) -> bool:
        """Eliminar un vehículo"""
        if not self.is_connected():
            return False
        
        query = "DELETE FROM vehiculos WHERE placa = %s"
        
        try:
            self.cursor.execute(query, (placa,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error al eliminar en MySQL: {e}")
            return False
    
    def exists(self, placa: str) -> bool:
        """Verificar si existe un vehículo con esa placa"""
        if not self.is_connected():
            return False
        
        query = "SELECT COUNT(*) FROM vehiculos WHERE placa = %s"
        
        try:
            self.cursor.execute(query, (placa,))
            count = self.cursor.fetchone()[0]
            return count > 0
        except Error as e:
            print(f"Error al verificar existencia en MySQL: {e}")
            return False