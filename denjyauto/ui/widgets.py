from tkinter import Frame, Canvas, Scrollbar, VERTICAL, HORIZONTAL
from tkinter import ttk
import tkinter as tk


def clear_content(container):
    for widget in container.winfo_children():
        widget.destroy()

def create_scrollable_frame(parent, scroll="vertical", use_ttk=True, style_name=None, bg="gray80"):
    container = Frame(parent, bg=bg)
    canvas = Canvas(container, borderwidth=0, highlightthickness=0, bg=bg)

    # Избор между ttk.Frame и tk.Frame
    if use_ttk:
        scrollable_frame = ttk.Frame(canvas, style=style_name or "TFrame")
    else:
        scrollable_frame = tk.Frame(canvas, bg=bg)

    # Добавяне на вътрешната рамка към платното
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_configure)

    # Автоматично разтягане по ширина на вътрешната рамка
    def _resize_scrollable_frame(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", _resize_scrollable_frame)

    # Скролбари
    if scroll in ("vertical", "both"):
        v_scrollbar = ttk.Scrollbar(container, orient=VERTICAL, command=canvas.yview, style="Vertical.TScrollbar")
        canvas.configure(yscrollcommand=v_scrollbar.set)
        v_scrollbar.pack(side="right", fill="y")

    if scroll in ("horizontal", "both"):
        h_scrollbar = ttk.Scrollbar(container, orient=HORIZONTAL, command=canvas.xview, style="Horizontal.TScrollbar")
        canvas.configure(xscrollcommand=h_scrollbar.set)
        h_scrollbar.pack(side="bottom", fill="x")

    canvas.pack(side="left", fill="both", expand=True)
    container.pack(fill="both", expand=True)

    # Скролване с мишка
    def _on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def _on_linux_scroll_up(event): canvas.yview_scroll(-1, "units")
    def _on_linux_scroll_down(event): canvas.yview_scroll(1, "units")

    scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)
    scrollable_frame.bind_all("<Button-4>", _on_linux_scroll_up)
    scrollable_frame.bind_all("<Button-5>", _on_linux_scroll_down)

    return scrollable_frame

def create_copyable_label(parent, text):
    entry = tk.Entry(parent, readonlybackground="gray80", foreground="dodger blue")
    entry.insert(0, text)
    entry.config(state='readonly')
    entry.pack(padx=10, pady=5, fill="x")
    return entry