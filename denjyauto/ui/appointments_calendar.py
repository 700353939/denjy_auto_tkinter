from tkcalendar import Calendar
from tkinter import ttk, messagebox
import tkinter as tk
from sqlalchemy.orm import Session, joinedload
from denjyauto.database import SessionLocal
from denjyauto.models.appointments import Appointment
from datetime import datetime

from denjyauto.models.car import Car

def open_calendar_window(context):
    top = tk.Toplevel(context.master)
    top.title("Календар с прегледи")
    top.geometry("400x400")
    top.configure(bg="gray80")

    cal = Calendar(top, selectmode="day", date_pattern="dd-mm-yyyy")
    cal.pack(pady=20)

    session: Session = SessionLocal()
    appointments = session.query(Appointment).options(
        joinedload(Appointment.car).joinedload(Car.client)
    ).all()
    session.close()

    grouped = {}
    for appt in appointments:
        key = appt.date.strftime("%d-%m-%Y")
        if key not in grouped:
            grouped[key] = []
        grouped[key].append((
            appt.car.client.name,
            appt.car.client.phone_number,
            appt.car.registration_number,
            appt.hour
        ))

    # Colored date
    for date_str in grouped:
        try:
            date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
            cal.calevent_create(date_obj, 'Преглед', 'review')
        except Exception:
            continue

    cal.tag_config('review', background='red', foreground='white')

    info_frame = ttk.Frame(top)
    info_frame.pack(fill="both", expand=True)

    def on_date_selected(event):

        selected_date = cal.get_date()

        for widget in info_frame.winfo_children():
            widget.destroy()

        if selected_date in grouped:
            ttk.Label(info_frame,
                      text=f"Прегледи за {selected_date}\n"
                           +"\n"
                           + "\n \n".join(
                          f"{name}, {phone}, {reg} - {hour}ч." for name, phone, reg, hour in grouped[selected_date]),
                      foreground="dodger blue"
                      ).pack(anchor="nw", pady=5, padx=10)
        else:
            ttk.Label(info_frame,
                      text=f"Няма прегледи за {selected_date}",
                      foreground="dodger blue"
                      ).pack(anchor="nw", pady=5, padx=10)

    cal.bind("<<CalendarSelected>>", on_date_selected)

def delete_appointment(appointment, reload_callback=None):
    confirm = messagebox.askyesno("Потвърждение",
                                  f"Сигурен ли си, че искаш да изтриеш насроченият преглед.")
    if not confirm:
        return

    session: Session = SessionLocal()
    try:
        appointment = session.query(Appointment).get(appointment.id)
        session.delete(appointment)
        session.commit()
        messagebox.showinfo("Готово", f"Прегледът е изтрит.")
        if reload_callback:
            reload_callback()
    except Exception as e:
        session.rollback()
        messagebox.showerror("Грешка", f"Неуспешно изтриване: {e}")
    finally:
        session.close()