import tkinter as tk
from tkinter import ttk


def crear_ventana_principal():
    ventana = tk.Tk()
    ventana.title("Arriendo Deportivo")
    ventana.geometry("1000x650")
    ventana.minsize(800, 500)

    contenedor = ttk.Frame(ventana, padding=20)
    contenedor.pack(fill="both", expand=True)

    ttk.Label(
        contenedor,
        text="Arriendo Deportivo",
        font=("Segoe UI", 20, "bold")
    ).pack(anchor="w")

    ttk.Label(
        contenedor,
        text="Gestión de arriendo de equipamiento deportivo"
    ).pack(anchor="w", pady=(4, 0))

    # Notebook es el contenedor de las pestañas.
    pestanas = ttk.Notebook(contenedor)
    pestanas.pack(fill="both", expand=True, pady=(20, 0))

    secciones = [
        ("Categorías", "Aquí podrás administrar las categorías de los equipos."),
        ("Clientes", "Aquí podrás administrar los clientes."),
        ("Equipos", "Aquí podrás administrar los equipos y consultar su disponibilidad."),
        ("Arriendos", "Aquí podrás registrar arriendos, procesar devoluciones y ver el historial."),
        ("Gráficos", "Aquí podrás ver los arriendos por categoría y los equipos más arrendados.")
    ]

    # Cada sección tiene un Frame donde después se agregarán sus formularios.
    for nombre, descripcion in secciones:
        pestana = ttk.Frame(pestanas, padding=20)
        pestanas.add(pestana, text=nombre)

        ttk.Label(
            pestana,
            text=nombre,
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w")

        ttk.Label(
            pestana,
            text=descripcion,
            wraplength=700
        ).pack(anchor="w", pady=(10, 0))

    ttk.Button(
        contenedor,
        text="Salir",
        command=ventana.destroy
    ).pack(anchor="e", pady=(15, 0))

    return ventana
