import tkinter as tk
from denjyauto.path_utils import resource_path
from denjyauto.database import init_db, SessionLocal
from denjyauto.ui.main_window import MainWindow
from denjyauto.ui.styles import apply_custom_style

def run():
    init_db()
    session = SessionLocal()
    root = tk.Tk()
    root.state("zoomed")
    root.configure(background="gray80")
    app = MainWindow(root)
    apply_custom_style()
    root.iconphoto(False, tk.PhotoImage(file=resource_path("images/denjyauto.gif")))
    root.mainloop()

if __name__ == '__main__':
    run()