import tkinter as tk
from denjyauto.database import init_db, SessionLocal
from denjyauto.ui.main_window import MainWindow

# Основен код за стартиране
def run():
    init_db()
    session = SessionLocal()
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    run()