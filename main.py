from crear_tablas import crear_tablas
from interfaz import crear_ventana_principal


def main():
    crear_tablas()

    ventana = crear_ventana_principal()
    ventana.mainloop()


if __name__ == "__main__":
    main()
