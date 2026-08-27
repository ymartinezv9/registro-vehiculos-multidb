# Registro de Vehículos - Múltiples Bases de Datos

## Descripción

Aplicación de escritorio para la gestión de vehículos que soporta tres motores de base de datos diferentes: **MySQL**, **SQL Server** y **Oracle**. Desarrollada con **Python** y **Tkinter**, siguiendo los principios de arquitectura limpia y patrones de diseño para garantizar escalabilidad y mantenibilidad.

## Características

- **Multi-SGBD**: Conexión dinámica a MySQL, SQL Server y Oracle
- **CRUD Completo**: Crear, Leer, Actualizar y Eliminar vehículos
- **Validaciones**: Validación de datos antes de almacenar
- **Prevención de Duplicados**: Evita registros duplicados por placa
- **Interfaz Intuitiva**: Diseño limpio con Tkinter
- **Arquitectura Escalable**: Patrón Repository + Service
- **Cambio Dinámico**: Selecciona la base de datos en tiempo de ejecución

## Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.8+ | Lenguaje de programación |
| Tkinter | - | Interfaz gráfica |
| MySQL Connector | 8.0.33 | Conector para MySQL |
| PyODBC | 5.0.1 | Conector para SQL Server |
| Python-Oracledb | 2.2.0 | Conector para Oracle |
| Python-Dotenv | 1.0.0 | Variables de entorno |

## Estructura del Proyecto

```text
registro-vehiculos-multidb/
│
├── app/                                  # Código fuente principal
│   ├── config/                           # Configuración de la aplicación
│   │   ├── __init__.py
│   │   └── database.py                   # Configuración de BD y fábrica de repositorios
│   │
│   ├── models/                           # Modelos de datos (DTO)
│   │   ├── __init__.py
│   │   └── vehiculo.py                   # Modelo Vehículo
│   │
│   ├── repositories/                     # Capa de acceso a datos
│   │   ├── __init__.py
│   │   ├── base_repository.py            # Interfaz abstracta
│   │   ├── mysql_repository.py           # Implementación MySQL
│   │   ├── sqlserver_repository.py       # Implementación SQL Server
│   │   └── oracle_repository.py          # Implementación Oracle
│   │
│   ├── services/                         # Capa de lógica de negocio
│   │   ├── __init__.py
│   │   └── vehiculo_service.py           # Servicio de vehículos
│   │
│   ├── validators/                       # Validaciones de datos
│   │   ├── __init__.py
│   │   └── vehiculo_validator.py         # Validador de vehículos
│   │
│   └── ui/                               # Interfaz de usuario
│       ├── __init__.py
│       └── main_window.py                # Ventana principal Tkinter
│
├── database/                             # Scripts SQL por base de datos
│   ├── mysql/
│   │   └── schema.sql                    # Esquema MySQL
│   ├── sqlserver/
│   │   └── schema.sql                    # Esquema SQL Server
│   └── oracle/
│       └── schema.sql                    # Esquema Oracle
│
├── docs/                                 # Documentación
│   ├── manual_usuario.md
│   └── manual_tecnico.md
│
├── tests/                                # Pruebas unitarias
│   ├── __init__.py
│   ├── test_repositories.py
│   └── test_services.py
│
├── .env                                  # Variables de entorno (local, no subir)
├── .env.example                          # Ejemplo de variables de entorno
├── .gitignore                            # Archivos ignorados por Git
├── README.md                             # Este archivo
├── requirements.txt                      # Dependencias del proyecto
└── run.py                                # Punto de entrada de la aplicación
```


## Instalación y Configuración

```bash
# 1. Clonar
git clone https://github.com/ymartinezv9/registro-vehiculos-multidb.git
cd registro-vehiculos-multidb

# 2. Entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar .env
cp .env.example .env
# Editar .env con tus credenciales

# 5. Crear tablas en cada BD
# Ejecutar scripts en database/[motor]/schema.sql

# 6. Ejecutar
python run.py
```
## Uso Básico

1. **Conectar:** Selecciona el motor y haz clic en "Conectar".
2. **Registrar:** Completa el formulario y haz clic en "Registrar".
3. **Consultar:** Ingresa la placa y haz clic en "Consultar".
4. **Actualizar:** Modifica los datos y haz clic en "Actualizar".
5. **Eliminar:** Selecciona el vehículo y haz clic en "Eliminar".
6. **Listar:** Haz clic en "Listar Todos" para ver todos los registros.

## Agregar Nueva Base de Datos

1. Crear el repositorio en `app/repositories/`.
2. Implementar `BaseRepository`.
3. Registrar el repositorio en `RepositoryFactory` en `app/config/database.py`.
4. Agregar la configuración correspondiente en `.env`.
5. Crear el script SQL en `database/[nueva_bd]/schema.sql`.

## Documentación

- [Manual de Usuario](docs/manual_usuario.md)
- [Manual Técnico](docs/manual_tecnico.md)

## Autores

- **Lutwing Martinez** - Desarrollador Principal