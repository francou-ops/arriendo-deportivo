import tkinter as tk
from tkinter import messagebox, ttk

from sqlalchemy.exc import SQLAlchemyError

from actualizar import actualizar_categoria
from consultar import consultar_categorias
from eliminar import eliminar_categoria
from insertar import insertar_categoria


def crear_vista_categorias(contenedor):
    nombre = tk.StringVar()
    descripcion = tk.StringVar()
    mensaje = tk.StringVar(value="Selecciona una categoría en la tabla para editarla o eliminarla.")

    def mostrar_error(error):
        if isinstance(error, ValueError):
            texto = str(error)
        else:
            texto = "No se pudo completar la operación en la base de datos."
        messagebox.showerror("Categorías", texto, parent=contenedor)

    def limpiar():
        nombre.set("")
        descripcion.set("")
        for fila in tabla.selection():
            tabla.selection_remove(fila)
        mensaje.set("Formulario limpio. Puedes crear una categoría.")

    def cargar_datos():
        try:
            registros = consultar_categorias()
        except SQLAlchemyError as error:
            mostrar_error(error)
            return

        for fila in tabla.get_children():
            tabla.delete(fila)

        for registro in registros:
            tabla.insert("", "end", iid=str(registro["id"]), values=(
                registro["id"], registro["nombre"], registro["descripcion"] or ""
            ))
        limpiar()

    def seleccionar(event):
        seleccion = tabla.selection()
        if not seleccion:
            return
        valores = tabla.item(seleccion[0], "values")
        nombre.set(valores[1])
        descripcion.set(valores[2])
        mensaje.set("Categoría seleccionada.")

    def crear():
        try:
            insertar_categoria(nombre.get(), descripcion.get())
        except (ValueError, SQLAlchemyError) as error:
            mostrar_error(error)
            return
        cargar_datos()
        mensaje.set("Categoría creada correctamente.")

    def actualizar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Categorías", "Selecciona una categoría en la tabla.", parent=contenedor)
            return
        try:
            actualizar_categoria(int(seleccion[0]), nombre.get(), descripcion.get())
        except (ValueError, SQLAlchemyError) as error:
            mostrar_error(error)
            return
        cargar_datos()
        mensaje.set("Categoría actualizada correctamente.")

    def eliminar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Categorías", "Selecciona una categoría en la tabla.", parent=contenedor)
            return
        if not messagebox.askyesno("Categorías", "¿Quieres eliminar la categoría seleccionada?", parent=contenedor):
            return
        try:
            eliminar_categoria(int(seleccion[0]))
        except (ValueError, SQLAlchemyError) as error:
            mostrar_error(error)
            return
        cargar_datos()
        mensaje.set("Categoría eliminada correctamente.")

    ttk.Label(contenedor, text="Categorías", font=("Segoe UI", 14, "bold")).pack(anchor="w")

    formulario = ttk.LabelFrame(contenedor, text="Datos de la categoría", padding=10)
    formulario.pack(fill="x", pady=(10, 10))
    formulario.columnconfigure(1, weight=1)

    ttk.Label(formulario, text="Nombre:").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=4)
    ttk.Entry(formulario, textvariable=nombre).grid(row=0, column=1, sticky="ew", pady=4)

    ttk.Label(formulario, text="Descripción:").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=4)
    ttk.Entry(formulario, textvariable=descripcion).grid(row=1, column=1, sticky="ew", pady=4)

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

    tabla = ttk.Treeview(marco_tabla, columns=("id", "nombre", "descripcion"), show="headings", selectmode="browse")
    for columna, titulo, ancho in [
        ("id", "ID", 60),
        ("nombre", "Nombre", 220),
        ("descripcion", "Descripción", 440)
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

