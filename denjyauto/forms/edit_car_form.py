import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.models.car import Car

class EditCarForm(tk.Toplevel):
    def __init__(self, context, car, client, reload_callback):
        super().__init__(context.master)
        self.car = car
        self.reload_callback = reload_callback
        self.title(f"Редакция на автомобил {car.registration_number}")
        self.geometry("400x400")
        self.configure(bg="gray80")

        ttk.Label(self, text=f"Клиент: {client.name}", foreground="black").pack(anchor="nw", pady=5)

        ttk.Label(self, text="Регистрационен номер:", background="gray80", foreground="black").pack(pady=5)
        self.registration_number_var = tk.StringVar(value=car.registration_number)
        self.registration_number_entry = ttk.Entry(self, textvariable=self.registration_number_var)
        self.registration_number_entry.pack(pady=5, fill="x", padx=10)

        ttk.Label(self, text="VIN:", background="gray80", foreground="black").pack(pady=5)
        self.vin_var = tk.StringVar(value=car.vin)
        self.vin_entry = ttk.Entry(self, textvariable=self.vin_var)
        self.vin_entry.pack(pady=5, fill="x", padx=10)

        ttk.Label(self, text="Марка:", background="gray80", foreground="black").pack(pady=5)
        self.brand_var = tk.StringVar(value=car.brand)
        self.brand_entry = ttk.Entry(self, textvariable=self.brand_var)
        self.brand_entry.pack(pady=5, fill="x", padx=10)

        ttk.Label(self, text="Модел:", background="gray80", foreground="black").pack(pady=5)
        self.model_var = tk.StringVar(value=car.model)
        self.model_entry = ttk.Entry(self, textvariable=self.model_var)
        self.model_entry.pack(pady=5, fill="x", padx=10)

        ttk.Label(self, text="Година:", background="gray80", foreground="black").pack(pady=5)
        self.year_var = tk.StringVar(value=str(car.year) if car.year else "")
        self.year_entry = ttk.Entry(self, textvariable=self.year_var)
        self.year_entry.pack(pady=5, fill="x", padx=10)

        ttk.Button(self, text="Запази", command=self.save_car).pack(pady=10)

    def save_car(self):
        session: Session = SessionLocal()
        try:
            car = session.query(Car).get(self.car.id)
            car.registration_number = self.registration_number_var.get().strip().upper()
            car.lower_registration_number = self.registration_number_var.get().strip().lower()
            car.vin = self.vin_var.get().strip().upper()
            car.brand = self.brand_var.get().strip().capitalize()
            car.model = self.model_var.get().strip().capitalize()

            year_input = self.year_var.get().strip()
            if year_input and not year_input.isdigit():
                raise ValueError("Годината трябва да е цяло число.")
            car.year = int(year_input) if year_input else 0

            session.commit()
            messagebox.showinfo("Готово", "Автомобилът е записан успешно.")

            self.reload_callback()
            self.destroy()

        except Exception as e:
            session.rollback()
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Грешка", "Автомобил с такъв регистрационен номер вече съществува.")
            else:
                messagebox.showerror("Грешка", str(e))
            self.lift()
            self.focus_force()
        finally:
            session.close()
