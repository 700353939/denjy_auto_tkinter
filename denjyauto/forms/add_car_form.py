import tkinter as tk
from tkinter import ttk
from denjyauto.database import add_car_to_client, get_all_clients

class AddCarForm:
    def __init__(self, parent, client):
        self.window = tk.Toplevel(parent)
        self.window.title("Добавяне на нова автомобил към клиент")
        self.window.geometry("500x500")
        self.window.configure(bg="gray80")
        self.window.grab_set()  # Прави прозореца модален
        self.client = client

        ttk.Label(self.window, text=f"Въведете данни за автомобила на клиент: {self.client.name}", foreground="blue").pack(pady=20)

        ttk.Label(self.window, text="Регистрационен номер:").pack()
        self.license_plate_entry = ttk.Entry(self.window)
        self.license_plate_entry.pack(pady=10)

        ttk.Label(self.window, text="VIN номер:").pack()
        self.vin_entry = ttk.Entry(self.window)
        self.vin_entry.pack(pady=10)

        ttk.Label(self.window, text="Марка:").pack()
        self.brand_entry = ttk.Entry(self.window)
        self.brand_entry.pack(pady=10)

        ttk.Label(self.window, text="Модел:").pack()
        self.model_entry = ttk.Entry(self.window)
        self.model_entry.pack(pady=10)

        ttk.Label(self.window, text="Година:").pack()
        self.year_entry = ttk.Entry(self.window)
        self.year_entry.pack(pady=10)

        ttk.Button(self.window, text="Добави автомобил", command=self.add_car).pack(pady=20)

    def get_clients_for_combobox(self):
        clients = get_all_clients()
        test = []
        for client in clients:
            test.append(f"{client[1]}&{client[0]}")
        print(test)
        return test

    def add_car(self):
        try:
            selected_client_id = self.client.id
            license_plate = self.license_plate_entry.get()
            vin = self.vin_entry.get()
            brand = self.brand_entry.get()
            model = self.model_entry.get()
            year = self.year_entry.get()

            if selected_client_id and license_plate and vin and brand and model and year:
                add_car_to_client(selected_client_id, license_plate, vin, brand, model, year)
                self.window.destroy()  # само затваря прозореца
            else:
                print("Попълнете всички полета.")
        except Exception as e:
            print(f"Грешка при добавяне на автомобил: {e}")
