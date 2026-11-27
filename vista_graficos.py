import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy.exc import SQLAlchemyError

from estilos import COLORES
from graficos import crear_grafico_categorias, crear_grafico_equipos


def crear_vista_graficos(contenedor):
    mensaje = tk.StringVar(value="Entra a esta pestaña o pulsa Recargar para ver los gráficos.")
    lienzos = []

    def mostrar_grafico(marco, crear_figura):
        try:
            figura = crear_figura()
        except ValueError:
            ttk.Label(marco, text="Todavía no hay arriendos para mostrar.", style="Ayuda.TLabel").pack(expand=True)
            return False

        # Usamos la misma paleta que el resto de la aplicación.
        figura.set_facecolor(COLORES["superficie"])
        figura.set_layout_engine("tight")
        for ejes in figura.axes:
            ejes.set_facecolor(COLORES["superficie"])
            ejes.title.set_color(COLORES["texto"])
            ejes.xaxis.label.set_color(COLORES["secundario"])
            ejes.tick_params(colors=COLORES["secundario"])
            for borde in ejes.spines.values():
                borde.set_edgecolor(COLORES["borde"])
            for barra in ejes.patches:
                barra.set_facecolor(COLORES["acento"])
            for etiqueta in ejes.texts:
                etiqueta.set_color(COLORES["texto"])

        lienzo = FigureCanvasTkAgg(figura, master=marco)
        lienzo.draw()
        lienzo.get_tk_widget().pack(fill="both", expand=True)
        lienzos.append(lienzo)
        return True

    def cargar_graficos():
        for marco in [marco_categorias, marco_equipos]:
            for hijo in marco.winfo_children():
                hijo.destroy()
        lienzos.clear()
        try:
            hay_categorias = mostrar_grafico(marco_categorias, crear_grafico_categorias)
            hay_equipos = mostrar_grafico(marco_equipos, crear_grafico_equipos)
        except SQLAlchemyError:
            mensaje.set("No se pudieron cargar los gráficos desde la base de datos.")
            return

        if hay_categorias and hay_equipos:
            mensaje.set("Gráficos actualizados. Se cuentan operaciones de arriendo, no unidades.")
        else:
            mensaje.set("Registra un arriendo para ver los gráficos.")

    cabecera = ttk.Frame(contenedor)
    cabecera.pack(fill="x")
    ttk.Label(cabecera, text="Gráficos", style="TituloVista.TLabel").pack(side="left")
    ttk.Label(cabecera, text="Arriendos por categoría y equipos más arrendados.", style="Ayuda.TLabel").pack(side="left", padx=(16, 0))
    ttk.Button(cabecera, text="Recargar", command=cargar_graficos).pack(side="right")

    # El mensaje mantiene su espacio aunque los gráficos crezcan.
    ttk.Label(contenedor, textvariable=mensaje, style="Ayuda.TLabel", wraplength=850).pack(side="bottom", fill="x", pady=(12, 0))

    area = ttk.Frame(contenedor)
    area.pack(fill="both", expand=True, pady=(16, 0))
    area.columnconfigure(0, weight=1, uniform="graficos")
    area.columnconfigure(1, weight=1, uniform="graficos")
    area.rowconfigure(0, weight=1)

    marco_categorias = ttk.Frame(area, style="Panel.TFrame", padding=8)
    marco_categorias.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
    marco_equipos = ttk.Frame(area, style="Panel.TFrame", padding=8)
    marco_equipos.grid(row=0, column=1, sticky="nsew", padx=(7, 0))

    return cargar_graficos
