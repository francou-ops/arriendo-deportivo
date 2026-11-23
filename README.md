# Arriendo deportivo

Sistema de gestión de arriendo de equipamiento deportivo.

## Factory Method

### Por qué se usa

Cada tipo de equipo calcula su costo de forma distinta. Con Factory Method, el código de arriendos no necesita saber qué clase concreta está usando: pide el tipo a la fábrica y llama a `calcular_costo`. Para agregar un tipo nuevo se crea su clase y su fábrica, y se registra en `FABRICAS`, sin cambiar el código de arriendos.

### Partes del patrón

| Parte | Clases |
|---|---|
| Producto | `TipoEquipo` |
| Productos concretos | `Balon`, `Raqueta`, `Bicicleta`, `Proteccion` |
| Creador | `FabricaEquipo` |
| Creadores concretos | `FabricaBalon`, `FabricaRaqueta`, `FabricaBicicleta`, `FabricaProteccion` |

### Conexión con la base de datos

`Equipo.tipo` guarda el tipo como texto (por ejemplo, `bicicleta`). Al calcular un arriendo, `calcular_costo_arriendo` lee ese valor y `crear_tipo_equipo` lo convierte en el objeto correcto.

```python
from conexion import SessionLocal
from factory import calcular_costo_arriendo
from models import Arriendo

with SessionLocal() as session:
    arriendo = session.get(Arriendo, 1)
    costo = calcular_costo_arriendo(arriendo)
```

La función debe llamarse con la sesión abierta, porque `arriendo.equipo` se carga desde la base de datos.

### Reglas de costo

Los días se cuentan incluyendo el día de inicio y el de término, por lo que un arriendo de un solo día cuenta como 1 día.

| Tipo | Fórmula |
|---|---|
| Balón | `precio_diario * dias * cantidad` |
| Raqueta | `precio_diario * dias * cantidad` |
| Bicicleta | `(precio_diario * dias + 10000) * cantidad` (garantía de $10.000 por unidad) |
| Protección | `precio_diario * dias * cantidad * 0.8` (descuento de 20%) |

### Fuentes consultadas

- Claude (Anthropic), asistente de IA: fuente de información sobre Factory Method y apoyo en la redacción del README.
