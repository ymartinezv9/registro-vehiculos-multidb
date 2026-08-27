# Manual Técnico

## Sistema de Registro de Vehículos - MultiBD

### Tabla de Contenidos

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Tecnologías Utilizadas](#tecnologías-utilizadas)
4. [Configuración y Variables de Entorno](#configuración-y-variables-de-entorno)
5. [Descripción de Componentes](#descripción-de-componentes)
6. [Flujo de Datos](#flujo-de-datos)
7. [Extensiones y Mantenimiento](#extensiones-y-mantenimiento)
8. [Solución de Problemas](#solución-de-problemas)

---

## Arquitectura del Sistema

El sistema sigue una arquitectura en capas que separa las responsabilidades:

```text
┌─────────────────────────────────────────────────────────────┐
│ UI Layer (Tkinter)                                         │
│ app/ui/main_window.py                                      │
├─────────────────────────────────────────────────────────────┤
│ Service Layer                                               │
│ app/services/vehiculo_service.py                           │
├─────────────────────────────────────────────────────────────┤
│ Repository Layer                                             │
│ app/repositories/*.py                                      │
├─────────────────────────────────────────────────────────────┤
│ Database Layer                                               │
│ MySQL | SQL Server | Oracle                                │
└─────────────────────────────────────────────────────────────┘
```

### Patrones de Diseño

| Patrón     | Descripción                   | Ubicación                |
| ---------- | ----------------------------- | ------------------------ |
| Repository | Abstrae el acceso a datos     | `app/repositories/`      |
| Service    | Contiene la lógica de negocio | `app/services/`          |
| Factory    | Crea instancias según el tipo | `app/config/database.py` |
| DTO        | Transferencia de datos        | `app/models/vehiculo.py` |

---

## Estructura del Proyecto

```text
registro-vehiculos-multidb/
│
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   └── database.py              # Configuración y fábrica
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── vehiculo.py              # Modelo Vehículo
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base_repository.py       # Interfaz abstracta
│   │   ├── mysql_repository.py
│   │   ├── sqlserver_repository.py
│   │   └── oracle_repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── vehiculo_service.py      # Lógica de negocio
│   │
│   ├── validators/
│   │   ├── __init__.py
│   │   └── vehiculo_validator.py
│   │
│   └── ui/
│       ├── __init__.py
│       └── main_window.py           # Interfaz gráfica
│
├── database/                         # Scripts SQL
│   ├── mysql/
│   │   └── schema.sql
│   ├── sqlserver/
│   │   └── schema.sql
│   └── oracle/
│       └── schema.sql
│
├── docs/
│   ├── manual_usuario.md
│   └── manual_tecnico.md
│
├── tests/                            # Pruebas unitarias
│
├── .env                              # Variables de entorno (local)
├── .env.example                      # Ejemplo de variables
├── .gitignore
├── README.md
├── requirements.txt
└── run.py                            # Punto de entrada
```

---

## Tecnologías Utilizadas

| Tecnología             | Versión | Propósito                |
| ---------------------- | ------- | ------------------------ |
| Python                 | 3.8+    | Lenguaje de programación |
| Tkinter                | -       | Interfaz gráfica         |
| mysql-connector-python | 8.0.33  | Conector para MySQL      |
| pyodbc                 | 5.0.1   | Conector para SQL Server |
| oracledb               | 2.2.0   | Conector para Oracle     |
| python-dotenv          | 1.0.0   | Variables de entorno     |

---

## Configuración y Variables de Entorno

### Variables de Entorno

| Variable                       | Descripción              | Valor por Defecto               |
| ------------------------------ | ------------------------ | ------------------------------- |
| `MYSQL_HOST`                   | Host de MySQL            | `localhost`                     |
| `MYSQL_PORT`                   | Puerto MySQL             | `3306`                          |
| `MYSQL_DATABASE`               | Base de datos MySQL      | `vehiculos_db`                  |
| `MYSQL_USER`                   | Usuario MySQL            | `root`                          |
| `MYSQL_PASSWORD`               | Contraseña MySQL         | *(vacío)*                       |
| `SQLSERVER_SERVER`             | Servidor SQL Server      | `(localdb)\MSSQLLocalDB`        |
| `SQLSERVER_DATABASE`           | Base de datos SQL Server | `vehiculos_db`                  |
| `SQLSERVER_TRUSTED_CONNECTION` | Autenticación integrada  | `true`                          |
| `SQLSERVER_DRIVER`             | Driver ODBC              | `ODBC Driver 17 for SQL Server` |
| `ORACLE_HOST`                  | Host Oracle              | `localhost`                     |
| `ORACLE_PORT`                  | Puerto Oracle            | `1521`                          |
| `ORACLE_SERVICE_NAME`          | Servicio Oracle          | `XE`                            |
| `ORACLE_USER`                  | Usuario Oracle           | `system`                        |
| `ORACLE_PASSWORD`              | Contraseña Oracle        | *(vacío)*                       |

### Archivo `.env.example`

```env
# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=vehiculos_db
MYSQL_USER=root
MYSQL_PASSWORD=

# SQL Server
SQLSERVER_SERVER=(localdb)\MSSQLLocalDB
SQLSERVER_DATABASE=vehiculos_db
SQLSERVER_TRUSTED_CONNECTION=true
SQLSERVER_DRIVER=ODBC Driver 17 for SQL Server

# Oracle
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=XE
ORACLE_USER=system
ORACLE_PASSWORD=
```

> **Nota:** El archivo `.env` contiene información sensible y no debe incluirse en el repositorio. Debe estar incluido en `.gitignore`.

---

## Descripción de Componentes

### Configuración — `app/config/database.py`

**Responsabilidad:** Cargar variables de entorno y crear repositorios mediante una fábrica.

```python
class DatabaseConfig:
    @staticmethod
    def get_mysql_config():
        return {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'database': os.getenv('MYSQL_DATABASE', 'vehiculos_db'),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', '')
        }


class RepositoryFactory:
    _repositories = {
        'mysql': MySQLRepository,
        'sqlserver': SQLServerRepository,
        'oracle': OracleRepository
    }

    @classmethod
    def create(cls, db_type: str):
        repo_class = cls._repositories.get(db_type)

        if not repo_class:
            raise ValueError(f"Tipo no soportado: {db_type}")

        return repo_class()
```

---

### Modelo — `app/models/vehiculo.py`

**Responsabilidad:** Definir la estructura de datos del vehículo.

```python
@dataclass
class Vehiculo:
    placa: str
    marca: str
    modelo: str
    año: int
    color: str

    def to_dict(self) -> dict:
        return {
            'placa': self.placa,
            'marca': self.marca,
            'modelo': self.modelo,
            'año': self.año,
            'color': self.color
        }
```

---

### Validadores — `app/validators/vehiculo_validator.py`

**Responsabilidad:** Validar los datos antes de realizar operaciones CRUD.

```python
class VehiculoValidator:
    @staticmethod
    def validar_año(año) -> bool:
        try:
            año_int = int(año)
            año_actual = datetime.datetime.now().year

            return 1900 <= año_int <= año_actual

        except (ValueError, TypeError):
            return False

    @classmethod
    def validar_vehiculo(cls, vehiculo: Vehiculo) -> List[str]:
        errores = []

        if not cls.validar_placa(vehiculo.placa):
            errores.append("La placa es obligatoria")

        if not cls.validar_año(vehiculo.año):
            errores.append("El año debe ser entre 1900 y el actual")

        return errores
```

---

### Repositorios — `app/repositories/`

**Responsabilidad:** Proporcionar acceso a los datos mediante operaciones CRUD. Cada motor de base de datos tiene su propia implementación.

#### Interfaz Base

```python
class BaseRepository(ABC):

    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def save(self, vehiculo: Vehiculo) -> bool:
        pass

    @abstractmethod
    def find_by_plate(self, placa: str) -> Optional[Vehiculo]:
        pass

    @abstractmethod
    def find_all(self) -> List[Vehiculo]:
        pass

    @abstractmethod
    def update(self, vehiculo: Vehiculo) -> bool:
        pass

    @abstractmethod
    def delete(self, placa: str) -> bool:
        pass

    @abstractmethod
    def exists(self, placa: str) -> bool:
        pass
```

#### Diferencias entre Motores

| Aspecto     | MySQL     | SQL Server | Oracle     |
| ----------- | --------- | ---------- | ---------- |
| Placeholder | `%s`      | `?`        | `:1`       |
| Tipo String | `VARCHAR` | `NVARCHAR` | `VARCHAR2` |
| Tipo Número | `INT`     | `INT`      | `NUMBER`   |
| Columna Año | `año`     | `año`      | `anio`     |

---

### Servicios — `app/services/vehiculo_service.py`

**Responsabilidad:** Contener la lógica de negocio y orquestar las operaciones entre la interfaz, los validadores y los repositorios.

```python
class VehiculoService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def registrar_vehiculo(self, placa, marca, modelo, anio, color):
        if not self.is_connected():
            return False, "No hay conexión"

        vehiculo = Vehiculo(
            placa,
            marca,
            modelo,
            anio,
            color
        )

        errores = VehiculoValidator.validar_vehiculo(vehiculo)

        if errores:
            return False, "\n".join(errores)

        if self.repository.exists(placa):
            return False, f"Placa {placa} ya existe"

        if self.repository.save(vehiculo):
            return True, f"Vehículo {placa} registrado"

        return False, "Error al registrar"
```

---

### UI — `app/ui/main_window.py`

**Responsabilidad:** Proporcionar la interfaz gráfica y manejar los eventos generados por el usuario.

```python
class MainWindow:
    def __init__(self, root):
        self.root = root
        self.db_type = tk.StringVar(value="mysql")
        self.service = None
        self._crear_widgets()

    def _registrar(self):
        if not self._verificar_conexion():
            return

        placa = self.entries['entry_placa'].get().strip().upper()
        marca = self.entries['entry_marca'].get().strip()
        modelo = self.entries['entry_modelo'].get().strip()
        anio = int(self.entries['entry_anio'].get().strip())
        color = self.entries['entry_color'].get().strip()

        success, message = self.service.registrar_vehiculo(
            placa,
            marca,
            modelo,
            anio,
            color
        )

        if success:
            messagebox.showinfo("Éxito", message)
            self._limpiar_campos()
            self._listar()
        else:
            messagebox.showerror("Error", message)
```

---

## Flujo de Datos

### Diagrama de Secuencia — Registro

```text
Usuario → UI → Service → Repository → Database
  │        │       │           │           │
  │        │       │           │           │
  │        │       │           │           │
  │        │       │           │           │
  1. Ingresa datos
  2. Hace clic en Registrar
  3. La UI obtiene los datos del formulario
  4. La UI llama a registrar_vehiculo()
  5. El Service valida los datos
  6. El Service verifica duplicados
  7. El Repository guarda los datos en la BD
  8. El resultado es retornado
  9. La UI muestra el mensaje y actualiza la tabla
```

### Métodos del Servicio

| Método                  | Descripción                     | Retorna                 |
| ----------------------- | ------------------------------- | ----------------------- |
| `registrar_vehiculo()`  | Crear nuevo vehículo            | `(bool, str)`           |
| `consultar_vehiculo()`  | Buscar por placa                | `(Vehiculo, str)`       |
| `listar_vehiculos()`    | Obtener todos los vehículos     | `(List[Vehiculo], str)` |
| `actualizar_vehiculo()` | Modificar un vehículo existente | `(bool, str)`           |
| `eliminar_vehiculo()`   | Eliminar por placa              | `(bool, str)`           |

---

## Extensiones y Mantenimiento

### Agregar una Nueva Base de Datos

#### 1. Crear el repositorio

Crear el archivo:

`app/repositories/postgresql_repository.py`

```python
from app.repositories.base_repository import BaseRepository


class PostgreSQLRepository(BaseRepository):

    def __init__(self):
        self.config = DatabaseConfig.get_postgresql_config()

    def connect(self) -> bool:
        # Implementar conexión
        pass

    def save(self, vehiculo: Vehiculo) -> bool:
        # Implementar INSERT
        pass

    # Implementar todos los métodos abstractos...
```

#### 2. Registrar el repositorio en la fábrica

Modificar `app/config/database.py`:

```python
class RepositoryFactory:
    _repositories = {
        'mysql': MySQLRepository,
        'sqlserver': SQLServerRepository,
        'oracle': OracleRepository,
        'postgresql': PostgreSQLRepository
    }
```

#### 3. Agregar la configuración

Agregar las siguientes variables al archivo `.env`:

```env
# PostgreSQL
POSTGRESQL_HOST=localhost
POSTGRESQL_DATABASE=vehiculos_db
POSTGRESQL_USER=postgres
POSTGRESQL_PASSWORD=
```

#### 4. Crear el script SQL

Crear:

`database/postgresql/schema.sql`

```sql
CREATE TABLE vehiculos (
    placa VARCHAR(10) PRIMARY KEY,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    año INTEGER NOT NULL,
    color VARCHAR(30) NOT NULL
);
```

---

## Solución de Problemas

| Error                                                  | Causa                               | Solución                                   |
| ------------------------------------------------------ | ----------------------------------- | ------------------------------------------ |
| `ModuleNotFoundError: No module named 'pkg_resources'` | Falta `setuptools`                  | Ejecutar `pip install setuptools`          |
| `ORA-00942: table or view does not exist`              | Tabla no creada                     | Ejecutar el script SQL correspondiente     |
| `Encryption not supported on SQL Server`               | Configuración de cifrado en LocalDB | Eliminar las opciones de `Encrypt`         |
| `Access denied for user`                               | Credenciales incorrectas            | Verificar las variables del archivo `.env` |

---

## Contacto

* **GitHub:** https://github.com/ymartinezv9
