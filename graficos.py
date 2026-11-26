from textwrap import fill

from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from consultar import consultar_historial_arriendos


def ordenar_filas(filas):
    # Primero los que tienen más arriendos; si empatan, por nombre.
    return sorted(filas, key=lambda fila: (-fila[1], fila[0]))


def contar_arriendos_por_categoria():
    conteo = {}

    # Cada fila del historial es una operación, sin importar sus unidades.
    for arriendo in consultar_historial_arriendos():
        categoria = arriendo["categoria"]
        conteo[categoria] = conteo.get(categoria, 0) + 1

    return ordenar_filas(list(conteo.items()))


def contar_arriendos_por_equipo(limite=5):
    conteo = {}
    nombres = {}

    # Se agrupa por ID porque dos equipos pueden tener el mismo nombre.
    for arriendo in consultar_historial_arriendos():
        equipo_id = arriendo["equipo_id"]
        nombres[equipo_id] = arriendo["equipo"]
        conteo[equipo_id] = conteo.get(equipo_id, 0) + 1

    filas = []
    for equipo_id, cantidad in conteo.items():
        etiqueta = f"{nombres[equipo_id]} #{equipo_id}"
        filas.append((etiqueta, cantidad))

    return ordenar_filas(filas)[:limite]


def crear_grafico(filas, titulo):
    if not filas:
        raise ValueError("Todavía no hay arriendos para graficar.")

    # Los nombres largos se dividen en varias líneas.
    etiquetas = [fill(fila[0], 24) for fila in filas]
    valores = [fila[1] for fila in filas]
    posiciones = list(range(len(filas)))

    figura = Figure(figsize=(7, 4))
    ejes = figura.add_subplot()

    barras = ejes.barh(posiciones, valores, color="#2f6f9f")
    ejes.bar_label(barras, padding=3)
    ejes.set_yticks(posiciones, etiquetas)
    ejes.invert_yaxis()  # Deja arriba la barra más grande.
    ejes.set_title(titulo)
    ejes.set_xlabel("Cantidad de arriendos")
    ejes.xaxis.set_major_locator(MaxNLocator(integer=True))
    ejes.margins(x=0.1)
    ejes.spines[["top", "right"]].set_visible(False)
    figura.tight_layout()

    return figura


def crear_grafico_categorias():
    filas = contar_arriendos_por_categoria()
    return crear_grafico(filas, "Arriendos por categoría")


def crear_grafico_equipos():
    filas = contar_arriendos_por_equipo()
    return crear_grafico(filas, "Equipos con mayor número de arriendos")
