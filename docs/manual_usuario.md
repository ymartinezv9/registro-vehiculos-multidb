# Manual de Usuario
## Sistema de Registro de Vehículos - MultiBD

### Introducción

Aplicación de escritorio para administrar vehículos en MySQL, SQL Server y Oracle.

### Requisitos

- Windows, Linux o macOS
- Python 3.8 o superior
- Acceso a la base de datos que desees usar

### Instalación

```bash
# 1. Clonar
git clone https://github.com/ymartinezv9/registro-vehiculos-multidb.git
cd registro-vehiculos-multidb
```
### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate 
```
 Windows
```bash
source venv/bin/activate  # Linux/Mac
```
### 3. Instalar dependencias
``` bash
pip install -r requirements.txt
```
### 4. Configurar .env

```bash
cp .env.example .env
```
Editar ```.env``` con tus credenciales

# 5. Ejecutar
python run.py