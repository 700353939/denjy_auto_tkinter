import tkinter as tk
from tkinter import ttk

from denjyauto.ui.car_ui import search_cars
from denjyauto.ui.income_and_debts_ui import income, list_not_paid_repairs
from denjyauto.ui.widgets import create_scrollable_frame
from denjyauto.ui.clients_ui import load_clients, add_new_client, search_clients
from denjyauto.context import AppContext

class MainWindow:
    def __init__(self, master):
        self.context = AppContext(master)
        master.title("DenjyAuto")

        self.logo_image = tk.PhotoImage(file="images/denjyauto.gif")

        self.start_frame = ttk.Frame(master)
        self.start_frame.pack()

        self.search_bar = ttk.Frame(master)
        self.search_bar.pack(fill="x", padx=10)

        ttk.Button(
            self.start_frame,
            text="ОБНОВИ СПИСЪКА",
            command=lambda: load_clients(self.context)
        ).pack(side="left", pady=10, padx=50, fill="x", expand=True)

        ttk.Button(
            self.start_frame,
            text="НОВ КЛИЕНТ",
            command=lambda: add_new_client(self.context)
        ).pack(side="left", pady=10, padx=10, fill="x", expand=True)

        ttk.Label(
            self.start_frame,
            image=self.logo_image,
            font=("Arial", 16),
            foreground="red"
        ).pack(side="left", anchor="center", pady=10, padx=50)

        ttk.Button(
            self.start_frame,
            text="ПРИХОД ОТ ПЛАТЕНИ РЕМОНТИ",
            command=lambda: income(self.context)
        ).pack(side="left", pady=10, padx=10, fill="x", expand=True)

        ttk.Button(
            self.start_frame,
            text="НЕПЛАТЕНИ РЕМОНТИ",
            command=lambda: list_not_paid_repairs(self.context.master)
        ).pack(side="left", pady=10, padx=10, fill="x", expand=True)

        ttk.Label(self.search_bar,
                  foreground="royal blue",
                  text=f"Търси по име на клиента:",
                  ).pack(side="left", padx=0, pady=10)
        self.search_by_client_var = tk.StringVar()
        self.search_by_client_var.trace_add("write", lambda *args: search_clients(self.context, self.search_by_client_var.get()))
        ttk.Entry(self.search_bar, textvariable=self.search_by_client_var, width=30).pack(side="left", padx=0, pady=10)

        self.search_by_car_var = tk.StringVar()
        self.search_by_car_var.trace_add("write", lambda *args: search_cars(self.context, self.search_by_car_var.get()))
        ttk.Entry(self.search_bar, textvariable=self.search_by_car_var, width=30).pack(side="right", padx=0, pady=10)
        ttk.Label(self.search_bar,
                  foreground="royal blue",
                  text=f"Търси по регистрационен номер на колата:",
                  ).pack(side="right", padx=0, pady=10)

        self.context.content_frame = create_scrollable_frame(master, scroll="both")

        load_clients(self.context)
