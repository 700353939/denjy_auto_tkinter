from tkinter import Frame, Canvas, Scrollbar, VERTICAL, HORIZONTAL
from tkinter import ttk
import tkinter as tk


def clear_content(container):
    for widget in container.winfo_children():
        widget.destroy()

def create_scrollable_frame(parent, scroll="vertical"):
    container = Frame(parent, bg="#111")  # черен фон
    canvas = Canvas(container, borderwidth=0, background="#111", highlightthickness=0)

    scrollable_frame = ttk.Frame(canvas, style="TFrame")  # стилът трябва да е дефиниран с черен фон

    def _on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", _on_configure)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    if scroll in ("vertical", "both"):
        v_scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview, bg="#111", troughcolor="#111")
        canvas.configure(yscrollcommand=v_scrollbar.set)
        v_scrollbar.pack(side="right", fill="y")

    if scroll in ("horizontal", "both"):
        h_scrollbar = Scrollbar(container, orient=HORIZONTAL, command=canvas.xview, bg="#111", troughcolor="#111")
        canvas.configure(xscrollcommand=h_scrollbar.set)
        h_scrollbar.pack(side="bottom", fill="x")

    canvas.pack(side="left", fill="both", expand=True)
    container.pack(fill="both", expand=True)

    # Поддръжка на скролване с мишка
    def _on_mousewheel(event):
        if scroll in ("vertical", "both"):
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def _on_linux_scroll_up(event):
        canvas.yview_scroll(-1, "units")

    def _on_linux_scroll_down(event):
        canvas.yview_scroll(1, "units")

    scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)
    scrollable_frame.bind_all("<Button-4>", _on_linux_scroll_up)
    scrollable_frame.bind_all("<Button-5>", _on_linux_scroll_down)

    return scrollable_frame

def create_copyable_label(parent, text):
    entry = tk.Entry(parent, readonlybackground="#111", foreground="red")
    entry.insert(0, text)
    entry.config(state='readonly')
    entry.pack(padx=10, pady=5, fill="x")
    return entry