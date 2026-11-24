import tkinter as tk
from tkinter import messagebox, ttk

from sqlalchemy.exc import SQLAlchemyError

from actualizar import actualizar_cliente
from consultar import consultar_clientes
from eliminar import eliminar_cliente
from insertar import insertar_cliente


def crear_vista_clientes(contenedor):
    nombre = tk.StringVar()
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

        for registro in registros:
            tabla.insert("", "end", iid=str(registro["id"]), values=(
                registro["id"], registro["nombre"], registro["correo"], registro["telefono"] or ""
            ))
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

    ttk.Label(contenedor, text="Clientes", font=("Segoe UI", 14, "bold")).pack(anchor="w")

    formulario = ttk.LabelFrame(contenedor, text="Datos del cliente", padding=10)
    formulario.pack(fill="x", pady=(10, 10))
    formulario.columnconfigure(1, weight=1)

    ttk.Label(formulario, text="Nombre:").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=4)
    ttk.Entry(formulario, textvariable=nombre).grid(row=0, column=1, sticky="ew", pady=4)

    ttk.Label(formulario, text="Correo:").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=4)
    ttk.Entry(formulario, textvariable=correo).grid(row=1, column=1, sticky="ew", pady=4)

    ttk.Label(formulario, text="Teléfono:").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=4)
    ttk.Entry(formulario, textvariable=telefono).grid(row=2, column=1, sticky="ew", pady=4)

    botones = ttk.Frame(contenedor)
    botones.pack(fill="x", pady=(0, 10))
    for texto, accion in [
        ("Crear", crear),
        ("Actualizar", actualizar),
        ("Eliminar", eliminar),
        ("Limpiar", limpiar),
        ("Recargar", cargar_datos)
    ]:
        ttk.Button(botones, text=texto, command=accion).pack(side="left", padx=(0, 6))

    marco_tabla = ttk.Frame(contenedor)
    marco_tabla.pack(fill="both", expand=True)

    tabla = ttk.Treeview(marco_tabla, columns=("id", "nombre", "correo", "telefono"), show="headings", selectmode="browse")
    for columna, titulo, ancho in [
        ("id", "ID", 60),
        ("nombre", "Nombre", 220),
        ("correo", "Correo", 260),
        ("telefono", "Teléfono", 150)
    ]:
        tabla.heading(columna, text=titulo)
        tabla.column(columna, width=ancho, minwidth=50)
    tabla.column("id", stretch=False)

    barra = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=barra.set)
    tabla.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    ttk.Label(contenedor, textvariable=mensaje, wraplength=700).pack(fill="x", pady=(8, 0))

    cargar_datos()
    return cargar_datos

