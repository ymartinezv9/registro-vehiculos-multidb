# Ventana principal de la aplicación
import tkinter as tk
from tkinter import ttk, messagebox

from app.config.database import DatabaseConfig
from app.repositories import MySQLRepository, SQLServerRepository, OracleRepository
from app.services import VehiculoService

class MainWindow:
    """Ventana principal de la aplicación"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Registro de Vehículos - MultiBD")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Estado de la aplicación
        self.db_type = tk.StringVar(value="mysql")
        self.service = None
        self.current_repo = None
        
        # Diccionario de repositorios disponibles
        self.repositories = {
            'mysql': MySQLRepository,
            'sqlserver': SQLServerRepository,
            'oracle': OracleRepository
        }
        
        self._crear_widgets()
        self._actualizar_estado_conexion(False)
    
    def _crear_widgets(self):
        """Crear todos los widgets de la interfaz"""
        
        # Frame de conexión
        frame_conexion = ttk.LabelFrame(self.root, text="Conexión", padding=10)
        frame_conexion.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_conexion, text="Base de Datos:").pack(side=tk.LEFT, padx=5)
        
        combo_bd = ttk.Combobox(
            frame_conexion,
            textvariable=self.db_type,
            values=list(self.repositories.keys()),
            state="readonly",
            width=15
        )
        combo_bd.pack(side=tk.LEFT, padx=5)
        
        btn_conectar = ttk.Button(
            frame_conexion,
            text="Conectar",
            command=self._conectar
        )
        btn_conectar.pack(side=tk.LEFT, padx=5)
        
        btn_desconectar = ttk.Button(
            frame_conexion,
            text="Desconectar",
            command=self._desconectar
        )
        btn_desconectar.pack(side=tk.LEFT, padx=5)
        
        self.lbl_estado = ttk.Label(
            frame_conexion,
            text="● Desconectado",
            foreground="red"
        )
        self.lbl_estado.pack(side=tk.LEFT, padx=20)
        
        # Frame del formulario
        frame_form = ttk.LabelFrame(self.root, text="Datos del Vehículo", padding=10)
        frame_form.pack(fill=tk.X, padx=10, pady=5)
        
        # Campos del formulario
        campos = [
            ("Placa (única):", "entry_placa", 15),
            ("Marca:", "entry_marca", 30),
            ("Modelo:", "entry_modelo", 30),
            ("Año:", "entry_anio", 10),
            ("Color:", "entry_color", 20)
        ]
        
        self.entries = {}
        
        for i, (label, key, width) in enumerate(campos):
            ttk.Label(frame_form, text=label).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = ttk.Entry(frame_form, width=width)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
            self.entries[key] = entry
        
        # Botones de acción
        frame_botones = ttk.Frame(frame_form)
        frame_botones.grid(row=len(campos), column=0, columnspan=2, pady=10)
        
        btn_registrar = ttk.Button(frame_botones, text="Registrar", command=self._registrar)
        btn_registrar.pack(side=tk.LEFT, padx=5)
        
        btn_consultar = ttk.Button(frame_botones, text="Consultar", command=self._consultar)
        btn_consultar.pack(side=tk.LEFT, padx=5)
        
        btn_actualizar = ttk.Button(frame_botones, text="Actualizar", command=self._actualizar)
        btn_actualizar.pack(side=tk.LEFT, padx=5)
        
        btn_eliminar = ttk.Button(frame_botones, text="Eliminar", command=self._eliminar)
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        btn_limpiar = ttk.Button(frame_botones, text="Limpiar", command=self._limpiar_campos)
        btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        btn_listar = ttk.Button(frame_botones, text="Listar Todos", command=self._listar)
        btn_listar.pack(side=tk.LEFT, padx=5)
        
        # Frame de la tabla
        frame_tabla = ttk.LabelFrame(self.root, text="Listado de Vehículos", padding=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("Placa", "Marca", "Modelo", "Año", "Color"),
            show="headings",
            height=10
        )
        
        self.tree.heading("Placa", text="Placa")
        self.tree.heading("Marca", text="Marca")
        self.tree.heading("Modelo", text="Modelo")
        self.tree.heading("Año", text="Año")
        self.tree.heading("Color", text="Color")
        
        self.tree.column("Placa", width=100)
        self.tree.column("Marca", width=150)
        self.tree.column("Modelo", width=150)
        self.tree.column("Año", width=80)
        self.tree.column("Color", width=100)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self._seleccionar_fila)
        
        # Botón recargar
        btn_recargar = ttk.Button(frame_tabla, text="Recargar Lista", command=self._listar)
        btn_recargar.pack(pady=5)
        
        # Frame de estado
        frame_status = ttk.Frame(self.root)
        frame_status.pack(fill=tk.X, padx=10, pady=5)
        
        self.lbl_status = ttk.Label(frame_status, text="Listo")
        self.lbl_status.pack(side=tk.LEFT)
    
    def _actualizar_estado_conexion(self, conectado: bool, db_type: str = ""):
        """Actualizar el estado de conexión en la interfaz"""
        if conectado:
            self.lbl_estado.config(text=f"● Conectado a {db_type}", foreground="green")
            self.lbl_status.config(text=f"Conectado a {db_type}")
        else:
            self.lbl_estado.config(text="● Desconectado", foreground="red")
            self.lbl_status.config(text="Desconectado")
    
    def _conectar(self):
        """Conectar a la base de datos seleccionada"""
        db_type = self.db_type.get()
        
        try:
            # Crear repositorio
            repo_class = self.repositories.get(db_type)
            if not repo_class:
                messagebox.showerror("Error", f"Tipo de base de datos no soportado: {db_type}")
                return
            
            repo = repo_class()
            self.current_repo = repo
            
            # Crear servicio
            self.service = VehiculoService(repo)
            
            # Conectar
            if self.service.connect():
                self._actualizar_estado_conexion(True, db_type)
                messagebox.showinfo("Éxito", f"Conexión exitosa a {db_type}")
                self._listar()
            else:
                self._actualizar_estado_conexion(False)
                messagebox.showerror(
                    "Error",
                    f"No se pudo conectar a {db_type}\n\n"
                    "Verifique que:\n"
                    "1. El servicio de base de datos esté ejecutándose\n"
                    "2. Las credenciales sean correctas\n"
                    "3. La base de datos exista"
                )
        except Exception as e:
            self._actualizar_estado_conexion(False)
            messagebox.showerror("Error", f"Error al conectar: {str(e)}")
    
    def _desconectar(self):
        """Desconectar de la base de datos"""
        if self.service and self.service.is_connected():
            self.service.disconnect()
            self._actualizar_estado_conexion(False)
            
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            messagebox.showinfo("Información", "Desconectado de la base de datos")
    
    def _verificar_conexion(self) -> bool:
        """Verificar si hay conexión activa"""
        if not self.service or not self.service.is_connected():
            messagebox.showwarning(
                "Advertencia",
                "Primero debe conectar a una base de datos\n"
                "Seleccione el tipo y haga clic en 'Conectar'"
            )
            return False
        return True
    
    def _registrar(self):
        """Registrar un nuevo vehículo"""
        if not self._verificar_conexion():
            return
        
        # Obtener datos
        placa = self.entries['entry_placa'].get().strip().upper()
        marca = self.entries['entry_marca'].get().strip()
        modelo = self.entries['entry_modelo'].get().strip()
        anio_str = self.entries['entry_anio'].get().strip()
        color = self.entries['entry_color'].get().strip()
        
        # Validar año
        try:
            anio = int(anio_str)
        except ValueError:
            messagebox.showerror("Error", "El año debe ser un número")
            return
        
        # Registrar
        success, message = self.service.registrar_vehiculo(placa, marca, modelo, anio, color)
        
        if success:
            messagebox.showinfo("Éxito", message)
            self._limpiar_campos()
            self._listar()
        else:
            messagebox.showerror("Error", message)
    
    def _consultar(self):
        """Consultar un vehículo por placa"""
        if not self._verificar_conexion():
            return
        
        placa = self.entries['entry_placa'].get().strip().upper()
        
        if not placa:
            messagebox.showwarning("Advertencia", "Ingrese una placa para consultar")
            return
        
        vehiculo, message = self.service.consultar_vehiculo(placa)
        
        if vehiculo:
            self.entries['entry_marca'].delete(0, tk.END)
            self.entries['entry_marca'].insert(0, vehiculo.marca)
            self.entries['entry_modelo'].delete(0, tk.END)
            self.entries['entry_modelo'].insert(0, vehiculo.modelo)
            self.entries['entry_anio'].delete(0, tk.END)
            self.entries['entry_anio'].insert(0, vehiculo.año)
            self.entries['entry_color'].delete(0, tk.END)
            self.entries['entry_color'].insert(0, vehiculo.color)
            messagebox.showinfo("Información", message)
        else:
            messagebox.showwarning("No encontrado", message)
    
    def _actualizar(self):
        """Actualizar un vehículo existente"""
        if not self._verificar_conexion():
            return
        
        placa = self.entries['entry_placa'].get().strip().upper()
        marca = self.entries['entry_marca'].get().strip()
        modelo = self.entries['entry_modelo'].get().strip()
        anio_str = self.entries['entry_anio'].get().strip()
        color = self.entries['entry_color'].get().strip()
        
        if not placa:
            messagebox.showwarning("Advertencia", "Ingrese una placa para actualizar")
            return
        
        try:
            anio = int(anio_str)
        except ValueError:
            messagebox.showerror("Error", "El año debe ser un número")
            return
        
        success, message = self.service.actualizar_vehiculo(placa, marca, modelo, anio, color)
        
        if success:
            messagebox.showinfo("Éxito", message)
            self._limpiar_campos()
            self._listar()
        else:
            messagebox.showerror("Error", message)
    
    def _eliminar(self):
        """Eliminar un vehículo"""
        if not self._verificar_conexion():
            return
        
        placa = self.entries['entry_placa'].get().strip().upper()
        
        if not placa:
            messagebox.showwarning("Advertencia", "Ingrese una placa para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el vehículo {placa}?"):
            success, message = self.service.eliminar_vehiculo(placa)
            
            if success:
                messagebox.showinfo("Éxito", message)
                self._limpiar_campos()
                self._listar()
            else:
                messagebox.showerror("Error", message)
    
    def _listar(self):
        """Listar todos los vehículos"""
        if not self._verificar_conexion():
            return
        
        vehiculos, message = self.service.listar_vehiculos()
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar datos
        for v in vehiculos:
            self.tree.insert("", tk.END, values=(v.placa, v.marca, v.modelo, v.año, v.color))
    
    def _seleccionar_fila(self, event):
        """Cargar datos de la fila seleccionada en el formulario"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']
            if valores:
                self.entries['entry_placa'].delete(0, tk.END)
                self.entries['entry_placa'].insert(0, valores[0])
                self.entries['entry_marca'].delete(0, tk.END)
                self.entries['entry_marca'].insert(0, valores[1])
                self.entries['entry_modelo'].delete(0, tk.END)
                self.entries['entry_modelo'].insert(0, valores[2])
                self.entries['entry_anio'].delete(0, tk.END)
                self.entries['entry_anio'].insert(0, valores[3])
                self.entries['entry_color'].delete(0, tk.END)
                self.entries['entry_color'].insert(0, valores[4])
    
    def _limpiar_campos(self):
        """Limpiar todos los campos del formulario"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)