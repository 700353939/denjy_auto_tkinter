import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from denjyauto.database import SessionLocal
from denjyauto.models.client import Client

class EditClientForm(tk.Toplevel):
    def __init__(self, context, client: Client, reload_callback):
        super().__init__(context.master)
        self.client = client
        self.reload_callback = reload_callback
        self.title("Редакция на клиент")
        self.geometry("400x400")
        self.configure(bg="gray80")

        ttk.Label(self, text="Име на клиента:", background="gray80", foreground="black").pack(pady=5)
        self.name_var = tk.StringVar(value=client.name)
        self.name_entry = ttk.Entry(self, textvariable=self.name_var)
        self.name_entry.pack(pady=5, fill="x", padx=10)

        ttk.Label(self, text="Телефон:", background="gray80", foreground="black").pack(pady=5)
        self.phone_var = tk.StringVar(value=client.phone_number)
        self.phone_entry = ttk.Entry(self, textvariable=self.phone_var)
        self.phone_entry.pack(pady=5, fill="x", padx=10)

        ttk.Label(self, text="Бележки:", background="gray80", foreground="black").pack(pady=5)
        self.notes_text = tk.Text(self, height=6, bg="gray70", fg="black", insertbackground="black")
        self.notes_text.pack(pady=5, fill="both", expand=True, padx=10)
        if client.client_notes:
            self.notes_text.insert("1.0", client.client_notes)

        ttk.Button(self, text="Запази", command=self.save_client).pack(pady=10)

    def save_client(self):
        session: Session = SessionLocal()
        try:
            client = session.query(Client).get(self.client.id)
            client.name = self.name_var.get().strip()
            client.lower_name = self.name_var.get().strip().lower()
            client.phone_number = self.phone_var.get().strip()
            client.client_notes = self.notes_text.get("1.0", "end-1c").strip()

            session.commit()
            messagebox.showinfo("Готово", "Клиентът е записан успешно.")

            self.reload_callback()
            self.destroy()

        except Exception as e:
            session.rollback()
            messagebox.showerror("Грешка", str(e))
            self.lift()
            self.focus_force()

        finally:
            session.close()
