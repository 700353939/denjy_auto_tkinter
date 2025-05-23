import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from datetime import datetime
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.models.repair import Repair

REPAIR_TYPE_OPTIONS = [
    "Маслен филтър", "Горивен филтър", "Въздушен филтър", "Филтър купе",
    "Диагностика", "Смяна на масло", "Смяна на гуми",
    "Ремонт на ходова част", "Ремонт на двигателя", "Козметичен ремонт",
    "Записване на ден и час: Запиши в бележки",
    "Друг ремонт: Запиши в бележки"
]

class AddRepairForm(tk.Toplevel):
    def __init__(self, master, car):
        super().__init__(master)
        self.title("Добавяне на ремонт")
        self.car = car
        self.geometry("600x600")
        self.configure(bg="#111")

        ttk.Label(self, text=f"Автомобил: {car.registration_number}", font=("Arial", 12, "bold"), foreground="red").pack(pady=5)

        ttk.Label(self, text="Дата:").pack()
        self.date_var = tk.StringVar(value=str(date.today()))
        ttk.Entry(self, textvariable=self.date_var).pack()

        ttk.Label(self, text="Километри:").pack()
        self.mileage_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.mileage_var).pack()

        ttk.Label(self, text="Видове ремонт:").pack()
        self.repair_type_vars = {}
        for option in REPAIR_TYPE_OPTIONS:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self, text=option, variable=var)
            chk.pack(anchor="w", padx=20)
            self.repair_type_vars[option] = var

        ttk.Label(self, text="Цена (лв):").pack()
        self.price_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.price_var).pack()

        ttk.Label(self, text="Бележки:").pack()
        self.notes_text = tk.Text(self, height=4, background="#111", foreground="white", insertbackground="white")
        self.notes_text.pack()

        ttk.Button(self, text="Запази ремонта", command=self.save_repair).pack(pady=10)

    def save_repair(self):
        try:
            selected_types = [t for t, var in self.repair_type_vars.items() if var.get()]
            if not selected_types:
                raise ValueError("Моля, избери поне един вид ремонт.")

            repair = Repair(
                repair_date = datetime.strptime(self.date_var.get(), "%Y-%m-%d").date(),
                repair_km=int(self.mileage_var.get()),
                repairs_type_field="\n".join(selected_types),
                repair_price=float(self.price_var.get()),
                repair_notes=self.notes_text.get("1.0", "end").strip(),
                car_id=self.car.id
            )

            session: Session = SessionLocal()
            session.add(repair)
            session.commit()
            session.close()

            messagebox.showinfo("Готово", "Ремонтът е добавен успешно.")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Грешка", str(e))
