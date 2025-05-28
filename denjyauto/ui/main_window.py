import tkinter as tk
from tkinter import ttk

from denjyauto.ui.income_ui import income
from denjyauto.ui.widgets import create_scrollable_frame
from denjyauto.ui.clients_ui import load_clients, add_new_client
from denjyauto.context import AppContext

class MainWindow:
    def __init__(self, master):
        self.context = AppContext(master)
        master.title("DenjyAuto")

        self.logo_image = tk.PhotoImage(file="images/denjyauto.gif")

        self.start_frame = ttk.Frame(master)
        self.start_frame.pack()

        self.refresh_button = ttk.Button(
            self.start_frame,
            text="ОБНОВИ СПИСЪКА",
            command=lambda: load_clients(self.context)
        )
        self.refresh_button.pack(side="left", pady=10, padx=50, fill="x", expand=True)

        self.logo = ttk.Label(
            self.start_frame,
            image=self.logo_image,
            font=("Arial", 16),
            foreground="red"
        )
        self.logo.pack(side="left", anchor="center", pady=10, padx=50)

        self.new_client_button = ttk.Button(
            self.start_frame,
            text="НОВ КЛИЕНТ",
            command=lambda: add_new_client(self.context)
        )
        self.new_client_button.pack(side="left", pady=10, padx=10, fill="x", expand=True)

        self.profit_button = ttk.Button(
            self.start_frame,
            text="ПРИХОД",
            command=lambda: income(self.context.master)
        )
        self.profit_button.pack(side="left", pady=10, padx=10, fill="x", expand=True)

        self.context.content_frame = create_scrollable_frame(master, scroll="both")

        load_clients(self.context)