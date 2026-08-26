# Punto de entrada de la aplicación
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models import Vehiculo
from app.validators import VehiculoValidator
from app.config import DatabaseConfig
from app.repositories import BaseRepository, MySQLRepository

def main():
    print("Probando MySQL Repository...")
    print("-" * 40)
    
    # 1. Mostrar configuración
    print("\nConfiguracion MySQL:")
    config = DatabaseConfig.get_mysql_config()
    # Ocultar contraseña por seguridad
    config_mostrar = config.copy()
    config_mostrar['password'] = '***' if config['password'] else '(vacia)'
    print(f"   {config_mostrar}")
    
    # 2. Crear repositorio
    repo = MySQLRepository()
    
    # 3. Probar conexión
    print("\nProbando conexion...")
    if repo.connect():
        print("   Conexion exitosa a MySQL")
    else:
        print("   Error de conexion a MySQL")
        print("\nVerifique:")
        print("   1. Que MySQL este ejecutandose")
        print("   2. Que las credenciales sean correctas en .env")
        print("   3. Que la base de datos 'vehiculos_db' exista")
        return
    
    # 4. Probar operaciones CRUD
    print("\nProbando operaciones CRUD...")
    
    # Crear vehículo de prueba
    vehiculo_test = Vehiculo("TEST001", "Toyota", "Corolla", 2020, "Rojo")
    print(f"\n   Vehiculo de prueba: {vehiculo_test}")
    
    # Guardar
    print("\n   Guardando vehiculo...")
    if repo.save(vehiculo_test):
        print("      Guardado exitoso")
    else:
        print("      Error al guardar")
    
    # Verificar existencia
    print("\n   Verificando existencia...")
    if repo.exists("TEST001"):
        print("      Vehiculo existe")
    else:
        print("      Vehiculo no encontrado")
    
    # Buscar por placa
    print("\n   Buscando por placa...")
    encontrado = repo.find_by_plate("TEST001")
    if encontrado:
        print(f"      Encontrado: {encontrado}")
    else:
        print("      No encontrado")
    
    # Listar todos
    print("\n   Listando todos los vehiculos...")
    todos = repo.find_all()
    print(f"      Total: {len(todos)} vehiculos")
    for v in todos[:3]:
        print(f"      - {v}")
    
    # Actualizar
    print("\n   Actualizando vehiculo...")
    vehiculo_actualizado = Vehiculo("TEST001", "Toyota", "Camry", 2021, "Azul")
    if repo.update(vehiculo_actualizado):
        print("      Actualizado exitosamente")
        actualizado = repo.find_by_plate("TEST001")
        if actualizado:
            print(f"      Nuevos datos: {actualizado}")
    else:
        print("      Error al actualizar")
    
    # Eliminar
    print("\n   Eliminando vehiculo...")
    if repo.delete("TEST001"):
        print("      Eliminado exitosamente")
        if not repo.exists("TEST001"):
            print("      Confirmado: vehiculo ya no existe")
    else:
        print("      Error al eliminar")
    
    # 5. Desconectar
    print("\nDesconectando...")
    repo.disconnect()
    print("   Desconectado")
    
    print("\nPrueba completada!")

if __name__ == "__main__":
    main()