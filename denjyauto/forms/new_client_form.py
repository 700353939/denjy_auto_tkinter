import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import sessionmaker
from denjyauto.database import engine
from denjyauto.models.client import Client
from denjyauto.models.car import Car

Session = sessionmaker(bind=engine)

class NewClientForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Нов клиент и автомобил")
        self.geometry("400x400")
        self.configure(bg="gray80")

        # Client model
        self.name_entry = self._create_labeled_entry("Име на клиент")
        self.phone_entry = self._create_labeled_entry("Телефон")
        ttk.Label(self, text="Бележки:", foreground="dodger blue").pack()
        self.notes_text = tk.Text(self, height=3, background="gray70", foreground="black", insertbackground="black")
        self.notes_text.pack()

        # Car model
        self.reg_number_entry = self._create_labeled_entry("Рег. номер")
        self.vin_entry = self._create_labeled_entry("VIN")
        self.brand_entry = self._create_labeled_entry("Марка")
        self.model_entry = self._create_labeled_entry("Модел")
        self.year_entry = self._create_labeled_entry("Година")

        save_button = ttk.Button(self, text="Запази", command=self.save_client)
        save_button.pack(pady=10)

    def _create_labeled_entry(self, label_text):
        label = ttk.Label(self, text=label_text, foreground="dodger blue")
        label.pack()
        entry = ttk.Entry(self)
        entry.pack()
        return entry

    def save_client(self):
        session = Session()
        try:
            client = Client(
                name=self.name_entry.get(),
                phone_number=self.phone_entry.get(),
                client_notes=self.notes_text.get("1.0", "end").strip(),
            )
            session.add(client)
            session.flush()  # За да получим client.id преди да commit-нем

            car = Car(
                registration_number=self.reg_number_entry.get().upper(),
                vin=self.vin_entry.get().upper(),
                brand=self.brand_entry.get().capitalize(),
                model=self.model_entry.get().capitalize(),
                year=int(self.year_entry.get()),
                client_id=client.id
            )
            session.add(car)

            session.commit()
            messagebox.showinfo("Успех", "Клиентът и автомобила са записани.")
            self.destroy()
        except Exception as e:
            session.rollback()
            messagebox.showerror("Грешка", str(e))
        finally:
            session.close()
