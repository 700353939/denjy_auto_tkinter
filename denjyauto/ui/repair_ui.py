import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.forms.add_repair_form import AddRepairForm
from denjyauto.forms.edit_repair_form import EditRepairForm
from denjyauto.models.repair import Repair
from denjyauto.context import AppContext
from denjyauto.ui.widgets import close_parent_window_and

def add_repair_to_car(context: AppContext, car, client):
    AddRepairForm(context, car, client, reload_callback=lambda repair_id: show_repair_details(context, repair_id, car, client))

def show_repair_details(context: AppContext, repair_id, car, client):
    from denjyauto.ui.car_ui import show_car_details

    session: Session = SessionLocal()
    try:
        repair = session.query(Repair).get(repair_id)
        if not car:
            messagebox.showerror("Грешка", "Автомобилът не е намерен.")
            return
    finally:
        session.close()

    win = tk.Toplevel(context.master)
    win.configure(bg="gray80")
    win.geometry("500x600")
    win.title(f"РЕМОНТ")

    ttk.Label(win, text=f"КЛИЕНТ: {client.name}").pack(anchor="n", padx=10, pady=5)
    ttk.Label(win, text=f"Телефон: {client.phone_number}").pack(anchor="n", padx=10, pady=5)
    ttk.Label(win, text=f"АВТОМОБИЛ: {car.registration_number}").pack(anchor="n", padx=10, pady=5)
    ttk.Label(win, text=f"ДАТА: {repair.repair_date}").pack(anchor="nw", padx=10, pady=5)

    repair_km = "" if repair.repair_km == 0 else repair.repair_km
    ttk.Label(win, text=f"КИЛОМЕТРИ ПРИ РЕМОНТА: {repair_km}").pack(anchor="nw",padx=10, pady=5)

    ttk.Label(win, text=f"РЕМОНТИ: {repair.repairs_type_field}", wraplength=500, justify="left").pack(anchor="nw",padx=10, pady=5)
    ttk.Label(win, text=f"БЕЛЕЖКИ: {repair.repair_notes}", wraplength=500, justify="left").pack(anchor="nw",padx=10, pady=5)
    ttk.Label(win, text=f"ЦЕНА НА РЕМОНТА: {repair.repair_price}").pack(anchor="nw",padx=10, pady=5)

    paid_bool = "Да" if repair.is_it_paid else "Не"
    color = "dodger blue" if repair.is_it_paid else "red"
    ttk.Label(win, text=f"Платено: {paid_bool}", foreground=color).pack(anchor="nw",padx=10, pady=5)


    repair_buttons_frame = ttk.Frame(win, padding=10 )
    repair_buttons_frame.pack(side="top", fill="y", pady=5)

    ttk.Button(
        repair_buttons_frame,
        text="РЕДАКТИРАЙ РЕМОНТА",
        style="TButton",
        command=lambda r=repair: close_parent_window_and(
            edit_repair,
            repair_buttons_frame,
            context,
            r.id,
            car,
            client)
    ).pack(side="left", pady=10, padx=10)

    ttk.Button(
        repair_buttons_frame,
        text="ИЗТРИЙ РЕМОНТА",
        style="RedText.TButton",
        command=lambda r=repair: close_parent_window_and(
            delete_repair,
            repair_buttons_frame,
            r,
            reload_callback=lambda: show_car_details(context, car.id, client))
    ).pack(side="left", pady=10, padx=10)


def edit_repair(context: AppContext, repair_id, car, client):
    session: Session = SessionLocal()
    try:
        repair = session.query(Repair).get(repair_id)
        if not repair:
            messagebox.showerror("Грешка", "Ремонтът не е намерен.")
            return
    finally:
        session.close()
    EditRepairForm(context, repair, car, client, reload_callback=lambda: show_repair_details(context, repair.id, car, client))

def delete_repair(repair, reload_callback=None):
    confirm = messagebox.askyesno("Потвърждение",
                                  f"Сигурен ли си, че искаш да изтриеш ремонта на дата '{repair.repair_date}'?")
    if not confirm:
        return

    session: Session = SessionLocal()
    try:
        repair = session.query(Repair).get(repair.id)
        session.delete(repair)
        session.commit()
        messagebox.showinfo("Готово", f"Ремонтът е изтрит.")
        if reload_callback:
            reload_callback()
    except Exception as e:
        session.rollback()
        messagebox.showerror("Грешка", f"Неуспешно изтриване: {e}")
    finally:
        session.close()


