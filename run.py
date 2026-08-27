# Punto de entrada de la aplicación
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models import Vehiculo
from app.services import VehiculoService
from app.repositories import MySQLRepository, SQLServerRepository, OracleRepository
from app.config import DatabaseConfig

def probar_servicio(repo, nombre_bd):
    """Función para probar el servicio con un repositorio específico"""
    print(f"\n{'='*60}")
    print(f"Probando Servicio con {nombre_bd}")
    print('='*60)
    
    # Crear servicio
    service = VehiculoService(repo)
    
    # Conectar
    print("\nConectando...")
    if not service.connect():
        print("   Error de conexion")
        return
    
    print("   Conexion exitosa")
    
    # 1. Registrar vehículo
    print("\n1. Registrando vehiculo...")
    success, message = service.registrar_vehiculo("TEST001", "Toyota", "Corolla", 2020, "Rojo")
    print(f"   {message}")
    
    # 2. Listar todos
    print("\n2. Listando vehiculos...")
    vehiculos, message = service.listar_vehiculos()
    print(f"   {message}")
    for v in vehiculos[:3]:
        print(f"      - {v}")
    
    # 3. Consultar por placa
    print("\n3. Consultando vehiculo TEST001...")
    vehiculo, message = service.consultar_vehiculo("TEST001")
    print(f"   {message}")
    if vehiculo:
        print(f"      Datos: {vehiculo}")
    
    # 4. Actualizar vehículo
    print("\n4. Actualizando vehiculo...")
    success, message = service.actualizar_vehiculo("TEST001", "Toyota", "Camry", 2021, "Azul")
    print(f"   {message}")
    
    # 5. Verificar actualización
    print("\n5. Verificando actualizacion...")
    vehiculo, message = service.consultar_vehiculo("TEST001")
    if vehiculo:
        print(f"      Datos actualizados: {vehiculo}")
    
    # 6. Eliminar vehículo
    print("\n6. Eliminando vehiculo...")
    success, message = service.eliminar_vehiculo("TEST001")
    print(f"   {message}")
    
    # 7. Verificar eliminación
    print("\n7. Verificando eliminacion...")
    vehiculo, message = service.consultar_vehiculo("TEST001")
    print(f"   {message}")
    
    # Desconectar
    print("\nDesconectando...")
    service.disconnect()
    print("   Desconectado")


def main():
    print("Probando Capa de Servicios")
    print("="*60)
    
    # Probar con MySQL
    print("\n[1] Probando con MySQL")
    print("-" * 40)
    repo_mysql = MySQLRepository()
    probar_servicio(repo_mysql, "MySQL")
    
    # Probar con SQL Server
    print("\n[2] Probando con SQL Server")
    print("-" * 40)
    repo_sqlserver = SQLServerRepository()
    probar_servicio(repo_sqlserver, "SQL Server")
    
    # Probar con Oracle
    print("\n[3] Probando con Oracle")
    print("-" * 40)
    repo_oracle = OracleRepository()
    probar_servicio(repo_oracle, "Oracle")


if __name__ == "__main__":
    main()