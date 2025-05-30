import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import Session, joinedload
from denjyauto.database import SessionLocal
from denjyauto.models.car import Car
from denjyauto.models.repair import Repair
from datetime import datetime

from denjyauto.ui.car_ui import show_repair_details
from denjyauto.ui.widgets import create_scrollable_frame, close_parent_window_and


def income(context):
    win = tk.Toplevel(context.master)
    win.title("Приходи от ремонти за период")
    win.geometry("400x200")
    win.configure(bg="gray80")

    ttk.Label(win, text="От дата (гггг-мм-дд):").pack()
    start_date_var = tk.StringVar(value=str(datetime.today().date()))
    ttk.Entry(win, textvariable=start_date_var, foreground="dodger blue").pack()

    ttk.Label(win, text="До дата (гггг-мм-дд):").pack()
    end_date_var = tk.StringVar(value=str(datetime.today().date()))
    ttk.Entry(win, textvariable=end_date_var, foreground="dodger blue").pack(padx=10, pady=5)


    def calculate_income():
        try:
            start = datetime.strptime(start_date_var.get(), "%Y-%m-%d").date()
            end = datetime.strptime(end_date_var.get(), "%Y-%m-%d").date()
        except ValueError:
            result_label.config(text="Невалиден формат на дата.")
            return

        session: Session = SessionLocal()
        try:
            total_income = (
                session.query(Repair)
                .filter(
                    Repair.repair_date.between(start, end),
                    Repair.is_it_paid == True
                ).with_entities(Repair.repair_price)
                .all()
            )
            print(total_income)
            total = sum([r[0] for r in total_income if r[0] is not None])
            result_label.config(text=f"Общо: {total:.2f} лв.", foreground="red")
        finally:
            session.close()

    ttk.Button(win, text="Изчисли", command=calculate_income).pack(padx=10, pady=5)

    result_label = ttk.Label(win, text="")
    result_label.pack(pady=10)

def list_not_paid_repairs(context):
    win = tk.Toplevel(context.master)
    win.title("Неплатени ремонти")
    win.geometry("600x400")
    win.configure(bg="gray80")

    repairs_frame = create_scrollable_frame(win)
    session: Session = SessionLocal()
    try:
        repairs = session.query(Repair).filter(Repair.is_it_paid == False).options(
            joinedload(Repair.car).joinedload(Car.client)
        ).all()

        if not repairs:
            ttk.Label(win, text="Няма неплатени ремонти.").grid(row=0, column=0, sticky="w")
        else:
            for repair in repairs:
                ttk.Button(
                    repairs_frame,
                    text=f"Клиент: {repair.car.client.name}, Автомобил {repair.car.registration_number}, дата на ремонта: {repair.repair_date}",
                    command=lambda r=repair: show_repair_details(context, r.id, r.car, r.car.client)
                ).pack(anchor="nw", padx=5, pady=5)
    finally:
        session.close()

