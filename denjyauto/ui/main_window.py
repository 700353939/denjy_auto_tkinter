from tkinter import ttk
from denjyauto.ui.widgets import create_scrollable_frame

from denjyauto.ui.clients_ui import load_clients, open_new_client_form
from denjyauto.ui.income_ui import income


class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("DenjyAuto")
        master.geometry("900x600")

        self.header = ttk.Label(master, text="D E N J Y  A U T O", font=("Arial", 16), foreground="red")
        self.header.pack(pady=10)

        self.toolbar = ttk.Frame(master)
        self.toolbar.pack(pady=5)

        self.content_frame = create_scrollable_frame(master, scroll="both")

        self.refresh_button = ttk.Button(self.toolbar, text="Обнови списъка", command=lambda: load_clients(master, self.content_frame))
        self.refresh_button.grid(row=0, column=0, padx=5)

        self.new_client_button = ttk.Button(self.toolbar, text="Нов клиент", command=lambda: open_new_client_form(master))
        self.new_client_button.grid(row=0, column=1, padx=5)

        self.profit_button = ttk.Button(self.toolbar, text="Приход", command=lambda: income(master))
        self.profit_button.grid(row=0, column=2, padx=5)


        load_clients(master, self.content_frame)
