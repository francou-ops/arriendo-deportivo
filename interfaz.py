import tkinter as tk
from tkinter import ttk

from estilos import configurar_estilos

from vista_categorias import crear_vista_categorias
from vista_clientes import crear_vista_clientes
from vista_equipos import crear_vista_equipos


def crear_ventana_principal():
    ventana = tk.Tk()
    configurar_estilos(ventana)
    ventana.title("Arriendo Deportivo")
    ventana.geometry("1160x740")
    ventana.minsize(1040, 700)

    contenedor = ttk.Frame(ventana, style="App.TFrame")
    contenedor.pack(fill="both", expand=True)

    cabecera = ttk.Frame(contenedor, padding=(22, 18), style="App.TFrame")
    cabecera.pack(fill="x")
    ttk.Label(cabecera, text="AD", style="Marca.TLabel").pack(side="left", padx=(0, 15))

    titulos = ttk.Frame(cabecera, style="App.TFrame")
    titulos.pack(side="left")
    ttk.Label(titulos, text="Arriendo Deportivo", style="Titulo.TLabel").pack(anchor="w")
    ttk.Label(
        titulos,
        text="Administra equipos, clientes y disponibilidad",
        style="Subtitulo.TLabel"
    ).pack(anchor="w", pady=(3, 0))

    ttk.Frame(contenedor, height=1, style="Linea.TFrame").pack(fill="x")

    cuerpo = ttk.Frame(contenedor, style="App.TFrame")
    cuerpo.pack(fill="both", expand=True)

    menu = ttk.Frame(cuerpo, width=160, padding=(12, 20), style="App.TFrame")
    menu.pack(side="left", fill="y")
    menu.pack_propagate(False)
    ttk.Button(menu, text="Salir", command=ventana.destroy, style="Menu.TButton").pack(side="bottom", fill="x")
    ttk.Frame(cuerpo, width=1, style="Linea.TFrame").pack(side="left", fill="y")

    contenido = ttk.Frame(cuerpo, padding=20, style="App.TFrame")
    contenido.pack(side="left", fill="both", expand=True)
    contenido.columnconfigure(0, weight=1)
    contenido.rowconfigure(0, weight=1)

    categorias = ttk.Frame(contenido, name="categorias", style="App.TFrame")
    clientes = ttk.Frame(contenido, name="clientes", style="App.TFrame")
    equipos = ttk.Frame(contenido, name="equipos", style="App.TFrame")
    arriendos = ttk.Frame(contenido, name="arriendos", style="App.TFrame")
    graficos = ttk.Frame(contenido, name="graficos", style="App.TFrame")

    # Las vistas comparten el mismo espacio; tkraise muestra la elegida.
    for vista in [categorias, clientes, equipos, arriendos, graficos]:
        vista.grid(row=0, column=0, sticky="nsew")

    cargar_categorias = crear_vista_categorias(categorias)
    cargar_clientes = crear_vista_clientes(clientes)
    cargar_equipos = crear_vista_equipos(equipos)

    def mostrar_vista(vista):
        vista.tkraise()
        for boton in botones.values():
            boton.configure(style="Menu.TButton")
        botones[vista].configure(style="MenuActivo.TButton")

        # Al entrar a una vista se recargan sus datos desde la base.
        if vista == categorias:
            cargar_categorias()
        elif vista == clientes:
            cargar_clientes()
        elif vista == equipos:
            cargar_equipos()

    botones = {
        categorias: ttk.Button(menu, text="Categorías", command=lambda: mostrar_vista(categorias), style="Menu.TButton"),
        clientes: ttk.Button(menu, text="Clientes", command=lambda: mostrar_vista(clientes), style="Menu.TButton"),
        equipos: ttk.Button(menu, text="Equipos", command=lambda: mostrar_vista(equipos), style="Menu.TButton"),
        arriendos: ttk.Button(menu, text="Arriendos", command=lambda: mostrar_vista(arriendos), style="Menu.TButton"),
        graficos: ttk.Button(menu, text="Gráficos", command=lambda: mostrar_vista(graficos), style="Menu.TButton"),
    }
    for boton in botones.values():
        boton.pack(fill="x", pady=(0, 6))

    for vista, titulo, descripcion in [
        (arriendos, "Arriendos", "Aquí podrás registrar arriendos, procesar devoluciones y ver el historial."),
        (graficos, "Gráficos", "Aquí podrás ver los arriendos por categoría y los equipos más arrendados.")
    ]:
        ttk.Label(vista, text=titulo, style="TituloVista.TLabel").pack(anchor="w")
        ttk.Label(vista, text=descripcion, style="Subtitulo.TLabel", wraplength=650).pack(anchor="w", pady=(10, 0))

    mostrar_vista(categorias)
    return ventana
