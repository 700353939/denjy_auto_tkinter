import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.models.repair import Repair
from datetime import datetime


def income(master):
    win = tk.Toplevel(master)
    win.title("Приходи от ремонти за период")
    win.geometry("400x200")
    win.configure(bg="#111")

    ttk.Label(win, text="От дата (гггг-мм-дд):").pack()
    start_date_var = tk.StringVar(value=str(datetime.today().date()))
    ttk.Entry(win, textvariable=start_date_var, foreground="red").pack()

    ttk.Label(win, text="До дата (гггг-мм-дд):").pack()
    end_date_var = tk.StringVar(value=str(datetime.today().date()))
    ttk.Entry(win, textvariable=end_date_var, foreground="red").pack(padx=10, pady=5)


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
                .filter(Repair.repair_date.between(start, end))
                .with_entities(Repair.repair_price)
                .all()
            )
            total = sum([r[0] for r in total_income if r[0] is not None])
            result_label.config(text=f"Общо: {total:.2f} лв.", foreground="red")
        finally:
            session.close()

    ttk.Button(win, text="Изчисли", command=calculate_income).pack(padx=10, pady=5)

    result_label = ttk.Label(win, text="")
    result_label.pack(pady=10)
