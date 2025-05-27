import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.database import add_car_to_client, get_all_clients
from denjyauto.models.car import Car


class AddCarForm:
    def __init__(self, parent, client, reload_callback=None):
        self.window = tk.Toplevel(parent)
        self.window.title("Добавяне на нова автомобил към клиент")
        self.window.geometry("500x500")
        self.window.configure(bg="gray80")
        self.window.grab_set()  # Прави прозореца модален
        self.client = client
        self.reload_callback = reload_callback

        ttk.Label(self.window, text=f"Въведете данни за автомобила на клиент: {self.client.name}", foreground="dodger blue").pack(pady=20)

        ttk.Label(self.window, text="Регистрационен номер:").pack()
        self.registration_number_entry = ttk.Entry(self.window)
        self.registration_number_entry.pack(pady=10)

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
            registration_number = self.registration_number_entry.get()
            vin = self.vin_entry.get()
            brand = self.brand_entry.get()
            model = self.model_entry.get()
            year = self.year_entry.get()

            if selected_client_id and registration_number and vin and brand and model and year:
                add_car_to_client(selected_client_id, registration_number, vin, brand, model, year)

                session: Session = SessionLocal()
                car = session.query(Car).filter_by(
                    registration_number=registration_number,
                    vin=vin,
                    brand=brand,
                    model=model,
                    year = year).first()
                session.close()

                self.reload_callback(car.id)
                self.window.destroy()

            else:
                messagebox.showinfo("Грешка", "Попълнете всички полета.")
        except Exception as e:
            messagebox.showerror("Грешка", str(e))
