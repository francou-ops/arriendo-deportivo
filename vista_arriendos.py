import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from sqlalchemy.exc import SQLAlchemyError

from estilos import COLORES

from arriendos import devolver_arriendo, registrar_arriendo
from consultar import consultar_clientes, consultar_equipos_disponibles, consultar_historial_arriendos


def formato_pesos(valor):
    # Muestra 50000.0 como $50.000
    return f"${valor:,.0f}".replace(",", ".")


def crear_vista_arriendos(contenedor):
    equipo = tk.StringVar()
    cliente = tk.StringVar()
    fecha_inicio = tk.StringVar()
    fecha_fin = tk.StringVar()
    cantidad = tk.StringVar()
    total_registros = tk.StringVar()
    solo_activos = tk.BooleanVar(value=False)
    mensaje = tk.StringVar()
    equipos = {}
    clientes = {}

    def mostrar_error(error):
        if isinstance(error, ValueError):
            texto = str(error)
        else:
            texto = "No se pudo completar la operación en la base de datos."
        messagebox.showerror("Arriendos", texto, parent=contenedor)

    def limpiar():
        equipo.set("")
        cliente.set("")
        fecha_inicio.set(date.today().isoformat())
        fecha_fin.set(date.today().isoformat())
        cantidad.set("1")
        for fila in tabla.selection():
            tabla.selection_remove(fila)
        mensaje.set("Completa el formulario para registrar un arriendo.")

    def cargar_datos():
        try:
            lista_equipos = consultar_equipos_disponibles()
            lista_clientes = consultar_clientes()
            arriendos = consultar_historial_arriendos(solo_activos=solo_activos.get())
        except SQLAlchemyError as error:
            mostrar_error(error)
            return

        # El texto se muestra en la lista y el ID se usa para guardar.
        equipos.clear()
        for registro in lista_equipos:
            texto = f"{registro['nombre']} #{registro['id']} ({registro['stock_disponible']} disponibles)"
            equipos[texto] = registro["id"]
        lista_equipo["values"] = list(equipos.keys())

        clientes.clear()
        for registro in lista_clientes:
            texto = f"{registro['nombre']} #{registro['id']}"
            clientes[texto] = registro["id"]
        lista_cliente["values"] = list(clientes.keys())

        for fila in tabla.get_children():
            tabla.delete(fila)
        for indice, arriendo in enumerate(arriendos):
            tabla.insert("", "end", iid=str(arriendo["id"]), values=(
                arriendo["id"], arriendo["equipo"], arriendo["cliente"],
                arriendo["fecha_inicio"], arriendo["fecha_fin_prevista"],
                arriendo["cantidad"], arriendo["estado"], formato_pesos(arriendo["costo_total"])
            ), tags=("par" if indice % 2 == 0 else "impar",))
        total_registros.set(f"Registros: {len(arriendos)}")
        limpiar()

    def seleccionar(event):
        seleccion = tabla.selection()
        if not seleccion:
            return
        valores = tabla.item(seleccion[0], "values")
        mensaje.set(f"Arriendo {valores[0]} seleccionado. Estado: {valores[6]}.")

    def leer_datos():
        equipo_id = equipos.get(equipo.get())
        if equipo_id is None:
            raise ValueError("Selecciona un equipo de la lista.")
        cliente_id = clientes.get(cliente.get())
        if cliente_id is None:
            raise ValueError("Selecciona un cliente de la lista.")
        try:
            inicio = date.fromisoformat(fecha_inicio.get().strip())
            fin = date.fromisoformat(fecha_fin.get().strip())
        except ValueError:
            raise ValueError("Las fechas deben tener el formato AAAA-MM-DD.") from None
        try:
            unidades = int(cantidad.get())
        except ValueError:
            raise ValueError("La cantidad debe ser un número entero.") from None
        return equipo_id, cliente_id, inicio, fin, unidades

    def registrar():
        try:
            equipo_id, cliente_id, inicio, fin, unidades = leer_datos()
            registrar_arriendo(equipo_id, cliente_id, inicio, fin, unidades)
        except (ValueError, SQLAlchemyError) as error:
            mostrar_error(error)
            return
        cargar_datos()
        mensaje.set("Arriendo registrado correctamente.")

    def devolver():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Arriendos", "Selecciona un arriendo en la tabla.", parent=contenedor)
            return
        if not messagebox.askyesno("Arriendos", "¿Quieres devolver el arriendo seleccionado?", parent=contenedor):
            return
        try:
            devolver_arriendo(int(seleccion[0]))
        except (ValueError, SQLAlchemyError) as error:
            mostrar_error(error)
            return
        cargar_datos()
        mensaje.set("Arriendo devuelto correctamente.")

    cabecera = ttk.Frame(contenedor)
    cabecera.pack(fill="x")
    ttk.Label(cabecera, text="Arriendos", style="TituloVista.TLabel").pack(side="left")
    ttk.Label(cabecera, text="Registra arriendos y procesa devoluciones.", style="Ayuda.TLabel").pack(side="left", padx=(16, 0))

    formulario = ttk.Frame(contenedor, padding=12, style="Panel.TFrame")
    formulario.pack(fill="x", pady=(14, 14))
    formulario.columnconfigure(0, weight=3)
    formulario.columnconfigure(1, weight=3)
    formulario.columnconfigure(2, weight=2)
    formulario.columnconfigure(3, weight=2)
    formulario.columnconfigure(4, weight=1)

    ttk.Label(formulario, text="Equipo:").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 6))
    lista_equipo = ttk.Combobox(formulario, textvariable=equipo, state="readonly", width=26)
    lista_equipo.grid(row=1, column=0, sticky="ew", padx=(0, 10))
    ttk.Label(formulario, text="Cliente:").grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(0, 6))
    lista_cliente = ttk.Combobox(formulario, textvariable=cliente, state="readonly", width=20)
    lista_cliente.grid(row=1, column=1, sticky="ew", padx=(0, 10))
    ttk.Label(formulario, text="Fecha inicio:").grid(row=0, column=2, sticky="w", padx=(0, 10), pady=(0, 6))
    ttk.Entry(formulario, textvariable=fecha_inicio, width=12).grid(row=1, column=2, sticky="ew", padx=(0, 10))
    ttk.Label(formulario, text="Fecha término:").grid(row=0, column=3, sticky="w", padx=(0, 10), pady=(0, 6))
    ttk.Entry(formulario, textvariable=fecha_fin, width=12).grid(row=1, column=3, sticky="ew", padx=(0, 10))
    ttk.Label(formulario, text="Cantidad:").grid(row=0, column=4, sticky="w", pady=(0, 6))
    ttk.Entry(formulario, textvariable=cantidad, width=7).grid(row=1, column=4, sticky="ew")
    ttk.Label(formulario, text="Fechas en formato AAAA-MM-DD.", style="Ayuda.TLabel").grid(row=2, column=0, columnspan=5, sticky="w", pady=(8, 0))

    # El mensaje se reserva antes que la tabla para que siempre quede visible.
    ttk.Label(contenedor, textvariable=mensaje, style="Ayuda.TLabel", wraplength=850).pack(side="bottom", fill="x", pady=(10, 0))
    botones = ttk.Frame(contenedor)
    botones.pack(side="bottom", fill="x", pady=(12, 0))
    principales = ttk.Frame(botones)
    principales.pack(side="left")
    ttk.Button(principales, text="Registrar", command=registrar, style="Primario.TButton").pack(side="left", padx=(0, 8))
    ttk.Button(principales, text="Devolver", command=devolver).pack(side="left")
    ttk.Button(botones, text="Limpiar", command=limpiar, style="Discreto.TButton").pack(side="right")

    listado = ttk.Frame(contenedor, style="Panel.TFrame")
    listado.pack(fill="both", expand=True)
    controles_tabla = ttk.Frame(listado, padding=(12, 8))
    controles_tabla.pack(fill="x")
    ttk.Label(controles_tabla, text="Historial", style="TituloPanel.TLabel").pack(side="left")
    ttk.Button(controles_tabla, text="Recargar", command=cargar_datos, style="Discreto.TButton").pack(side="right")
    ttk.Checkbutton(controles_tabla, text="Solo activos", variable=solo_activos, command=cargar_datos).pack(side="right", padx=(0, 8))
    ttk.Label(listado, textvariable=total_registros, style="Ayuda.TLabel").pack(side="bottom", fill="x", padx=12, pady=8)
    ttk.Frame(listado, height=1, style="Linea.TFrame").pack(side="bottom", fill="x")

    marco_tabla = ttk.Frame(listado)
    marco_tabla.pack(fill="both", expand=True, padx=1)
    marco_tabla.columnconfigure(0, weight=1)
    marco_tabla.rowconfigure(0, weight=1)

    columnas = ("id", "equipo", "cliente", "inicio", "fin", "cantidad", "estado", "costo")
    tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", selectmode="browse")
    for columna, titulo, ancho in [
        ("id", "ID", 50),
        ("equipo", "Equipo", 190),
        ("cliente", "Cliente", 160),
        ("inicio", "Inicio", 110),
        ("fin", "Término", 110),
        ("cantidad", "Cantidad", 80),
        ("estado", "Estado", 100),
        ("costo", "Costo total", 120)
    ]:
        tabla.heading(columna, text=titulo, anchor="w")
        tabla.column(columna, width=ancho, minwidth=50)
    tabla.column("id", stretch=False, anchor="center")
    tabla.column("cantidad", anchor="center")
    tabla.column("costo", anchor="e")
    tabla.tag_configure("par", background=COLORES["fila"])
    tabla.tag_configure("impar", background=COLORES["superficie"])

    barra_vertical = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla.yview)
    barra_horizontal = ttk.Scrollbar(marco_tabla, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=barra_vertical.set, xscrollcommand=barra_horizontal.set)
    tabla.grid(row=0, column=0, sticky="nsew")
    barra_vertical.grid(row=0, column=1, sticky="ns")
    barra_horizontal.grid(row=1, column=0, sticky="ew")
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    cargar_datos()
    return cargar_datos
