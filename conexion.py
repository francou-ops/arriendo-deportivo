from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///arriendos.db")


# SQLite no revisa las claves foráneas por defecto.
@event.listens_for(engine, "connect")
def activar_claves_foraneas(conexion, _):
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
