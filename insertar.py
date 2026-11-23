from sqlalchemy.exc import IntegrityError

from conexion import SessionLocal
from factory import crear_tipo_equipo
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

    # Acepta, por ejemplo, "Balón" y "Protección".
    tipo = validar_texto(tipo, "tipo").lower().replace("ó", "o")

    # La fábrica valida el tipo y entrega su nombre para guardarlo en la BD.
    tipo = crear_tipo_equipo(tipo).nombre

    if type(categoria_id) is not int or categoria_id <= 0:
        raise ValueError(
            "El ID de la categoría debe ser un entero positivo."
        )

    if type(precio_diario) not in (int, float):
        raise ValueError(
            "El precio diario debe ser un número."
        )

    # Acepta precios positivos y finitos sin usar math.
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
            categoria = sesion.get(Categoria, categoria_id)

            if categoria is None:
                raise ValueError(
                    "La categoría seleccionada no existe."
                )

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