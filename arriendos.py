from datetime import date

from conexion import SessionLocal
from factory import calcular_costo_arriendo
from models import Arriendo, Cliente, Equipo


def registrar_arriendo(equipo_id, cliente_id, fecha_inicio, fecha_fin_prevista, cantidad):
    if not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError("La cantidad debe ser un entero mayor que cero.")
    if not isinstance(fecha_inicio, date) or not isinstance(fecha_fin_prevista, date):
        raise ValueError("Las fechas no son válidas.")
    if fecha_fin_prevista < fecha_inicio:
        raise ValueError("La fecha de término no puede ser anterior a la fecha de inicio.")

    with SessionLocal() as session:
        equipo = session.get(Equipo, equipo_id)
        cliente = session.get(Cliente, cliente_id)

        if equipo is None:
            raise ValueError("No existe un equipo con ese ID.")
        if cliente is None:
            raise ValueError("No existe un cliente con ese ID.")
        if cantidad > equipo.stock_disponible:
            raise ValueError("No hay suficiente stock disponible.")

        arriendo = Arriendo(
            equipo=equipo,
            cliente=cliente,
            fecha_inicio=fecha_inicio,
            fecha_fin_prevista=fecha_fin_prevista,
            cantidad=cantidad,
            estado="ACTIVO"
        )

        # Se guarda el costo para que no cambie si después se edita el equipo.
        arriendo.costo_total = round(calcular_costo_arriendo(arriendo))

        # El arriendo y el descuento de stock se guardan en el mismo commit.
        equipo.stock_disponible -= cantidad
        session.add(arriendo)
        session.commit()
        return arriendo.id


def devolver_arriendo(arriendo_id):
    with SessionLocal() as session:
        arriendo = session.get(Arriendo, arriendo_id)

        if arriendo is None:
            raise ValueError("No existe un arriendo con ese ID.")
        if arriendo.estado != "ACTIVO":
            raise ValueError("Este arriendo ya fue devuelto.")

        # El cambio de estado y la restitución se guardan en el mismo commit.
        arriendo.estado = "DEVUELTO"
        arriendo.equipo.stock_disponible += arriendo.cantidad
        session.commit()
        return arriendo.id
