# Punto de entrada de la aplicación
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.ui import MainWindow
import tkinter as tk

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()