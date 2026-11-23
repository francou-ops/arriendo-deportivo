from datetime import date
from sqlalchemy import String, Integer, Float, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from conexion import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    descripcion: Mapped[str] = mapped_column(String(200), nullable=True)

    equipos: Mapped[list["Equipo"]] = relationship(back_populates="categoria") # Relación con la clase Equipo


class Equipo(Base):
    __tablename__ = "equipo"

    __table_args__ = (
        CheckConstraint("precio_diario > 0", name="check_precio"),
        CheckConstraint("stock_total >= 0", name="check_stock_total"),
        CheckConstraint("stock_disponible >= 0", name="check_stock_disponible"),
        CheckConstraint("stock_disponible <= stock_total", name="check_disponible_total"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False) # Tipo de objeto EJ: Balón etc.
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categoria.id"), nullable=False) # Categoría de Deporte EJ: Fútbol
    precio_diario: Mapped[float] = mapped_column(Float, nullable=False)
    stock_total: Mapped[int] = mapped_column(Integer, nullable=False)
    stock_disponible: Mapped[int] = mapped_column(Integer, nullable=False)

    categoria: Mapped["Categoria"] = relationship(back_populates="equipos") # Relación con la clase Categoria
    arriendos: Mapped[list["Arriendo"]] = relationship(back_populates="equipo") # Relación con la clase Arriendo


class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    telefono: Mapped[str] = mapped_column(String(15), nullable=True)

    arriendos: Mapped[list["Arriendo"]] = relationship(back_populates="cliente") # Relación con la clase Arriendo


class Arriendo(Base):
    __tablename__ = "arriendo"

    __table_args__ = (
        CheckConstraint("cantidad > 0", name="check_cantidad"),
        CheckConstraint("estado IN ('ACTIVO', 'DEVUELTO')", name="check_estado"),
        CheckConstraint("fecha_fin_prevista >= fecha_inicio", name="check_fechas"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    equipo_id: Mapped[int] = mapped_column(ForeignKey("equipo.id"), nullable=False)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"), nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin_prevista: Mapped[date] = mapped_column(Date, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    estado: Mapped[str] = mapped_column(String(10), nullable=False, default="ACTIVO")
    costo_total: Mapped[float] = mapped_column(Float, nullable=False) # Costo guardado al registrar el arriendo

    equipo: Mapped["Equipo"] = relationship(back_populates="arriendos") # Relación con la clase Equipo
    cliente: Mapped["Cliente"] = relationship(back_populates="arriendos") # Relación con la clase Cliente
