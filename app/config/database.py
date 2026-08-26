# Configuración de la base de datos
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env.local
load_dotenv('.env.local')

class DatabaseConfig:
    """Configuración de conexión a bases de datos"""
    
    @staticmethod
    def get_mysql_config():
        """Obtener configuración de MySQL"""
        return {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'database': os.getenv('MYSQL_DATABASE', 'vehiculos_db'),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', '')
        }
    
    @staticmethod
    def get_sqlserver_config():
        """Obtener configuración de SQL Server"""
        return {
            'server': os.getenv('SQLSERVER_HOST', 'localhost'),
            'database': os.getenv('SQLSERVER_DATABASE', 'vehiculos_db'),
            'user': os.getenv('SQLSERVER_USER', 'sa'),
            'password': os.getenv('SQLSERVER_PASSWORD', ''),
            'driver': os.getenv('SQLSERVER_DRIVER', 'ODBC Driver 17 for SQL Server')
        }
    
    @staticmethod
    def get_oracle_config():
        """Obtener configuración de Oracle"""
        return {
            'host': os.getenv('ORACLE_HOST', 'localhost'),
            'port': int(os.getenv('ORACLE_PORT', 1521)),
            'service_name': os.getenv('ORACLE_SERVICE_NAME', 'XE'),
            'user': os.getenv('ORACLE_USER', 'system'),
            'password': os.getenv('ORACLE_PASSWORD', '')
        }