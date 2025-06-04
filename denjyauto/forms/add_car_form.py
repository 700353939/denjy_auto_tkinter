import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.models.car import Car

class AddCarForm(tk.Toplevel):
    def __init__(self, context, client, reload_callback=None):
        super().__init__(context.master)
        self.title("Добавяне на нов автомобил към клиент")
        self.geometry("500x500")
        self.configure(bg="gray80")
        self.grab_set()

        self.client = client
        self.reload_callback = reload_callback

        ttk.Label(self, text=f"Въведете данни за автомобила на клиент: {self.client.name}",
                  foreground="dodger blue").pack(pady=20)

        self.registration_number_entry = self._create_labeled_entry("Регистрационен номер:")
        self.vin_entry = self._create_labeled_entry("VIN номер:")
        self.brand_entry = self._create_labeled_entry("Марка:")
        self.model_entry = self._create_labeled_entry("Модел:")
        self.year_entry = self._create_labeled_entry("Година:")

        ttk.Button(self, text="Добави автомобил", command=self.add_car).pack(pady=20)

    def _create_labeled_entry(self, label_text):
        ttk.Label(self, text=label_text).pack()
        entry = ttk.Entry(self)
        entry.pack(pady=10)
        return entry

    def add_car(self):
        try:
            year_text = self.year_entry.get()
            if year_text and not year_text.isdigit():
                raise ValueError("Годината трябва да е число.")

            car = Car(
                client_id=self.client.id,
                registration_number=self.registration_number_entry.get().upper(),
                lower_registration_number=self.registration_number_entry.get().lower(),
                vin=self.vin_entry.get(),
                brand=self.brand_entry.get(),
                model=self.model_entry.get(),
                year=int(year_text) if year_text else 0
            )

            if not car.registration_number:
                raise ValueError("Регистрационният номер е задължителен.")

            session: Session = SessionLocal()
            session.add(car)
            session.commit()
            session.refresh(car)  # получаваме car.id от базата

            messagebox.showinfo("Готово", "Автомобилът е добавен успешно.")

            if self.reload_callback:
                self.reload_callback(car.id)

            self.destroy()

        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Грешка", "Автомобил с такъв регистрационен номер вече съществува.")
            else:
                messagebox.showerror("Грешка", str(e))
