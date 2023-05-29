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
        self.synthesizer_len_s = INIT_LEN_S
        self.curr_preset_id = None

        # play thread
        self.play_thread = None

        # presets
        self.preset_handler = PresetHandler()
        self.presets = self.preset_handler.load_all_from_disk('presets.json')

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
                                                                     parent=self.root,
                                                                     synthesizer_len_s=self.synthesizer_len_s)
        
        self.floof_osc_component = WaveformOscillatorComponent(app_theme=self.app_theme,
                                                               column=1,
                                                               row=0,
                                                               padx=20,
                                                               pady=20,
                                                               title='Floof Oscillator',
                                                               parent=self.root,
                                                               synthesizer_len_s=self.synthesizer_len_s)
        
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
                                            presets=list(self.presets.values()),
                                            load_preset=self.load_preset,
                                            insert_init_and_load_all=self.insert_init_and_load_all,
                                            save_presets_to_disk=self.save_presets_to_disk)
        
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
        self.synthesizer_len_s = len_s
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
        if e.char == ' ' and not self.is_playing and self.root.focus_get() != self.menu_component.preset_name_entry:
            if self.play_thread != None and self.play_thread.is_alive():
                self.play_thread.join()
            self.play_thread = threading.Thread(target=self.play)
            self.play_thread.start()
        elif e.char == ' ' and self.is_playing and self.root.focus_get() != self.menu_component.preset_name_entry:
            self.stop()

    def insert_init_and_load_all(self,) -> None:
        self.presets = self.preset_handler.insert_init_and_load_all(name='new')
        self.refresh_presets_listbox()

    def refresh_presets_listbox(self) -> None:
        self.menu_component.preset_list.delete(0, self.menu_component.preset_list.size()-1)
        self.menu_component.presets = list(self.presets.values())
        for preset in self.menu_component.presets:
            self.menu_component.preset_list.insert(tk.END, preset.name)

    def load_preset(self,
                    preset_id: UUID) -> None:
        
        # set menu name
        self.menu_component.preset_name.set(self.presets[preset_id].name)
        
        # set oscillator params
        fundamental_params = self.presets[preset_id].fundamental_params
        self.fundamental_osc_controller.load_preset(osc_params=fundamental_params)

        floof_params = self.presets[preset_id].floof_params
        self.floof_osc_controller.load_preset(osc_params=floof_params)

        # set synthesizer len_s and regenerate all
        new_len_s = self.presets[preset_id].fundamental_params.waveform_params.len_s
        self.set_len_s_and_regen(len_s=new_len_s)

        # set curr_preset
        self.curr_preset_id = preset_id
        self.menu_component.curr_preset_name.set('Current Preset: ' + self.presets[preset_id].name)

    def save_presets_to_disk(self,) -> None:
        # get current preset info
        curr_name = self.menu_component.preset_name.get()
        curr_ref_path = '' # SET CURR REF
        curr_fundamental_params = self.fundamental_osc_controller.get_waveform_oscillator_params()
        curr_floof_params = self.floof_osc_controller.get_waveform_oscillator_params()

        # save current preset info to presets
        self.presets[self.curr_preset_id].name = curr_name
        self.presets[self.curr_preset_id].ref_path = curr_ref_path
        self.presets[self.curr_preset_id].fundamental_params = curr_fundamental_params
        self.presets[self.curr_preset_id].floof_params = curr_floof_params

        # save presets to disk
        self.preset_handler.save_presets_to_disk(preset_file='presets.json',
                                                 presets=self.presets)
        # refresh presets listbox
        self.refresh_presets_listbox()