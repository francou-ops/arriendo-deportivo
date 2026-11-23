from sqlalchemy.exc import IntegrityError

from conexion import SessionLocal
from models import Categoria, Cliente, Equipo


def eliminar_categoria(categoria_id):
    try:
        with SessionLocal.begin() as sesion:
            categoria = sesion.get(Categoria, categoria_id)

            if categoria is None:
                raise ValueError("La categoría seleccionada no existe.")

            if categoria.equipos:
                raise ValueError(
                    "No se puede eliminar la categoría porque tiene equipos asociados."
                )

            sesion.delete(categoria)

        return categoria_id

    except IntegrityError as error:
        raise ValueError(
            "No se pudo eliminar la categoría porque tiene registros relacionados."
        ) from error


def eliminar_cliente(cliente_id):
    try:
        with SessionLocal.begin() as sesion:
            cliente = sesion.get(Cliente, cliente_id)

            if cliente is None:
                raise ValueError("El cliente seleccionado no existe.")

            # Se conserva el historial, aunque los arriendos ya estén devueltos.
            if cliente.arriendos:
                raise ValueError(
                    "No se puede eliminar el cliente porque tiene arriendos registrados."
                )

            sesion.delete(cliente)

        return cliente_id

    except IntegrityError as error:
        raise ValueError(
            "No se pudo eliminar el cliente porque tiene registros relacionados."
        ) from error


def eliminar_equipo(equipo_id):
    try:
        with SessionLocal.begin() as sesion:
            equipo = sesion.get(Equipo, equipo_id)

            if equipo is None:
                raise ValueError("El equipo seleccionado no existe.")

            if equipo.arriendos:
                raise ValueError(
                    "No se puede eliminar el equipo porque tiene arriendos registrados."
                )

            sesion.delete(equipo)

        return equipo_id

    except IntegrityError as error:
        raise ValueError(
            "No se pudo eliminar el equipo porque tiene registros relacionados."
        ) from error
