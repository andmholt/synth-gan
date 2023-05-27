import sys
sys.path.append('..')
import tkinter as tk
from tkinter import ttk
from app_theme import AppTheme
from util import play_buff
from synthesizer import Synthesizer

class MenuComponent:
    def __init__(self,
                 app_theme: AppTheme,
                 column: int,
                 row: int,
                 padx: int,
                 pady: int,
                 parent,
                 synthesizer: Synthesizer):

        self.synthesizer = synthesizer

        # frame
        menu_frame = ttk.Frame(parent)
        menu_frame.grid(column=column, row=row, padx=padx, pady=pady)

        # components
        btn = ttk.Button(menu_frame, text='Play !', command=lambda: self.play())
        btn.grid(column=0, row=0)