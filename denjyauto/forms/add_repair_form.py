import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from datetime import datetime
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.models.repair import Repair

REPAIR_TYPE_OPTIONS = [
    "Смяна на гуми", "Смяна на масло", "Маслен филтър", "Горивен филтър",
    "Въздушен филтър", "Филтър купе", "Ремонт на ходова част",
    "Смяна на съединител", "Ремонт на двигателя", "Диагностика", "Козметичен ремонт",
    "Друг ремонт", "Поръчка на части", "Записване на ден и час",
]

class AddRepairForm(tk.Toplevel):
    def __init__(self, context, car, client, reload_callback=None):
        super().__init__(context.master)
        self.title("Добавяне на ремонт")
        self.car = car
        self.geometry("600x700")
        self.configure(bg="gray80")
        self.reload_callback = reload_callback

        ttk.Label(self, text="Дата:").pack()
        self.date_var = tk.StringVar(value=str(date.today()))
        ttk.Entry(self, textvariable=self.date_var).pack()

        ttk.Label(self, text="Километри:").pack()
        self.repair_km_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.repair_km_var).pack()

        ttk.Label(self, text="Видове ремонт:").pack()
        self.repair_type_vars = {}
        for option in REPAIR_TYPE_OPTIONS:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self,
                                  text=f"{option}: запиши в бележки"
                                  if option in ["Друг ремонт", "Поръчка на части", "Записване на ден и час"]
                                  else f"{option}",
                                  variable=var)
            chk.pack(anchor="w", padx=20)
            self.repair_type_vars[option] = var

        ttk.Label(self, text="Цена (лв):").pack()
        self.price_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.price_var).pack()

        self.is_paid_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self, text="Платено", variable=self.is_paid_var).pack(pady=5)

        ttk.Label(self, text="Бележки:").pack()
        self.notes_text = tk.Text(self, height=4, background="gray70", foreground="black", insertbackground="black")
        self.notes_text.pack()

        ttk.Label(self, text=f"Клиент: {client.name} Aвтомобил: {car.registration_number}",
                  foreground="black"
                  ).pack(anchor="nw", pady=5)

        ttk.Button(self, text="Запази ремонта", command=self.save_repair).pack(pady=10)

    def save_repair(self):
        try:
            selected_types = [t for t, var in self.repair_type_vars.items() if var.get()]
            if not selected_types:
                raise ValueError("Избери поне един вид ремонт.")

            repair_km_text = self.repair_km_var.get()
            if repair_km_text and not repair_km_text.isdigit():
                raise ValueError("Годината трябва да е число.")

            repair_price = self.price_var.get()
            if not repair_price:
                raise ValueError("Въвеждането на цена е задължително.")

            repair = Repair(
                repair_date = datetime.strptime(self.date_var.get(), "%Y-%m-%d").date(),
                repair_km=int(repair_km_text) if repair_km_text else 0,
                repairs_type_field=", ".join(selected_types),
                repair_price=float(repair_price),
                is_it_paid=self.is_paid_var.get(),
                repair_notes=self.notes_text.get("1.0", "end").strip(),
                car_id=self.car.id
            )

            session: Session = SessionLocal()
            session.add(repair)
            session.commit()
            session.refresh(repair)

            messagebox.showinfo("Готово", "Ремонтът е добавен успешно.")

            if self.reload_callback:
                self.reload_callback(repair.id)

            self.destroy()

        except Exception as e:
            messagebox.showerror("Грешка", str(e))
            self.lift()
            self.focus_force()
