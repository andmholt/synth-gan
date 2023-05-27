import sys
sys.path.append('..')
from typing import Callable
from tkinter import ttk
import tkinter as tk
from app_theme import AppTheme

class SynthesizerMenuComponent:
    def __init__(self,
                 app_theme: AppTheme,
                 column: int,
                 row: int,
                 padx: int,
                 pady: int,
                 parent,
                 set_len_s_and_regen: Callable):

        # frame
        synth_menu_frame = ttk.Labelframe(parent, text='Synthesizer Main')
        synth_menu_frame.grid(column=column, row=row, padx=padx, pady=pady, sticky=tk.N)

        # vars
        self.len_s = tk.DoubleVar(parent, 2)

        # components
        ttk.Label(synth_menu_frame, text='Signal Length (s)').grid(column=0, row=0, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        len_s_scale = tk.Scale(synth_menu_frame, from_=0.1, to=8, orient='horizontal', variable=self.len_s, resolution=0.1)
        len_s_scale.bind('<ButtonRelease-1>', lambda _: set_len_s_and_regen(self.len_s.get()))
        len_s_scale.grid(column=1, row=0, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))