import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from sqlalchemy.exc import SQLAlchemyError

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
        for arriendo in arriendos:
            tabla.insert("", "end", iid=str(arriendo["id"]), values=(
                arriendo["id"], arriendo["equipo"], arriendo["cliente"],
                arriendo["fecha_inicio"], arriendo["fecha_fin_prevista"],
                arriendo["cantidad"], arriendo["estado"], formato_pesos(arriendo["costo_total"])
            ))
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

    ttk.Label(contenedor, text="Arriendos", font=("Segoe UI", 14, "bold")).pack(anchor="w")

    formulario = ttk.LabelFrame(contenedor, text="Nuevo arriendo", padding=10)
    formulario.pack(fill="x", pady=(10, 10))
    formulario.columnconfigure(1, weight=1)
    formulario.columnconfigure(3, weight=1)

    ttk.Label(formulario, text="Equipo:").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=4)
    lista_equipo = ttk.Combobox(formulario, textvariable=equipo, state="readonly")
    lista_equipo.grid(row=0, column=1, sticky="ew", pady=4)
    ttk.Label(formulario, text="Cliente:").grid(row=0, column=2, sticky="w", padx=(15, 10), pady=4)
    lista_cliente = ttk.Combobox(formulario, textvariable=cliente, state="readonly")
    lista_cliente.grid(row=0, column=3, sticky="ew", pady=4)

    ttk.Label(formulario, text="Fecha inicio:").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=4)
    ttk.Entry(formulario, textvariable=fecha_inicio).grid(row=1, column=1, sticky="ew", pady=4)
    ttk.Label(formulario, text="Fecha término:").grid(row=1, column=2, sticky="w", padx=(15, 10), pady=4)
    ttk.Entry(formulario, textvariable=fecha_fin).grid(row=1, column=3, sticky="ew", pady=4)

    ttk.Label(formulario, text="Cantidad:").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=4)
    ttk.Entry(formulario, textvariable=cantidad).grid(row=2, column=1, sticky="ew", pady=4)
    ttk.Label(formulario, text="Fechas en formato AAAA-MM-DD.").grid(row=2, column=2, columnspan=2, sticky="w", padx=(15, 0), pady=4)

    botones = ttk.Frame(contenedor)
    botones.pack(fill="x", pady=(0, 10))
    for texto, accion in [
        ("Registrar", registrar),
        ("Devolver", devolver),
        ("Limpiar", limpiar),
        ("Recargar", cargar_datos)
    ]:
        ttk.Button(botones, text=texto, command=accion).pack(side="left", padx=(0, 6))
    ttk.Checkbutton(botones, text="Solo activos", variable=solo_activos, command=cargar_datos).pack(side="right")

    marco_tabla = ttk.Frame(contenedor)
    marco_tabla.pack(fill="both", expand=True)
    marco_tabla.columnconfigure(0, weight=1)
    marco_tabla.rowconfigure(0, weight=1)

    columnas = ("id", "equipo", "cliente", "inicio", "fin", "cantidad", "estado", "costo")
    tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", selectmode="browse")
    for columna, titulo, ancho in [
        ("id", "ID", 50),
        ("equipo", "Equipo", 150),
        ("cliente", "Cliente", 130),
        ("inicio", "Inicio", 95),
        ("fin", "Término", 95),
        ("cantidad", "Cantidad", 70),
        ("estado", "Estado", 85),
        ("costo", "Costo total", 95)
    ]:
        tabla.heading(columna, text=titulo)
        tabla.column(columna, width=ancho, minwidth=50)
    tabla.column("id", stretch=False)

    barra_vertical = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla.yview)
    barra_horizontal = ttk.Scrollbar(marco_tabla, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=barra_vertical.set, xscrollcommand=barra_horizontal.set)
    tabla.grid(row=0, column=0, sticky="nsew")
    barra_vertical.grid(row=0, column=1, sticky="ns")
    barra_horizontal.grid(row=1, column=0, sticky="ew")
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    ttk.Label(contenedor, textvariable=mensaje, wraplength=700).pack(fill="x", pady=(8, 0))

    cargar_datos()
    return cargar_datos
