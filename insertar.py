from math import isfinite
from sqlalchemy.exc import IntegrityError
from conexion import SessionLocal
from models import Categoria, Cliente, Equipo


def validar_texto(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"El campo {campo} es obligatorio.")
    return valor.strip()


def insertar_categoria(nombre, descripcion=None):
    nombre = validar_texto(nombre, "nombre")

    if descripcion is not None:
        descripcion = descripcion.strip() or None

    try:
        with SessionLocal.begin() as sesion:
            categoria = Categoria(
                nombre=nombre,
                descripcion=descripcion
            )

            sesion.add(categoria)
            sesion.flush()
            categoria_id = categoria.id

        return categoria_id

    except IntegrityError as error:
        raise ValueError(
            "Ya existe una categoría con ese nombre."
        ) from error


def insertar_cliente(nombre, correo, telefono=None):
    nombre = validar_texto(nombre, "nombre")
    correo = validar_texto(correo, "correo").lower()

    if telefono is not None:
        telefono = telefono.strip() or None

    try:
        with SessionLocal.begin() as sesion:
            cliente = Cliente(
                nombre=nombre,
                correo=correo,
                telefono=telefono
            )

            sesion.add(cliente)
            sesion.flush()
            cliente_id = cliente.id

        return cliente_id

    except IntegrityError as error:
        raise ValueError(
            "Ya existe un cliente con ese correo."
        ) from error


def insertar_equipo(nombre, tipo, categoria_id, precio_diario, stock_total):
    nombre = validar_texto(nombre, "nombre")
    tipo = validar_texto(tipo, "tipo")

    if type(categoria_id) is not int or categoria_id <= 0:
        raise ValueError("El ID de la categoría debe ser un entero positivo.")

    if (
        isinstance(precio_diario, bool)
        or not isinstance(precio_diario, (int, float))
        or not isfinite(precio_diario)
        or precio_diario <= 0
    ):
        raise ValueError("El precio diario debe ser un número mayor que cero.")

    if type(stock_total) is not int or stock_total < 0:
        raise ValueError("El stock total debe ser un entero mayor o igual a cero.")

    try:
        with SessionLocal.begin() as sesion:
            categoria = sesion.get(Categoria, categoria_id)

            if categoria is None:
                raise ValueError("La categoría seleccionada no existe.")

            equipo = Equipo(
                nombre=nombre,
                tipo=tipo,
                categoria_id=categoria_id,
                precio_diario=precio_diario,
                stock_total=stock_total,
                stock_disponible=stock_total
            )

            sesion.add(equipo)
            sesion.flush()
            equipo_id = equipo.id

        return equipo_id

    except IntegrityError as error:
        raise ValueError(
            "No se pudo guardar el equipo porque sus datos "
            "incumplen una restricción de la base de datos."
        ) from error