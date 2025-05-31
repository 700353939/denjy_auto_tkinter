import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import sessionmaker
from denjyauto.database import engine
from denjyauto.models.client import Client
from denjyauto.models.car import Car

Session = sessionmaker(bind=engine)

class NewClientForm(tk.Toplevel):
    def __init__(self, context, on_client_added_callback):
        super().__init__(context.master)
        self.title("Нов клиент и автомобил")
        self.geometry("400x500")
        self.configure(bg="gray80")
        self.on_client_added_callback = on_client_added_callback

        # Client model
        self.name_entry = self._create_labeled_entry("Име на клиент")
        self.phone_entry = self._create_labeled_entry("Телефон")
        ttk.Label(self, text="Бележки:", foreground="dodger blue").pack(padx=10, pady=5)
        self.notes_text = tk.Text(self, height=3, background="gray70", foreground="black", insertbackground="black")
        self.notes_text.pack()

        ttk.Label(self, text=f"Данни за автомобила", foreground="black").pack(padx=10, pady=5)
        self.reg_number_entry = self._create_labeled_entry("Рег. номер")
        self.vin_entry = self._create_labeled_entry("VIN")
        self.brand_entry = self._create_labeled_entry("Марка")
        self.model_entry = self._create_labeled_entry("Модел")
        self.year_entry = self._create_labeled_entry("Година")

        save_button = ttk.Button(self, text="Запази", command=self.save_client)
        save_button.pack(pady=10)

    def _create_labeled_entry(self, label_text):
        label = ttk.Label(self, text=label_text, foreground="dodger blue")
        label.pack(padx=10, pady=5)
        entry = ttk.Entry(self)
        entry.pack()
        return entry

    def save_client(self):
        session = Session()
        try:
            name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            notes = self.notes_text.get("1.0", "end").strip()
            reg_num = self.reg_number_entry.get().strip().upper()
            vin = self.vin_entry.get().strip().upper()
            brand = self.brand_entry.get().strip().capitalize()
            model = self.model_entry.get().strip().capitalize()
            year_str = self.year_entry.get().strip() if self.year_entry.get().strip() else 0

            if not all([name, reg_num]):
                raise ValueError("Полетата име и регистрационен номер са задължителни.")

            if year_str and not year_str.isdigit():
                raise ValueError("Годината трябва да е цяло число.")

            client = Client(name=name, lower_name=name.lower(), phone_number=phone, client_notes=notes)
            session.add(client)
            session.flush()

            car = Car(
                registration_number=reg_num,
                lower_registration_number=reg_num.lower(),
                vin=vin,
                brand=brand,
                model=model,
                year=int(year_str),
                client_id=client.id
            )
            session.add(car)

            session.commit()
            messagebox.showinfo("Успех", "Клиентът и автомобилът са записани.")

            if self.on_client_added_callback:
                self.on_client_added_callback()

            self.destroy()

        except Exception as e:
            session.rollback()
            messagebox.showerror("Грешка", str(e))
        finally:
            session.close()
