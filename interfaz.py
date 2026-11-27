import tkinter as tk
from tkinter import ttk

from estilos import configurar_estilos
from vista_categorias import crear_vista_categorias
from vista_clientes import crear_vista_clientes
from vista_equipos import crear_vista_equipos
from vista_arriendos import crear_vista_arriendos
from vista_graficos import crear_vista_graficos


def crear_ventana_principal():
    ventana = tk.Tk()
    configurar_estilos(ventana)
    ventana.title("Arriendo Deportivo")
    ventana.geometry("1100x740")
    ventana.minsize(1000, 680)

    contenedor = ttk.Frame(ventana, padding=20, style="App.TFrame")
    contenedor.pack(fill="both", expand=True)

    cabecera = ttk.Frame(contenedor, style="App.TFrame")
    cabecera.pack(fill="x")
    ttk.Label(cabecera, text="AD", style="Marca.TLabel").pack(side="left", padx=(0, 15))
    titulos = ttk.Frame(cabecera, style="App.TFrame")
    titulos.pack(side="left")
    ttk.Label(titulos, text="Arriendo Deportivo", style="Titulo.TLabel").pack(anchor="w")
    ttk.Label(titulos, text="Equipos, clientes y disponibilidad", style="Subtitulo.TLabel").pack(anchor="w", pady=(3, 0))

    # Reservamos Salir antes de darle el espacio restante a las pestañas.
    ttk.Button(contenedor, text="Salir", command=ventana.destroy).pack(side="bottom", anchor="e", pady=(14, 0))

    pestanas = ttk.Notebook(contenedor)
    pestanas.pack(fill="both", expand=True, pady=(18, 0))

    categorias = ttk.Frame(pestanas, name="categorias", padding=16)
    clientes = ttk.Frame(pestanas, name="clientes", padding=16)
    equipos = ttk.Frame(pestanas, name="equipos", padding=16)
    arriendos = ttk.Frame(pestanas, name="arriendos", padding=16)
    graficos = ttk.Frame(pestanas, name="graficos", padding=16)

    pestanas.add(categorias, text="Categorías")
    pestanas.add(clientes, text="Clientes")
    pestanas.add(equipos, text="Equipos")
    pestanas.add(arriendos, text="Arriendos")
    pestanas.add(graficos, text="Gráficos")

    cargar_categorias = crear_vista_categorias(categorias)
    cargar_clientes = crear_vista_clientes(clientes)
    cargar_equipos = crear_vista_equipos(equipos)
    cargar_arriendos = crear_vista_arriendos(arriendos)
    cargar_graficos = crear_vista_graficos(graficos)

    # Al cambiar de pestaña vemos los datos más recientes.
    def cambiar_pestana(event):
        seleccion = pestanas.select()
        if seleccion == str(categorias):
            cargar_categorias()
        elif seleccion == str(clientes):
            cargar_clientes()
        elif seleccion == str(equipos):
            cargar_equipos()
        elif seleccion == str(arriendos):
            cargar_arriendos()
        elif seleccion == str(graficos):
            cargar_graficos()

    pestanas.bind("<<NotebookTabChanged>>", cambiar_pestana)
    return ventana
