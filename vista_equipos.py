import tkinter as tk
from tkinter import messagebox, ttk

from sqlalchemy.exc import SQLAlchemyError

from actualizar import actualizar_equipo
from consultar import consultar_categorias, consultar_equipos
from eliminar import eliminar_equipo
from factory import TIPOS_VALIDOS
from insertar import insertar_equipo


def crear_vista_equipos(contenedor):
    nombre = tk.StringVar()
    tipo = tk.StringVar(value=TIPOS_VALIDOS[0])
    categoria = tk.StringVar()
    precio_diario = tk.StringVar()
    stock_total = tk.StringVar(value="0")
    solo_disponibles = tk.BooleanVar(value=False)
    mensaje = tk.StringVar()
    categorias = {}

    def mostrar_error(error):
        if isinstance(error, ValueError):
            texto = str(error)
        else:
            texto = "No se pudo completar la operación en la base de datos."
        messagebox.showerror("Equipos", texto, parent=contenedor)

    def limpiar():
        nombre.set("")
        tipo.set(TIPOS_VALIDOS[0])
        categoria.set("")
        precio_diario.set("")
        stock_total.set("0")
        for fila in tabla.selection():
            tabla.selection_remove(fila)
        mensaje.set("Formulario limpio. Puedes crear un equipo.")

    def cargar_datos():
        try:
            lista_categorias = consultar_categorias()
            equipos = consultar_equipos(solo_disponibles=solo_disponibles.get())
        except SQLAlchemyError as error:
            mostrar_error(error)
            return

        # El nombre se muestra en la lista y el ID se usa para guardar.
        categorias.clear()
        for registro in lista_categorias:
            categorias[registro["nombre"]] = registro["id"]
        lista_categoria["values"] = list(categorias.keys())

        for fila in tabla.get_children():
            tabla.delete(fila)
        for equipo in equipos:
            tabla.insert("", "end", iid=str(equipo["id"]), values=(
                equipo["id"], equipo["nombre"], equipo["tipo"], equipo["categoria"],
                equipo["precio_diario"], equipo["stock_total"], equipo["stock_disponible"]
            ))
        limpiar()
        if not categorias:
            mensaje.set("Primero crea una categoría para poder registrar equipos.")

    def seleccionar(event):
        seleccion = tabla.selection()
        if not seleccion:
            return
        valores = tabla.item(seleccion[0], "values")
        nombre.set(valores[1])
        tipo.set(valores[2])
        categoria.set(valores[3])
        precio_diario.set(valores[4])
        stock_total.set(valores[5])
        mensaje.set("Equipo seleccionado. El stock disponible se calcula automáticamente.")

    def leer_datos():
        categoria_id = categorias.get(categoria.get())
        if categoria_id is None:
            raise ValueError("Selecciona una categoría de la lista.")
        try:
            precio = float(precio_diario.get().replace(",", "."))
        except ValueError:
            raise ValueError("El precio diario debe ser un número.") from None
        try:
            stock = int(stock_total.get())
        except ValueError:
            raise ValueError("El stock total debe ser un número entero.") from None
        return nombre.get(), tipo.get(), categoria_id, precio, stock

    def crear():
        try:
            nombre_equipo, tipo_equipo, categoria_id, precio, stock = leer_datos()
            insertar_equipo(nombre_equipo, tipo_equipo, categoria_id, precio, stock)
        except (ValueError, SQLAlchemyError) as error:
            mostrar_error(error)
            return
        cargar_datos()
        mensaje.set("Equipo creado correctamente.")

    def actualizar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Equipos", "Selecciona un equipo en la tabla.", parent=contenedor)
            return
        try:
            nombre_equipo, tipo_equipo, categoria_id, precio, stock = leer_datos()
            actualizar_equipo(int(seleccion[0]), nombre_equipo, tipo_equipo, categoria_id, precio, stock)
        except (ValueError, SQLAlchemyError) as error:
            mostrar_error(error)
            return
        cargar_datos()
        mensaje.set("Equipo actualizado correctamente.")

    def eliminar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Equipos", "Selecciona un equipo en la tabla.", parent=contenedor)
            return
        if not messagebox.askyesno("Equipos", "¿Quieres eliminar el equipo seleccionado?", parent=contenedor):
            return
        try:
            eliminar_equipo(int(seleccion[0]))
        except (ValueError, SQLAlchemyError) as error:
            mostrar_error(error)
            return
        cargar_datos()
        mensaje.set("Equipo eliminado correctamente.")

    ttk.Label(contenedor, text="Equipos", font=("Segoe UI", 14, "bold")).pack(anchor="w")

    formulario = ttk.LabelFrame(contenedor, text="Datos del equipo", padding=10)
    formulario.pack(fill="x", pady=(10, 10))
    formulario.columnconfigure(1, weight=1)
    formulario.columnconfigure(3, weight=1)

    ttk.Label(formulario, text="Nombre:").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=4)
    ttk.Entry(formulario, textvariable=nombre).grid(row=0, column=1, sticky="ew", pady=4)
    ttk.Label(formulario, text="Tipo:").grid(row=0, column=2, sticky="w", padx=(15, 10), pady=4)
    ttk.Combobox(formulario, textvariable=tipo, values=TIPOS_VALIDOS, state="readonly").grid(row=0, column=3, sticky="ew", pady=4)

    ttk.Label(formulario, text="Categoría:").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=4)
    lista_categoria = ttk.Combobox(formulario, textvariable=categoria, state="readonly")
    lista_categoria.grid(row=1, column=1, sticky="ew", pady=4)
    ttk.Label(formulario, text="Precio diario:").grid(row=1, column=2, sticky="w", padx=(15, 10), pady=4)
    ttk.Entry(formulario, textvariable=precio_diario).grid(row=1, column=3, sticky="ew", pady=4)

    ttk.Label(formulario, text="Stock total:").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=4)
    ttk.Entry(formulario, textvariable=stock_total).grid(row=2, column=1, sticky="ew", pady=4)
    ttk.Label(formulario, text="El stock disponible se calcula automáticamente.", wraplength=300).grid(row=2, column=2, columnspan=2, sticky="w", padx=(15, 0), pady=4)

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
    ttk.Checkbutton(botones, text="Solo disponibles", variable=solo_disponibles, command=cargar_datos).pack(side="right")

    marco_tabla = ttk.Frame(contenedor)
    marco_tabla.pack(fill="both", expand=True)
    marco_tabla.columnconfigure(0, weight=1)
    marco_tabla.rowconfigure(0, weight=1)

    columnas = ("id", "nombre", "tipo", "categoria", "precio", "total", "disponible")
    tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", selectmode="browse")
    for columna, titulo, ancho in [
        ("id", "ID", 50),
        ("nombre", "Nombre", 160),
        ("tipo", "Tipo", 90),
        ("categoria", "Categoría", 130),
        ("precio", "Precio diario", 100),
        ("total", "Stock total", 90),
        ("disponible", "Disponible", 90)
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
