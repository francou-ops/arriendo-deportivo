from sqlalchemy import select

from conexion import SessionLocal
from models import Arriendo, Categoria, Cliente, Equipo


# Las consultas devuelven listas de diccionarios para usarlas en la interfaz.
def consultar_categorias():
    with SessionLocal() as sesion:
        consulta = select(Categoria).order_by(Categoria.nombre, Categoria.id)
        categorias = sesion.scalars(consulta).all()

        resultados = []
        for categoria in categorias:
            resultados.append({
                "id": categoria.id,
                "nombre": categoria.nombre,
                "descripcion": categoria.descripcion
            })

        return resultados


def consultar_clientes():
    with SessionLocal() as sesion:
        consulta = select(Cliente).order_by(Cliente.nombre, Cliente.id)
        clientes = sesion.scalars(consulta).all()

        resultados = []
        for cliente in clientes:
            resultados.append({
                "id": cliente.id,
                "nombre": cliente.nombre,
                "correo": cliente.correo,
                "telefono": cliente.telefono
            })

        return resultados


def consultar_equipos(solo_disponibles=False):
    with SessionLocal() as sesion:
        consulta = select(Equipo).order_by(Equipo.nombre, Equipo.id)

        if solo_disponibles:
            consulta = consulta.where(Equipo.stock_disponible > 0)

        equipos = sesion.scalars(consulta).all()

        resultados = []
        for equipo in equipos:
            resultados.append({
                "id": equipo.id,
                "nombre": equipo.nombre,
                "tipo": equipo.tipo,
                "categoria_id": equipo.categoria_id,
                "categoria": equipo.categoria.nombre,
                "precio_diario": equipo.precio_diario,
                "stock_total": equipo.stock_total,
                "stock_disponible": equipo.stock_disponible
            })

        return resultados


def consultar_equipos_disponibles():
    return consultar_equipos(solo_disponibles=True)


def consultar_historial_arriendos(solo_activos=False):
    with SessionLocal() as sesion:
        # Los arriendos más recientes aparecen primero.
        consulta = select(Arriendo).order_by(
            Arriendo.fecha_inicio.desc(), Arriendo.id.desc()
        )

        if solo_activos:
            consulta = consulta.where(Arriendo.estado == "ACTIVO")

        arriendos = sesion.scalars(consulta).all()

        resultados = []
        for arriendo in arriendos:
            resultados.append({
                "id": arriendo.id,
                "equipo_id": arriendo.equipo_id,
                "equipo": arriendo.equipo.nombre,
                "categoria": arriendo.equipo.categoria.nombre,
                "cliente_id": arriendo.cliente_id,
                "cliente": arriendo.cliente.nombre,
                "fecha_inicio": arriendo.fecha_inicio,
                "fecha_fin_prevista": arriendo.fecha_fin_prevista,
                "cantidad": arriendo.cantidad,
                "estado": arriendo.estado,
                # Se muestra el costo guardado al registrar el arriendo.
                "costo_total": arriendo.costo_total
            })

        return resultados


def consultar_arriendos_activos():
    return consultar_historial_arriendos(solo_activos=True)
