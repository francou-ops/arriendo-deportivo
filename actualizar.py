from sqlalchemy.exc import IntegrityError

from conexion import SessionLocal
from factory import crear_tipo_equipo
from insertar import validar_texto
from models import Categoria, Cliente, Equipo


def actualizar_categoria(categoria_id, nombre, descripcion=None):
    nombre = validar_texto(nombre, "nombre")

    if descripcion is not None:
        descripcion = descripcion.strip() or None

    try:
        with SessionLocal.begin() as sesion:
            categoria = sesion.get(Categoria, categoria_id)

            if categoria is None:
                raise ValueError("La categoría seleccionada no existe.")

            categoria.nombre = nombre
            categoria.descripcion = descripcion

        return categoria_id

    except IntegrityError as error:
        raise ValueError(
            "Ya existe una categoría con ese nombre."
        ) from error


def actualizar_cliente(cliente_id, nombre, correo, telefono=None):
    nombre = validar_texto(nombre, "nombre")
    correo = validar_texto(correo, "correo").lower()

    if telefono is not None:
        telefono = telefono.strip() or None

    try:
        with SessionLocal.begin() as sesion:
            cliente = sesion.get(Cliente, cliente_id)

            if cliente is None:
                raise ValueError("El cliente seleccionado no existe.")

            cliente.nombre = nombre
            cliente.correo = correo
            cliente.telefono = telefono

        return cliente_id

    except IntegrityError as error:
        raise ValueError(
            "Ya existe un cliente con ese correo."
        ) from error


def actualizar_equipo(equipo_id, nombre, tipo, categoria_id, precio_diario, stock_total):
    nombre = validar_texto(nombre, "nombre")
    tipo = validar_texto(tipo, "tipo").lower().replace("ó", "o")
    tipo = crear_tipo_equipo(tipo).nombre

    if type(categoria_id) is not int or categoria_id <= 0:
        raise ValueError(
            "El ID de la categoría debe ser un entero positivo."
        )

    if type(precio_diario) not in (int, float):
        raise ValueError("El precio diario debe ser un número.")

    if not 0 < precio_diario < float("inf"):
        raise ValueError(
            "El precio diario debe ser mayor que cero y menor que infinito."
        )

    if type(stock_total) is not int or stock_total < 0:
        raise ValueError(
            "El stock total debe ser un entero mayor o igual a cero."
        )

    try:
        with SessionLocal.begin() as sesion:
            equipo = sesion.get(Equipo, equipo_id)

            if equipo is None:
                raise ValueError("El equipo seleccionado no existe.")

            categoria = sesion.get(Categoria, categoria_id)

            if categoria is None:
                raise ValueError("La categoría seleccionada no existe.")

            # Las unidades arrendadas deben mantenerse al cambiar el total.
            cantidad_arrendada = equipo.stock_total - equipo.stock_disponible

            if stock_total < cantidad_arrendada:
                raise ValueError(
                    "El stock total no puede ser menor que las unidades arrendadas."
                )

            equipo.nombre = nombre
            equipo.tipo = tipo
            equipo.categoria_id = categoria_id
            equipo.precio_diario = precio_diario
            equipo.stock_total = stock_total
            equipo.stock_disponible = stock_total - cantidad_arrendada

        return equipo_id

    except IntegrityError as error:
        raise ValueError(
            "No se pudo actualizar el equipo porque sus datos "
            "incumplen una restricción de la base de datos."
        ) from error
