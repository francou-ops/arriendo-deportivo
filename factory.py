from abc import ABC, abstractmethod


class TipoEquipo(ABC):
    """Producto: lo que todos los tipos de equipo deben saber hacer."""

    nombre = ""

    @abstractmethod
    def calcular_costo(self, precio_diario, dias, cantidad):
        pass


class Balon(TipoEquipo):
    nombre = "balon"

    def calcular_costo(self, precio_diario, dias, cantidad):
        return precio_diario * dias * cantidad


class Raqueta(TipoEquipo):
    nombre = "raqueta"

    def calcular_costo(self, precio_diario, dias, cantidad):
        return precio_diario * dias * cantidad


class Bicicleta(TipoEquipo):
    nombre = "bicicleta"
    GARANTIA = 10000

    def calcular_costo(self, precio_diario, dias, cantidad):
        return (precio_diario * dias + self.GARANTIA) * cantidad


class Proteccion(TipoEquipo):
    nombre = "proteccion"
    DESCUENTO = 0.8

    def calcular_costo(self, precio_diario, dias, cantidad):
        return precio_diario * dias * cantidad * self.DESCUENTO


class FabricaEquipo(ABC):
    """Creador: declara el factory method."""

    @abstractmethod
    def crear(self):
        pass


class FabricaBalon(FabricaEquipo):
    def crear(self):
        return Balon()

class FabricaRaqueta(FabricaEquipo):
    def crear(self):
        return Raqueta()

class FabricaBicicleta(FabricaEquipo):
    def crear(self):
        return Bicicleta()

class FabricaProteccion(FabricaEquipo):
    def crear(self):
        return Proteccion()


# Diccionario de FABRICAS
FABRICAS = {
    "balon": FabricaBalon(),
    "raqueta": FabricaRaqueta(),
    "bicicleta": FabricaBicicleta(),
    "proteccion": FabricaProteccion(),
}

TIPOS_VALIDOS = list(FABRICAS.keys())

def crear_tipo_equipo(tipo):
    """Recibe el texto guardado en la BD y devuelve el objeto correcto."""
    fabrica = FABRICAS.get(tipo.strip().lower())
    if fabrica is None:
        raise ValueError("Tipo de equipo no válido")
    return fabrica.crear()
