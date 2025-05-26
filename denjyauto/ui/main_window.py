import tkinter as tk
from tkinter import ttk
from denjyauto.ui.widgets import create_scrollable_frame

from denjyauto.ui.clients_ui import load_clients, open_new_client_form
from denjyauto.ui.income_ui import income


class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("DenjyAuto")

        self.logo_image = tk.PhotoImage(file="images/denjyauto.gif")

        self.start_frame = ttk.Frame(master)
        self.start_frame.pack(side="top", anchor="nw", fill="y", pady=5)

        self.logo = ttk.Label(self.start_frame, image=self.logo_image, font=("Arial", 16), foreground="red")
        self.logo.pack(side="left", pady=10, padx=50)

        self.refresh_button = ttk.Button(self.start_frame, text="    ОБНОВИ СПИСЪКА    ", command=lambda: load_clients(master, self.content_frame))
        self.refresh_button.pack(side="left", pady=10, padx=50)

        self.new_client_button = ttk.Button(self.start_frame, text="    НОВ КЛИЕНТ    ", command=lambda: open_new_client_form(master))
        self.new_client_button.pack(side="left", pady=10, padx=50)

        self.profit_button = ttk.Button(self.start_frame, text="    ПРИХОД    ", command=lambda: income(master))
        self.profit_button.pack(side="left", pady=10, padx=50)

        self.content_frame = create_scrollable_frame(master, scroll="both")

        load_clients(master, self.content_frame)
