import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.models.repair import Repair

class EditRepairForm(tk.Toplevel):
    def __init__(self, master, repair: Repair):
        super().__init__(master)
        self.repair = repair
        self.title("Редакция на ремонт")
        self.geometry("400x400")
        self.configure(bg="#111")

        ttk.Label(self, text="Дата на ремонта:", background="#111", foreground="white").pack(pady=5)
        self.repair_date_var = tk.StringVar(value=repair.repair_date.strftime("%Y-%m-%d"))
        self.repair_date_entry = ttk.Entry(self, textvariable=self.repair_date_var)
        self.repair_date_entry.pack(pady=5, fill="x", padx=10)

        ttk.Label(self, text="Километри при ремонта:", background="#111", foreground="white").pack(pady=5)
        self.repair_km_var = tk.IntVar(value=repair.repair_km)
        self.repair_km_entry = ttk.Entry(self, textvariable=self.repair_km_var)
        self.repair_km_entry.pack(pady=5, fill="x", padx=10)

        ttk.Label(self, text="Видове ремонти:", background="#111", foreground="white").pack(pady=5)
        self.repairs_types_var = tk.StringVar(value=repair.repairs_type_field)
        self.repairs_types_entry = ttk.Entry(self, textvariable=self.repairs_types_var)
        self.repairs_types_entry.pack(pady=5, fill="x", padx=10)

        ttk.Label(self, text="Цена на ремонта:", background="#111", foreground="white").pack(pady=5)
        self.repair_price_var = tk.StringVar(value=str(repair.repair_price))
        self.repair_price_entry = ttk.Entry(self, textvariable=self.repair_price_var)
        self.repair_price_entry.pack(pady=5, fill="x", padx=10)

        ttk.Label(self, text="Бележки:", background="#111", foreground="white").pack(pady=5)
        self.notes_text = tk.Text(self, height=6, bg="#222", fg="white", insertbackground="white")
        self.notes_text.pack(pady=5, fill="both", expand=True, padx=10)
        if repair.repair_notes:
            self.notes_text.insert("1.0", repair.repair_notes)


        ttk.Button(self, text="Запази", command=self.save_repair).pack(pady=10)

    def save_repair(self):
        session: Session = SessionLocal()
        try:
            repair = session.query(Repair).get(self.repair.id)
            repair.repair_date = datetime.strptime(self.repair_date_var.get(), "%Y-%m-%d").date()
            repair.repair_km = self.repair_km_var.get()
            repair.repairs_type_field = self.repairs_types_var.get()
            repair.repair_price = float(self.repair_price_var.get())
            repair.repair_notes = self.notes_text.get("1.0", "end-1c").strip()

            session.commit()
            messagebox.showinfo("Успех", "Автомобилът е записан успешно.")

            self.destroy()

        except Exception as e:
            session.rollback()
            messagebox.showerror("Грешка", str(e))
        finally:
            session.close()
