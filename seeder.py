from datetime import date

from arriendos import devolver_arriendo, registrar_arriendo
from consultar import consultar_categorias
from crear_tablas import crear_tablas
from insertar import insertar_categoria, insertar_cliente, insertar_equipo


def cargar_datos():
    crear_tablas()

    # Si ya hay datos, no se vuelven a cargar.
    if consultar_categorias():
        print("La base ya tiene datos.")
        return

    # Categorías
    futbol = insertar_categoria("Fútbol", "Implementos para fútbol")
    tenis = insertar_categoria("Tenis", "Implementos para tenis")
    ciclismo = insertar_categoria("Ciclismo", "Bicicletas y accesorios")

    # Equipos (hay de los 4 tipos de la fábrica)
    balon = insertar_equipo("Balón Nike N°5", "balon", futbol, 3000, 10)
    canilleras = insertar_equipo("Canilleras Adidas", "proteccion", futbol, 1500, 8)
    raqueta = insertar_equipo("Raqueta Wilson", "raqueta", tenis, 5000, 4)
    bicicleta = insertar_equipo("Bicicleta Trek", "bicicleta", ciclismo, 12000, 3)
    casco = insertar_equipo("Casco Giro", "proteccion", ciclismo, 2000, 6)

    # Clientes
    ana = insertar_cliente("Ana Pérez", "ana@correo.cl", "911111111")
    luis = insertar_cliente("Luis Soto", "luis@correo.cl", "922222222")
    marta = insertar_cliente("Marta Rojas", "marta@correo.cl")

    # Arriendos ya devueltos (historial)
    a1 = registrar_arriendo(balon, ana, date(2026, 11, 1), date(2026, 11, 3), 2)
    a2 = registrar_arriendo(balon, luis, date(2026, 11, 5), date(2026, 11, 6), 1)
    a3 = registrar_arriendo(raqueta, marta, date(2026, 11, 7), date(2026, 11, 9), 1)
    a4 = registrar_arriendo(bicicleta, ana, date(2026, 11, 10), date(2026, 11, 12), 1)
    for arriendo_id in (a1, a2, a3, a4):
        devolver_arriendo(arriendo_id)

    # Arriendos activos
    registrar_arriendo(balon, marta, date(2026, 11, 20), date(2026, 11, 25), 3)
    registrar_arriendo(casco, luis, date(2026, 11, 21), date(2026, 11, 24), 2)
    registrar_arriendo(canilleras, ana, date(2026, 11, 22), date(2026, 11, 26), 2)

    print("Datos de ejemplo cargados.")


if __name__ == "__main__":
    cargar_datos()
