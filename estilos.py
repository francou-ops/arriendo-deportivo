from tkinter import ttk


# Cambiar estos colores actualiza la apariencia de toda la aplicación.
COLORES = {
    "fondo": "#211C28",
    "superficie": "#2B2533",
    "texto": "#F1EAF7",
    "secundario": "#C2B6CD",
    "acento": "#C1A4DB",
    "texto_acento": "#24192E",
    "acento_activo": "#B296CE",
    "suave": "#3A3045",
    "borde": "#4A3F56",
    "fila": "#302939",
    "seleccion": "#4B3C5A",
    "eliminar": "#E2AAC1",
    "eliminar_fondo": "#402C38",
    "eliminar_activo": "#503545"
}


def configurar_estilos(ventana):
    estilo = ttk.Style(ventana)
    # El tema clam permite aplicar nuestros colores a los controles.
    estilo.theme_use("clam")
    ventana.configure(background=COLORES["fondo"])

    estilo.configure(".", font=("Segoe UI", 10), background=COLORES["superficie"], foreground=COLORES["texto"])
    estilo.configure("TFrame", background=COLORES["superficie"])
    estilo.configure("App.TFrame", background=COLORES["fondo"])
    estilo.configure(
        "Panel.TFrame",
        background=COLORES["superficie"],
        bordercolor=COLORES["borde"],
        lightcolor=COLORES["borde"],
        darkcolor=COLORES["borde"],
        borderwidth=1,
        relief="solid",
    )
    estilo.configure("Linea.TFrame", background=COLORES["borde"])
    estilo.configure("TLabel", background=COLORES["superficie"], foreground=COLORES["texto"])
    estilo.configure("Titulo.TLabel", background=COLORES["fondo"], font=("Segoe UI", 18, "bold"))
    estilo.configure("Subtitulo.TLabel", background=COLORES["fondo"], foreground=COLORES["secundario"])
    estilo.configure(
        "Marca.TLabel",
        background=COLORES["suave"],
        foreground=COLORES["acento"],
        font=("Segoe UI", 17, "bold"),
        padding=(13, 10),
    )
    estilo.configure("TituloVista.TLabel", background=COLORES["superficie"], font=("Segoe UI", 15, "bold"))
    estilo.configure("TituloPanel.TLabel", font=("Segoe UI", 11, "bold"))
    estilo.configure("Ayuda.TLabel", foreground=COLORES["secundario"], font=("Segoe UI", 9))

    estilo.configure(
        "TNotebook",
        background=COLORES["fondo"],
        bordercolor=COLORES["borde"],
        lightcolor=COLORES["borde"],
        darkcolor=COLORES["borde"],
        borderwidth=0,
        tabmargins=(0, 0, 0, 0),
    )
    estilo.configure(
        "TNotebook.Tab",
        background=COLORES["suave"],
        foreground=COLORES["secundario"],
        bordercolor=COLORES["borde"],
        lightcolor=COLORES["borde"],
        darkcolor=COLORES["borde"],
        padding=(18, 9),
        font=("Segoe UI", 10, "bold"),
    )
    estilo.map(
        "TNotebook.Tab",
        background=[("selected", COLORES["superficie"]), ("active", COLORES["seleccion"])],
        foreground=[("selected", COLORES["acento"]), ("active", COLORES["texto"])],
        lightcolor=[("selected", COLORES["borde"]), ("!selected", COLORES["borde"])],
        padding=[("selected", (18, 9)), ("!selected", (18, 9))],
    )

    estilo.configure(
        "TEntry",
        padding=(9, 6),
        background=COLORES["superficie"],
        fieldbackground=COLORES["superficie"],
        foreground=COLORES["texto"],
        insertcolor=COLORES["texto"],
        selectbackground=COLORES["seleccion"],
        selectforeground=COLORES["texto"],
        bordercolor=COLORES["borde"],
        lightcolor=COLORES["borde"],
        darkcolor=COLORES["borde"],
    )
    estilo.map("TEntry", bordercolor=[("focus", COLORES["acento"])], lightcolor=[("focus", COLORES["acento"])])
    estilo.configure(
        "TCombobox",
        padding=(9, 6),
        background=COLORES["superficie"],
        fieldbackground=COLORES["superficie"],
        foreground=COLORES["texto"],
        bordercolor=COLORES["borde"],
        lightcolor=COLORES["borde"],
        darkcolor=COLORES["borde"],
        arrowcolor=COLORES["acento"],
    )
    estilo.map("TCombobox",
        background=[("active", COLORES["suave"]), ("readonly", COLORES["superficie"])],
        fieldbackground=[("readonly", COLORES["superficie"])],
        foreground=[("readonly", COLORES["texto"])],
        bordercolor=[("focus", COLORES["acento"])],
        selectbackground=[("readonly", COLORES["suave"])],
        selectforeground=[("readonly", COLORES["texto"])])
    ventana.option_add("*TCombobox*Listbox.background", COLORES["superficie"])
    ventana.option_add("*TCombobox*Listbox.foreground", COLORES["texto"])
    ventana.option_add("*TCombobox*Listbox.selectBackground", COLORES["seleccion"])
    ventana.option_add("*TCombobox*Listbox.selectForeground", COLORES["texto"])
    ventana.option_add("*TCombobox*Listbox.font", ("Segoe UI", 10))

    estilo.configure(
        "TButton",
        padding=(13, 8),
        background=COLORES["superficie"],
        foreground=COLORES["texto"],
        bordercolor=COLORES["borde"],
        lightcolor=COLORES["borde"],
        darkcolor=COLORES["borde"],
        relief="solid",
        borderwidth=1,
    )
    estilo.map(
        "TButton",
        background=[
            ("disabled", COLORES["fondo"]),
            ("pressed", COLORES["seleccion"]),
            ("active", COLORES["suave"]),
        ],
        foreground=[("disabled", COLORES["secundario"])],
        bordercolor=[("focus", COLORES["acento"]), ("active", COLORES["acento"])],
    )

    estilo.configure(
        "Primario.TButton",
        background=COLORES["acento"],
        foreground=COLORES["texto_acento"],
        bordercolor=COLORES["acento"],
        lightcolor=COLORES["acento"],
        darkcolor=COLORES["acento"],
        font=("Segoe UI", 10, "bold"),
    )
    estilo.map(
        "Primario.TButton",
        background=[
            ("disabled", COLORES["borde"]),
            ("pressed", COLORES["acento_activo"]),
            ("active", COLORES["acento_activo"]),
        ],
        foreground=[("disabled", COLORES["secundario"]), ("!disabled", COLORES["texto_acento"])],
        bordercolor=[("!disabled", COLORES["acento_activo"])],
    )
    estilo.configure(
        "Eliminar.TButton",
        background=COLORES["eliminar_fondo"],
        foreground=COLORES["eliminar"],
        bordercolor=COLORES["borde"],
        lightcolor=COLORES["borde"],
        darkcolor=COLORES["borde"],
    )
    estilo.map(
        "Eliminar.TButton",
        background=[("pressed", COLORES["eliminar_activo"]), ("active", COLORES["eliminar_activo"])],
        foreground=[("!disabled", COLORES["eliminar"])],
    )
    estilo.configure(
        "Discreto.TButton",
        foreground=COLORES["secundario"],
        bordercolor=COLORES["superficie"],
        lightcolor=COLORES["superficie"],
        darkcolor=COLORES["superficie"],
    )

    estilo.configure(
        "Treeview",
        background=COLORES["superficie"],
        fieldbackground=COLORES["superficie"],
        foreground=COLORES["texto"],
        font=("Segoe UI", 10),
        rowheight=34,
        bordercolor=COLORES["borde"],
        lightcolor=COLORES["borde"],
        darkcolor=COLORES["borde"],
        borderwidth=0,
        relief="flat",
    )
    estilo.configure(
        "Treeview.Heading",
        background=COLORES["suave"],
        foreground=COLORES["secundario"],
        font=("Segoe UI", 9, "bold"),
        padding=(10, 7),
        bordercolor=COLORES["borde"],
        lightcolor=COLORES["borde"],
        darkcolor=COLORES["borde"],
        relief="flat",
    )
    estilo.map(
        "Treeview",
        background=[("selected", COLORES["seleccion"])],
        foreground=[("selected", COLORES["texto"])],
        bordercolor=[("focus", COLORES["acento"])],
    )
    estilo.map("Treeview.Heading", background=[("active", COLORES["suave"])])

    estilo.configure(
        "TScrollbar",
        background=COLORES["borde"],
        troughcolor=COLORES["superficie"],
        bordercolor=COLORES["superficie"],
        lightcolor=COLORES["borde"],
        darkcolor=COLORES["borde"],
        arrowcolor=COLORES["secundario"],
        borderwidth=0,
        arrowsize=12,
    )
    estilo.map("TScrollbar", background=[("active", COLORES["seleccion"])])
    estilo.configure(
        "TCheckbutton",
        background=COLORES["superficie"],
        foreground=COLORES["secundario"],
        padding=(3, 5),
        font=("Segoe UI", 9),
        indicatorbackground=COLORES["superficie"],
        upperbordercolor=COLORES["borde"],
        lowerbordercolor=COLORES["borde"],
    )
    estilo.map(
        "TCheckbutton",
        background=[("active", COLORES["superficie"])],
        indicatorbackground=[("selected", COLORES["acento"])],
        indicatorforeground=[("selected", COLORES["texto_acento"])],
    )
