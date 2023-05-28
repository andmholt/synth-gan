import sys
sys.path.append('..')
from uuid import UUID
import sounddevice as sd
import threading
import numpy as np
import tkinter as tk
from tkinter import ttk
from util import play_buff, SampleRate
from synthesizer import Synthesizer

# components
from app_theme import AppTheme
from waveform_oscillator_component import WaveformOscillatorComponent
from menu_component import MenuComponent
from waveform_oscillator_controller import WaveformOscillatorController
from synthesizer_menu_component import SynthesizerMenuComponent
from preset import PresetHandler, Preset

INIT_LEN_S: float = 2.0

class App:
    def __init__(self):

        # state
        self.is_playing = False

        # play thread
        self.play_thread = None

        # presets
        self.preset_handler = PresetHandler()
        self.presets = self.preset_handler.load_all_presets('presets.json')

        # theme
        self.app_theme = AppTheme(title_pad_x=0,
                                  title_pad_y=5,
                                  label_pad_x=0,
                                  label_pad_y=0,
                                  control_pad_x=10,
                                  control_pad_y=2,
                                  check_pad_x=5,
                                  check_pad_y=1)
        
        # root
        self.root = tk.Tk()
        self.root.title('synth-gan admin')

        # syntehsizer
        self.synthesizer = Synthesizer(sample_rate=SampleRate._44100)

        # components
        self.fundamental_osc_component = WaveformOscillatorComponent(app_theme=self.app_theme,
                                                                     column=0,
                                                                     row=0,
                                                                     padx=20,
                                                                     pady=20,
                                                                     title='Fundamental Oscillator',
                                                                     parent=self.root)
        
        self.floof_osc_component = WaveformOscillatorComponent(app_theme=self.app_theme,
                                                               column=1,
                                                               row=0,
                                                               padx=20,
                                                               pady=20,
                                                               title='Floof Oscillator',
                                                               parent=self.root)
        
        self.synthesizer_menu_component = SynthesizerMenuComponent(app_theme=self.app_theme,
                                                                   column=2,
                                                                   row=0,
                                                                   padx=20,
                                                                   pady=20,
                                                                   parent=self.root,
                                                                   set_len_s_and_regen=self.set_len_s_and_regen)
        
        self.menu_component = MenuComponent(app_theme=self.app_theme,
                                            column=3,
                                            row=0,
                                            padx=20,
                                            pady=20,
                                            parent=self.root,
                                            presets=self.presets)
        
        # controllers
        self.fundamental_osc_controller = WaveformOscillatorController(is_fundamental_osc=True,
                                                                       synthesizer=self.synthesizer,
                                                                       osc_component=self.fundamental_osc_component,
                                                                       len_s=INIT_LEN_S)
        self.floof_osc_controller = WaveformOscillatorController(is_fundamental_osc=False,
                                                                 synthesizer=self.synthesizer,
                                                                 osc_component=self.floof_osc_component,
                                                                 len_s=INIT_LEN_S)
        
        # key press
        self.root.bind('<KeyPress>', lambda e: self.on_key_press(e))

        self.root.bind("<Return>")
        self.root.mainloop()

    def set_len_s_and_regen(self,
                            len_s: float) -> None:
        """
        Set the length of the oscillators and regenerate all.

        - len_s: float
        """
        self.fundamental_osc_controller.set_len_s_and_regen(len_s=len_s)
        self.floof_osc_controller.set_len_s_and_regen(len_s=len_s)

    def play(self) -> None:
        self.is_playing = True
        sd.play(np.column_stack((self.synthesizer.main_buff[0], self.synthesizer.main_buff[1])),
                self.synthesizer.sample_rate.value)
        sd.wait()
        self.is_playing = False
    
    def stop(self) -> None:
        sd.stop()
        self.is_playing = False

    def on_key_press(self,
                     e) -> None:
        if e.char == ' ' and not self.is_playing:
            if self.play_thread != None and self.play_thread.is_alive():
                self.play_thread.join()
            self.play_thread = threading.Thread(target=self.play)
            self.play_thread.start()
        elif e.char == ' ' and self.is_playing:
            self.stop()

    def insert_init_preset_and_load(self,) -> None:
        pass

    def load_preset(self,
                    preset_id: UUID) -> None:
        pass