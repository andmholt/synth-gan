import tkinter as tk
from tkinter import ttk
from app_theme import AppTheme

class MenuComponent:
    def __init__(self,
                 app_theme: AppTheme,
                 column: int,
                 row: int,
                 padx: int,
                 pady: int,
                 parent):

        # vars


        # frame
        menu_frame = ttk.Frame(parent)
        menu_frame.grid(column=column, row=row, padx=padx, pady=pady)

        # components
        btn = ttk.Button(menu_frame, text='Click me !', command=lambda: print('hi'))
        btn.grid(column=0, row=0)

        # ttk.Label(parent, text='Note').grid(column=0, row=3, padx=label_pad_x, pady=label_pad_y)
        # note_var = tk.StringVar()
        # note_combo = ttk.Combobox(parent, textvariable=note_var)
        # note_combo.grid(column=1, row=3, padx=control_pad_x, pady=control_pad_y, sticky=(tk.W, tk.E))
        # note_combo['values'] = ('C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B')
        # note_combo.state(['readonly'])