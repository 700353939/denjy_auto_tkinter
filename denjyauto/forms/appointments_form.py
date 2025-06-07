import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from sqlalchemy.orm import Session
from datetime import datetime
from denjyauto.database import SessionLocal
from denjyauto.models.appointments import Appointment

class AppointmentForm(tk.Toplevel):
    def __init__(self, context, car, reload_callback=None):
        super().__init__(context.master)
        self.title("Записване на преглед")
        self.geometry("300x250")
        self.car = car
        self.reload_callback = reload_callback
        self.configure(bg="gray80")
        self.grab_set()

        ttk.Label(self, text=f"Автомобил: {car.registration_number}").pack(pady=10)

        ttk.Label(self, text="Избери дата:").pack()
        self.date_entry = DateEntry(self, date_pattern="dd-mm-yyyy")
        self.date_entry.pack(pady=5)

        ttk.Label(self, text="Час (напр. 14:00):").pack()
        self.hour_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.hour_var).pack(pady=5)

        ttk.Button(self, text="Запази", command=self.save).pack(pady=15)

    def save(self):
        try:
            selected_date = datetime.strptime(self.date_entry.get(), "%d-%m-%Y").date()
            selected_hour = self.hour_var.get()

            session: Session = SessionLocal()
            appointment = Appointment(date=selected_date, hour=selected_hour, car_id=self.car.id)
            session.add(appointment)
            session.commit()
            session.close()

            messagebox.showinfo("Готово", "Часът за преглед е записан.")
            if self.reload_callback:
                self.reload_callback()
            self.destroy()

        except Exception as e:
            messagebox.showerror("Грешка", str(e))
