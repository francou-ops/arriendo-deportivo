from conexion import Base, engine
from models import Categoria, Equipo, Cliente, Arriendo


def crear_tablas():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    crear_tablas()
    print("Tablas creadas")
