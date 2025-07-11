from tkinter import ttk

def apply_custom_style():
    style = ttk.Style()
    style.theme_use("default")

    # Универсален стил за всички ttk widgets
    style.configure(".", background="gray80", foreground="black", font=("Monospace", 10, "bold"))

    # Frame и LabelFrame
    style.configure("TFrame", background="gray80")
    style.configure("TLabelframe", background="gray80", foreground="black")
    style.configure("TLabelframe.Label", background="gray80", foreground="dodger blue", font=("Monospace", 12, "bold"))

    # Label
    style.configure("TLabel", background="gray80", foreground="black")
    style.configure("Blue.TLabel", background="gray80", foreground="dodger blue")

    # Button
    style.configure("TButton", background="gray60", foreground="black", padding=6, relief="flat")
    style.map("TButton",
              background=[("active", "white"), ("pressed", "white")],
              foreground=[("active", "dodger blue"), ("pressed", "black")])

    style.configure("RedText.TButton", background="gray60", foreground="red", padding=6, relief="flat", font=("Monospace", 10))
    style.map("RedText.TButton",
              background=[("active", "white"), ("pressed", "white")],
              foreground=[("active", "red"), ("pressed", "black")])

    # Entry
    style.configure("TEntry", fieldbackground="gray70", foreground="black", insertcolor="black")

    # Text widget
    ttk.Entry.configure = lambda *a, **kw: None  # предотвратява грешка при monkey patch (за съвместимост)

    # Treeview
    style.configure("Treeview", background="gray70", foreground="black",
                    fieldbackground="#gray70", borderwidth=0)
    style.configure("Treeview.Heading", background="gray70", foreground="black", font=("Monospace", 10, "bold"))
    style.map("Treeview", background=[("selected", "gray60")])

    # Scrollbar
    style.configure("Scrollbar", background="gray80", troughcolor="black", arrowcolor="dodger blue")

    style.configure("TCheckbutton",
                    background="gray80",
                    foreground="black",
                    font=("Monospace", 10),
                    )

    style.map("TCheckbutton",
              foreground=[("selected", "dodger blue")],
              indicatorcolor=[("active", "dodger blue"), ("selected", "dodger blue")],
              background=[("active", "gray80")]
              )
