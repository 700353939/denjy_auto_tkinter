import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.forms.add_car_form import AddCarForm
from denjyauto.forms.add_repair_form import AddRepairForm
from denjyauto.forms.edit_car_form import EditCarForm
from denjyauto.models.car import Car
from denjyauto.models.repair import Repair
from denjyauto.ui.widgets import create_copyable_label, create_scrollable_frame

def add_new_car_to_client(master, client):
    AddCarForm(master, client)

def show_car_details(master, car, client_name):

    win = tk.Toplevel(master)
    win.title(f"Клиент: {client_name}, автомобил: {car.registration_number}")
    win.configure(background="#111")
    win.geometry("600x600")

    create_copyable_label(win, text=f"Рег. номер: {car.registration_number}")
    create_copyable_label(win, text=f"VIN: {car.vin}")
    create_copyable_label(win, text=f"Марка: {car.brand}")
    create_copyable_label(win, text=f"Модел: {car.model}")
    create_copyable_label(win, text=f"Година: {car.year}")

    cars_frame = ttk.Frame(win, padding=10 )
    cars_frame.pack(side="top", fill="y", pady=5)

    ttk.Button(
        cars_frame,
        text="ДОБАВИ РЕМОНТ",
        command=lambda: AddRepairForm(win, car)
    ).pack(side="left", pady=10, padx=10)

    ttk.Button(
        cars_frame,
        text="РЕДАКТИРАЙ АВТОМОБИЛА",
        style="RedText.TButton",
        command=lambda c=car: edit_car(master, c, client_name)
    ).pack(side="left", pady=10, padx=10)

    ttk.Button(
        cars_frame,
        text="ИЗТРИЙ АВТОМОБИЛА",
        style="RedText.TButton",
        command=lambda c=car: delete_car(c)
    ).pack(side="left", pady=10, padx=10)


    repairs_frame = create_scrollable_frame(win)

    session: Session = SessionLocal()
    try:
        repairs = session.query(Repair).filter_by(car_id=car.id).all()
        if not repairs:
            ttk.Label(repairs_frame, text="Няма регистрирани ремонти.").grid(row=0, column=0, sticky="w")
        else:
            for i, repair in enumerate(repairs):
                row = i // 4
                column = i % 4
                ttk.Button(
                    repairs_frame,
                    text=f"Ремонт: {repair.repair_date}",
                    command=lambda r=repair: show_repair_details(master, r)
                ).grid(row=row, column=column, padx=5, pady=5, sticky="w")

    finally:
        session.close()


def edit_car(master, car, client_name):
    EditCarForm(master, car, reload_callback=lambda: show_car_details(master, car, client_name))


def delete_car(car, reload_callback=None):
    confirm = messagebox.askyesno("Потвърждение",
                                  f"Сигурен ли си, че искаш да изтриеш автомобил '{car.registration_number}' и всички свързани данни?")
    if not confirm:
        return

    session: Session = SessionLocal()
    try:
        car = session.query(Car).get(car.id)
        session.delete(car)
        session.commit()
        messagebox.showinfo("Успех", f"Автомобилът '{car.registration_number}' е изтрит.")
        if reload_callback:
            reload_callback()
    except Exception as e:
        session.rollback()
        messagebox.showerror("Грешка", f"Неуспешно изтриване: {e}")
    finally:
        session.close()


def show_repair_details(master, repair):
    win = tk.Toplevel(master)
    win.configure(bg="#111")
    win.title(f"ДАТА НА РЕМОНТА: {repair.repair_date}")
    ttk.Label(win, text=f"КИЛОМЕТРИ ПРИ РЕМОНТА: {repair.repair_km}").pack(padx=10, pady=5)
    ttk.Label(win, text=f"РЕМОНТИ: \n{repair.repairs_type_field}").pack(padx=10, pady=5)
    ttk.Label(win, text=f"БЕЛЕЖКИ: {repair.repair_notes}").pack(padx=10, pady=5)
    ttk.Label(win, text=f"ЦЕНА НА РЕМОНТА: {repair.repair_price}").pack(padx=10, pady=5)


def edit_repair():
    pass


def delete_repair():
    pass