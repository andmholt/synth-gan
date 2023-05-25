import sys
sys.path.append('..')
import tkinter as tk
from tkinter import ttk
from util import play_buff

from app_theme import AppTheme
from oscillator_component import OscillatorComponent
from menu_component import MenuComponent

class App:
    def __init__(self):

        # theme
        self.app_theme = AppTheme(title_pad_x=0,
                                  title_pad_y=5,
                                  label_pad_x=0,
                                  label_pad_y=0,
                                  control_pad_x=10,
                                  control_pad_y=2)
        
        # root
        self.root = tk.Tk()
        self.root.title('synth-gan admin')

        # components
        self.fundamental_osc = OscillatorComponent(app_theme=self.app_theme,
                                                   column=0,
                                                   row=0,
                                                   padx=20,
                                                   pady=20,
                                                   title='Fundamental Oscillator',
                                                   parent=self.root)
        
        self.floof_osc = OscillatorComponent(app_theme=self.app_theme,
                                             column=1,
                                             row=0,
                                             padx=20,
                                             pady=20,
                                             title='Floof Oscillator',
                                             parent=self.root)
        
        self.menu = MenuComponent(app_theme=self.app_theme,
                                  column=2,
                                  row=0,
                                  padx=20,
                                  pady=20,
                                  parent=self.root)

        self.root.bind("<Return>")

    def __call__(self):
        self.root.mainloop()