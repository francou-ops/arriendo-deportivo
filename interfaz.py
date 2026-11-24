import tkinter as tk
from tkinter import ttk

from vista_categorias import crear_vista_categorias
from vista_clientes import crear_vista_clientes
from vista_equipos import crear_vista_equipos


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

    # Se reserva primero el espacio del botón para que siempre quede visible.
    ttk.Button(
        contenedor,
        text="Salir",
        command=ventana.destroy
    ).pack(side="bottom", anchor="e", pady=(15, 0))

    pestanas = ttk.Notebook(contenedor)
    pestanas.pack(fill="both", expand=True, pady=(20, 0))

    categorias = ttk.Frame(pestanas, padding=15)
    clientes = ttk.Frame(pestanas, padding=15)
    equipos = ttk.Frame(pestanas, padding=15)
    arriendos = ttk.Frame(pestanas, padding=15)
    graficos = ttk.Frame(pestanas, padding=15)

    pestanas.add(categorias, text="Categorías")
    pestanas.add(clientes, text="Clientes")
    pestanas.add(equipos, text="Equipos")
    pestanas.add(arriendos, text="Arriendos")
    pestanas.add(graficos, text="Gráficos")

    cargar_categorias = crear_vista_categorias(categorias)
    cargar_clientes = crear_vista_clientes(clientes)
    cargar_equipos = crear_vista_equipos(equipos)

    # Al entrar a una vista se recargan sus datos desde la base.
    def cambiar_pestana(event):
        seleccion = pestanas.select()
        if seleccion == str(categorias):
            cargar_categorias()
        elif seleccion == str(clientes):
            cargar_clientes()
        elif seleccion == str(equipos):
            cargar_equipos()

    pestanas.bind("<<NotebookTabChanged>>", cambiar_pestana)

    for pestana, titulo, descripcion in [
        (arriendos, "Arriendos", "Aquí podrás registrar arriendos, procesar devoluciones y ver el historial."),
        (graficos, "Gráficos", "Aquí podrás ver los arriendos por categoría y los equipos más arrendados.")
    ]:
        ttk.Label(pestana, text=titulo, font=("Segoe UI", 14, "bold")).pack(anchor="w")
        ttk.Label(pestana, text=descripcion, wraplength=700).pack(anchor="w", pady=(10, 0))

    return ventana
