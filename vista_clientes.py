import tkinter as tk
from tkinter import messagebox, ttk

from sqlalchemy.exc import SQLAlchemyError

from estilos import COLORES

from actualizar import actualizar_cliente
from consultar import consultar_clientes
from eliminar import eliminar_cliente
from insertar import insertar_cliente


def crear_vista_clientes(contenedor):
    nombre = tk.StringVar()
    cantidad = tk.StringVar()
    correo = tk.StringVar()
    telefono = tk.StringVar()
    mensaje = tk.StringVar(value="Selecciona un cliente en la tabla para editarlo o eliminarlo.")

    def mostrar_error(error):
        if isinstance(error, ValueError):
            texto = str(error)
        else:
            texto = "No se pudo completar la operación en la base de datos."
        messagebox.showerror("Clientes", texto, parent=contenedor)

    def limpiar():
        nombre.set("")
        correo.set("")
        telefono.set("")
        for fila in tabla.selection():
            tabla.selection_remove(fila)
        mensaje.set("Formulario limpio. Puedes crear un cliente.")

    def cargar_datos():
        try:
            registros = consultar_clientes()
        except SQLAlchemyError as error:
            mostrar_error(error)
            return

        for fila in tabla.get_children():
            tabla.delete(fila)

        for indice, registro in enumerate(registros):
            tabla.insert("", "end", iid=str(registro["id"]), values=(
                registro["id"], registro["nombre"], registro["correo"], registro["telefono"] or ""
            ), tags=("par" if indice % 2 == 0 else "impar",))
        cantidad.set(f"Registros: {len(registros)}")
        limpiar()

    def seleccionar(event):
        seleccion = tabla.selection()
        if not seleccion:
            return
        valores = tabla.item(seleccion[0], "values")
        nombre.set(valores[1])
        correo.set(valores[2])
        telefono.set(valores[3])
        mensaje.set("Cliente seleccionado.")

    def crear():
        try:
            insertar_cliente(nombre.get(), correo.get(), telefono.get())
        except (ValueError, SQLAlchemyError) as error:
            mostrar_error(error)
            return
        cargar_datos()
        mensaje.set("Cliente creado correctamente.")

    def actualizar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Clientes", "Selecciona un cliente en la tabla.", parent=contenedor)
            return
        try:
            actualizar_cliente(int(seleccion[0]), nombre.get(), correo.get(), telefono.get())
        except (ValueError, SQLAlchemyError) as error:
            mostrar_error(error)
            return
        cargar_datos()
        mensaje.set("Cliente actualizado correctamente.")

    def eliminar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Clientes", "Selecciona un cliente en la tabla.", parent=contenedor)
            return
        if not messagebox.askyesno("Clientes", "¿Quieres eliminar el cliente seleccionado?", parent=contenedor):
            return
        try:
            eliminar_cliente(int(seleccion[0]))
        except (ValueError, SQLAlchemyError) as error:
            mostrar_error(error)
            return
        cargar_datos()
        mensaje.set("Cliente eliminado correctamente.")

    cabecera = ttk.Frame(contenedor)
    cabecera.pack(fill="x")
    ttk.Label(cabecera, text="Clientes", style="TituloVista.TLabel").pack(side="left")
    ttk.Label(cabecera, text="Administra los datos de contacto de tus clientes.", style="Ayuda.TLabel").pack(side="left", padx=(16, 0))

    formulario = ttk.Frame(contenedor, padding=12, style="Panel.TFrame")
    formulario.pack(fill="x", pady=(14, 14))
    formulario.columnconfigure(0, weight=2)
    ttk.Label(formulario, text="Nombre:").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 6))
    ttk.Entry(formulario, textvariable=nombre, width=20).grid(row=1, column=0, sticky="ew", padx=(0, 10))
    formulario.columnconfigure(1, weight=3)
    ttk.Label(formulario, text="Correo:").grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(0, 6))
    ttk.Entry(formulario, textvariable=correo, width=20).grid(row=1, column=1, sticky="ew", padx=(0, 10))
    formulario.columnconfigure(2, weight=2)
    ttk.Label(formulario, text="Teléfono:").grid(row=0, column=2, sticky="w", padx=0, pady=(0, 6))
    ttk.Entry(formulario, textvariable=telefono, width=20).grid(row=1, column=2, sticky="ew", padx=0)

    # Reservamos el mensaje y las acciones antes de expandir el listado.
    ttk.Label(contenedor, textvariable=mensaje, style="Ayuda.TLabel", wraplength=850).pack(side="bottom", fill="x", pady=(10, 0))
    botones = ttk.Frame(contenedor)
    botones.pack(side="bottom", fill="x", pady=(12, 0))
    principales = ttk.Frame(botones)
    principales.pack(side="left")
    ttk.Button(principales, text="Crear", command=crear, style="Primario.TButton").pack(side="left", padx=(0, 8))
    ttk.Button(principales, text="Actualizar", command=actualizar).pack(side="left")
    secundarias = ttk.Frame(botones)
    secundarias.pack(side="right")
    ttk.Button(secundarias, text="Limpiar", command=limpiar, style="Discreto.TButton").pack(side="left", padx=(0, 8))
    ttk.Button(secundarias, text="Eliminar", command=eliminar, style="Eliminar.TButton").pack(side="left")

    listado = ttk.Frame(contenedor, style="Panel.TFrame")
    listado.pack(fill="both", expand=True)
    controles_tabla = ttk.Frame(listado, padding=(12, 8))
    controles_tabla.pack(fill="x")
    ttk.Label(controles_tabla, text="Listado", style="TituloPanel.TLabel").pack(side="left")
    ttk.Button(controles_tabla, text="Recargar", command=cargar_datos, style="Discreto.TButton").pack(side="right")

    ttk.Label(listado, textvariable=cantidad, style="Ayuda.TLabel").pack(side="bottom", fill="x", padx=12, pady=8)
    ttk.Frame(listado, height=1, style="Linea.TFrame").pack(side="bottom", fill="x")
    marco_tabla = ttk.Frame(listado)
    marco_tabla.pack(fill="both", expand=True, padx=1)
    marco_tabla.columnconfigure(0, weight=1)
    marco_tabla.rowconfigure(0, weight=1)

    tabla = ttk.Treeview(marco_tabla, columns=("id", "nombre", "correo", "telefono"), displaycolumns=("nombre", "correo", "telefono"), show="headings", selectmode="browse")
    for columna, titulo, ancho in [
        ("id", "ID", 50),
        ("nombre", "Nombre", 260),
        ("correo", "Correo", 400),
        ("telefono", "Teléfono", 180)
    ]:
        tabla.heading(columna, text=titulo, anchor="w")
        tabla.column(columna, width=ancho, minwidth=60)
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
