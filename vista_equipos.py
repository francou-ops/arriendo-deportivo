import tkinter as tk
from tkinter import messagebox, ttk

from sqlalchemy.exc import SQLAlchemyError

from estilos import COLORES

from actualizar import actualizar_equipo
from consultar import consultar_categorias, consultar_equipos
from eliminar import eliminar_equipo
from factory import TIPOS_VALIDOS
from insertar import insertar_equipo


def crear_vista_equipos(contenedor):
    nombre = tk.StringVar()
    cantidad = tk.StringVar()
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
        for indice, equipo in enumerate(equipos):
            tabla.insert("", "end", iid=str(equipo["id"]), values=(
                equipo["id"], equipo["nombre"], equipo["tipo"], equipo["categoria"],
                equipo["precio_diario"], equipo["stock_total"], equipo["stock_disponible"]
            ), tags=("par" if indice % 2 == 0 else "impar",))
        cantidad.set(f"Registros: {len(equipos)}")
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

    cabecera = ttk.Frame(contenedor, style="App.TFrame")
    cabecera.pack(fill="x")
    ttk.Label(cabecera, text="Equipos", style="TituloVista.TLabel").pack(side="left")
    ttk.Label(cabecera, text="Selecciona un registro para editarlo.", style="Subtitulo.TLabel").pack(side="left", padx=(16, 0))

    cuerpo = ttk.Frame(contenedor, style="App.TFrame")
    cuerpo.pack(fill="both", expand=True, pady=(18, 0))

    # Reservamos el formulario a la derecha y el listado ocupa el resto.
    panel = ttk.Frame(cuerpo, width=300, padding=16, style="Panel.TFrame")
    panel.pack(side="right", fill="y", padx=(18, 0))
    panel.pack_propagate(False)
    ttk.Label(panel, text="Datos del equipo", style="TituloPanel.TLabel").pack(anchor="w", pady=(0, 18))

    botones = ttk.Frame(panel)
    botones.pack(side="bottom", fill="x")
    for texto, accion, estilo in [
        ("Crear", crear, "Primario.TButton"),
        ("Actualizar", actualizar, "TButton"),
        ("Limpiar", limpiar, "Discreto.TButton"),
        ("Eliminar", eliminar, "Eliminar.TButton")
    ]:
        ttk.Button(botones, text=texto, command=accion, style=estilo).pack(fill="x", pady=(0, 8))

    formulario = ttk.Frame(panel)
    formulario.pack(fill="x")
    formulario.columnconfigure(0, weight=1, uniform="campos")
    formulario.columnconfigure(1, weight=1, uniform="campos")

    ttk.Label(formulario, text="Nombre:").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
    ttk.Entry(formulario, textvariable=nombre, width=20).grid(row=1, column=0, columnspan=2, sticky="ew")
    ttk.Label(formulario, text="Tipo:").grid(row=2, column=0, sticky="w", pady=(12, 5))
    ttk.Combobox(formulario, textvariable=tipo, values=TIPOS_VALIDOS, state="readonly", width=12).grid(row=3, column=0, sticky="ew", padx=(0, 6))
    ttk.Label(formulario, text="Categoría:").grid(row=2, column=1, sticky="w", padx=(6, 0), pady=(12, 5))
    lista_categoria = ttk.Combobox(formulario, textvariable=categoria, state="readonly", width=12)
    lista_categoria.grid(row=3, column=1, sticky="ew", padx=(6, 0))
    ttk.Label(formulario, text="Precio diario:").grid(row=4, column=0, sticky="w", pady=(12, 5))
    ttk.Entry(formulario, textvariable=precio_diario, width=12).grid(row=5, column=0, sticky="ew", padx=(0, 6))
    ttk.Label(formulario, text="Stock total:").grid(row=4, column=1, sticky="w", padx=(6, 0), pady=(12, 5))
    ttk.Entry(formulario, textvariable=stock_total, width=12).grid(row=5, column=1, sticky="ew", padx=(6, 0))
    ttk.Label(formulario, text="El disponible se calcula automáticamente.", style="Ayuda.TLabel", wraplength=260).grid(row=6, column=0, columnspan=2, sticky="w", pady=(16, 0))

    listado = ttk.Frame(cuerpo, style="Panel.TFrame")
    listado.pack(fill="both", expand=True)

    controles_tabla = ttk.Frame(listado, padding=(14, 12))
    controles_tabla.pack(fill="x")
    ttk.Label(controles_tabla, text="Listado", style="TituloPanel.TLabel").pack(side="left")
    ttk.Button(controles_tabla, text="Recargar", command=cargar_datos, style="Discreto.TButton").pack(side="right")
    ttk.Checkbutton(controles_tabla, text="Solo disponibles", variable=solo_disponibles, command=cargar_datos).pack(side="right", padx=(0, 8))

    pie = ttk.Frame(listado, padding=(14, 10))
    pie.pack(side="bottom", fill="x")
    ttk.Label(pie, textvariable=cantidad, style="Ayuda.TLabel").pack(anchor="w")
    ttk.Label(pie, textvariable=mensaje, style="Ayuda.TLabel", wraplength=450).pack(anchor="w", pady=(4, 0))
    ttk.Frame(listado, height=1, style="Linea.TFrame").pack(side="bottom", fill="x")

    marco_tabla = ttk.Frame(listado)
    marco_tabla.pack(fill="both", expand=True, padx=1)
    marco_tabla.columnconfigure(0, weight=1)
    marco_tabla.rowconfigure(0, weight=1)

    # Conservamos los valores completos; mostramos las columnas más útiles.
    tabla = ttk.Treeview(marco_tabla, columns=("id", "nombre", "tipo", "categoria", "precio", "total", "disponible"), displaycolumns=("nombre", "precio", "total", "disponible"), show="headings", selectmode="browse")
    for columna, titulo, ancho in [
        ("id", "ID", 50),
        ("nombre", "Equipo", 230),
        ("tipo", "Tipo", 90),
        ("categoria", "Categoría", 130),
        ("precio", "Precio/día", 100),
        ("total", "Total", 70),
        ("disponible", "Disponible", 100)
    ]:
        tabla.heading(columna, text=titulo, anchor="w")
        tabla.column(columna, width=ancho, minwidth=60)
    tabla.tag_configure("par", background=COLORES["fila"])
    tabla.tag_configure("impar", background=COLORES["superficie"])
    tabla.column("precio", anchor="e")
    tabla.column("total", anchor="center")
    tabla.column("disponible", anchor="center")

    barra_vertical = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla.yview)
    barra_horizontal = ttk.Scrollbar(marco_tabla, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=barra_vertical.set, xscrollcommand=barra_horizontal.set)
    tabla.grid(row=0, column=0, sticky="nsew")
    barra_vertical.grid(row=0, column=1, sticky="ns")
    barra_horizontal.grid(row=1, column=0, sticky="ew")
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    cargar_datos()
    return cargar_datos
