from conexion import Base, engine
from models import Categoria, Equipo, Cliente, Arriendo

Base.metadata.create_all(engine)

print("Tablas creadas")
