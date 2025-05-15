from tkinter import ttk

def apply_custom_style():
    style = ttk.Style()
    style.theme_use("default")

    # Универсален стил за всички ttk widgets
    style.configure(".", background="#111", foreground="white", font=("Monospace", 10))

    # Frame и LabelFrame
    style.configure("TFrame", background="#111")
    style.configure("TLabelframe", background="#111", foreground="white")
    style.configure("TLabelframe.Label", background="#111", foreground="red", font=("Monospace", 10, "bold"))

    # Label
    style.configure("TLabel", background="#111", foreground="white")

    # Button
    style.configure("TButton", background="#222", foreground="white", padding=6, relief="flat")
    style.map("TButton",
              background=[("active", "#444"), ("pressed", "#000")],
              foreground=[("active", "red"), ("pressed", "white")])

    # Entry
    style.configure("TEntry", fieldbackground="#111", foreground="white", insertcolor="white")

    # Text widget – това е от tk, не ttk
    ttk.Entry.configure = lambda *a, **kw: None  # предотвратява грешка при monkey patch (за съвместимост)

    # Treeview
    style.configure("Treeview", background="#222", foreground="white",
                    fieldbackground="#222", borderwidth=0)
    style.configure("Treeview.Heading", background="#333", foreground="white", font=("Monospace", 10, "bold"))
    style.map("Treeview", background=[("selected", "#555")])

    # Scrollbar
    style.configure("Scrollbar", background="#111", troughcolor="white", arrowcolor="red")

    style.configure("TCheckbutton",
                    background="#111",
                    foreground="white",
                    font=("Monospace", 10),
                    )

    style.map("TCheckbutton",
              foreground=[("active", "red"), ("selected", "red")],
              indicatorcolor=[("active", "red"), ("selected", "red")],
              background=[("active", "#111")]
              )
