import sys
sys.path.append('..')
import tkinter as tk
from tkinter import ttk
from uuid import UUID
from typing import List, Callable
from app_theme import AppTheme
from util import play_buff
from synthesizer import Synthesizer
from preset import Preset

class MenuComponent:
    def __init__(self,
                 app_theme: AppTheme,
                 column: int,
                 row: int,
                 padx: int,
                 pady: int,
                 parent,
                 presets: List[Preset],
                 load_preset: Callable[[UUID], None],
                 insert_init_and_load_all: Callable,
                 save_presets_to_disk: Callable):

        self.presets = presets

        # vars
        self.curr_preset_name = tk.StringVar(parent, 'Current Preset: None')

        self.preset_name = tk.StringVar(parent, '')

        self.kick_tag = tk.BooleanVar(parent, False)
        self.snare_tag = tk.BooleanVar(parent, False)
        self.clap_tag = tk.BooleanVar(parent, False)
        self.hat_tag = tk.BooleanVar(parent, False)

        self.rock_tag = tk.BooleanVar(parent, False)
        self.edm_tag = tk.BooleanVar(parent, False)
        self.harsh_tag = tk.BooleanVar(parent, False)
        self.soft_tag = tk.BooleanVar(parent, False)

        # frame
        menu_frame = ttk.Frame(parent)
        menu_frame.grid(column=column, row=row, padx=padx, pady=pady, sticky=(tk.N, tk.S))

        # components
        ttk.Label(menu_frame, textvariable=self.curr_preset_name).grid(column=0, row=0, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y+10, sticky=tk.W)

        ttk.Label(menu_frame, text='Presets').grid(column=0, row=1, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        preset_scroll = tk.Scrollbar(menu_frame)
        preset_scroll.grid(column=1, row=2, sticky=(tk.N, tk.S))
        self.preset_list = tk.Listbox(menu_frame, yscrollcommand=preset_scroll.set)
        self.preset_list.bind('<ButtonRelease-1>', lambda e: load_preset(self.presets[e.widget.curselection()[0]].id))
        self.preset_list.grid(column=0, row=2, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y)
        for preset in self.presets:
            self.preset_list.insert(tk.END, preset.name)

        preset_config_frame = ttk.Frame(menu_frame)
        preset_config_frame.grid(column=0, row=3, sticky=(tk.E, tk.W))

        init_preset_button = tk.Button(preset_config_frame, text='Init', foreground='black')
        init_preset_button.grid(column=0, row=0)

        new_preset_button = tk.Button(preset_config_frame, text='New', foreground='black')
        new_preset_button.bind('<ButtonRelease-1>', lambda _: insert_init_and_load_all())
        new_preset_button.grid(column=1, row=0)

        save_preset_button = tk.Button(preset_config_frame, text='Save', foreground='black')
        save_preset_button.bind('<ButtonRelease-1>', lambda _: save_presets_to_disk())
        save_preset_button.grid(column=2, row=0)

        ttk.Label(preset_config_frame, text='Name').grid(column=0, row=1, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        self.preset_name_entry = ttk.Entry(preset_config_frame, textvariable=self.preset_name)
        self.preset_name_entry.grid(column=0, row=2, columnspan=3, pady=5)
        
        # instr tags
        ttk.Label(menu_frame, text='Instrument Tags').grid(column=0, row=4, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y+10)
        instr_tags_frame = ttk.Frame(menu_frame)
        instr_tags_frame.grid(column=0, row=5, columnspan=2, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        kick_tag_check = ttk.Checkbutton(instr_tags_frame, text='Kick', variable=self.kick_tag, onvalue=True, offvalue=False)
        kick_tag_check.grid(column=0, row=0, padx=app_theme.check_pad_x, pady=app_theme.check_pad_y, sticky=tk.W)

        snare_tag_check = ttk.Checkbutton(instr_tags_frame, text='Snare', variable=self.snare_tag, onvalue=True, offvalue=False)
        snare_tag_check.grid(column=1, row=0, padx=app_theme.check_pad_x, pady=app_theme.check_pad_y, sticky=tk.W)

        # clap_tag_check = ttk.Checkbutton(instr_tags_frame, text='Clap', variable=self.clap_tag, onvalue=True, offvalue=False)
        # clap_tag_check.grid(column=2, row=0, padx=app_theme.check_pad_x, pady=app_theme.check_pad_y, sticky=tk.W)

        # hat_tag_check = ttk.Checkbutton(instr_tags_frame, text='Hat', variable=self.hat_tag, onvalue=True, offvalue=False)
        # hat_tag_check.grid(column=0, row=1, padx=app_theme.check_pad_x, pady=app_theme.check_pad_y, sticky=tk.W)

        # tags
        ttk.Label(menu_frame, text='Tags').grid(column=0, row=6, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y+10)
        tags_frame = ttk.Frame(menu_frame)
        tags_frame.grid(column=0, row=7, columnspan=2, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        rock_tag_check = ttk.Checkbutton(tags_frame, text='Rock', variable=self.rock_tag, onvalue=True, offvalue=False)
        rock_tag_check.grid(column=0, row=0, padx=app_theme.check_pad_x, pady=app_theme.check_pad_y, sticky=tk.W)

        edm_tag_check = ttk.Checkbutton(tags_frame, text='EDM', variable=self.edm_tag, onvalue=True, offvalue=False)
        edm_tag_check.grid(column=1, row=0, padx=app_theme.check_pad_x, pady=app_theme.check_pad_y, sticky=tk.W)

        harsh_tag_check = ttk.Checkbutton(tags_frame, text='Harsh', variable=self.harsh_tag, onvalue=True, offvalue=False)
        harsh_tag_check.grid(column=0, row=1, padx=app_theme.check_pad_x, pady=app_theme.check_pad_y, sticky=tk.W)

        soft_tag_check = ttk.Checkbutton(tags_frame, text='Soft', variable=self.soft_tag, onvalue=True, offvalue=False)
        soft_tag_check.grid(column=1, row=1, padx=app_theme.check_pad_x, pady=app_theme.check_pad_y, sticky=tk.W)