import sys
sys.path.append('..')
from uuid import UUID
from typing import List
import os
import sounddevice as sd
import threading
import numpy as np
import tkinter as tk
from tkinter import ttk
from util import play_buff, SampleRate, read_wav
from synthesizer import Synthesizer

# components
from app_theme import AppTheme
from waveform_oscillator_component import WaveformOscillatorComponent
from menu_component import MenuComponent
from waveform_oscillator_controller import WaveformOscillatorController
from synthesizer_menu_component import SynthesizerMenuComponent
from preset import PresetHandler, Preset
from plot_component import PlotComponent

INIT_LEN_S: float = 2.0

class App:
    def __init__(self):

        # state
        self.is_playing = False
        self.synthesizer_len_s = INIT_LEN_S
        self.curr_preset_id = None
        self.curr_ref_buff = None
        self.curr_ref_sr = None

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

        third_frame = ttk.Frame(self.root)
        third_frame.grid(column=2,
                         row=0,
                         padx=20,
                         pady=20,
                         sticky=tk.N)

        self.synthesizer_menu_component = SynthesizerMenuComponent(app_theme=self.app_theme,
                                                                   column=0,
                                                                   row=0,
                                                                   padx=0,
                                                                   pady=0,
                                                                   parent=third_frame,
                                                                   set_len_s_and_regen=self.set_len_s_and_regen)
        
        self.preset_plot = PlotComponent(column=0,
                                         row=1,
                                         padx=0,
                                         pady=10,
                                         fig_title='Preset',
                                         wave_color='green',
                                         parent=third_frame)
        
        self.ref_plot = PlotComponent(column=0,
                                      row=2,
                                      padx=0,
                                      pady=10,
                                      fig_title='Reference',
                                      wave_color='blue',
                                      parent=third_frame)

        # load refs
        self.refs = self.load_refs(path='../refs')
        
        self.menu_component = MenuComponent(app_theme=self.app_theme,
                                            column=3,
                                            row=0,
                                            padx=20,
                                            pady=20,
                                            parent=self.root,
                                            presets=list(self.presets.values()),
                                            refs=self.refs,
                                            load_preset=self.load_preset,
                                            load_ref=self.load_ref,
                                            insert_init_and_load_all=self.insert_init_and_load_all,
                                            save_presets_to_disk=self.save_presets_to_disk)
        
        # controllers
        self.fundamental_osc_controller = WaveformOscillatorController(is_fundamental_osc=True,
                                                                       synthesizer=self.synthesizer,
                                                                       osc_component=self.fundamental_osc_component,
                                                                       len_s=INIT_LEN_S,
                                                                       update_plots=self.update_plots)
        self.floof_osc_controller = WaveformOscillatorController(is_fundamental_osc=False,
                                                                 synthesizer=self.synthesizer,
                                                                 osc_component=self.floof_osc_component,
                                                                 len_s=INIT_LEN_S,
                                                                 update_plots=self.update_plots)
        
        # key press
        self.root.bind('<KeyPress>', lambda e: self.on_key_press(e))

        self.root.bind("<Return>")
        self.root.mainloop()

    def update_plots(self) -> None:

        # get lengths
        preset_len_s = None
        ref_len_s = None

        if type(self.synthesizer.main_buff) == np.ndarray:
            preset_len_s = len(self.synthesizer.main_buff[0]) / self.synthesizer.sample_rate.value
        if type(self.curr_ref_buff) == np.ndarray:
            ref_len_s = len(self.curr_ref_buff[0]) / self.curr_ref_sr.value

        plot_len_s = None
        if preset_len_s == None and ref_len_s == None:
            return
        elif preset_len_s == None:
            plot_len_s = ref_len_s
        elif ref_len_s == None:
            plot_len_s = preset_len_s
        else:
            plot_len_s = max(preset_len_s, ref_len_s)

        # update plots
        self.preset_plot.update_plot(buff=self.synthesizer.main_buff,
                                     plot_len_s=plot_len_s,
                                     sr=self.synthesizer.sample_rate)
        self.ref_plot.update_plot(buff=self.curr_ref_buff,
                                  plot_len_s=plot_len_s,
                                  sr=self.curr_ref_sr)

    def load_refs(self,
                  path: str) -> List[str]:
        refs = []
        for file in (os.listdir(path)):
            if file.endswith('.wav'):
                refs.append(file)
        return refs
    
    def load_ref(self,
                 ref_path: str) -> None:
        
        # save ref to preset
        if self.curr_preset_id != None:
            self.presets[self.curr_preset_id].ref_path = ref_path

        # read wav
        self.curr_ref_buff, self.curr_ref_sr = read_wav(path='../refs/' + ref_path)

        # update plots
        self.update_plots()

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
        pad = np.zeros(int(self.synthesizer.sample_rate.value * 0.25))
        sd.play(np.column_stack((np.concatenate((self.synthesizer.main_buff[0], pad)),
                                 np.concatenate((self.synthesizer.main_buff[1], pad)))),
                self.synthesizer.sample_rate.value)
        sd.wait()
        self.is_playing = False

    def play_ref(self) -> None:
        self.is_playing = True
        pad = np.zeros(int(self.curr_ref_sr.value * 0.25))
        sd.play(np.column_stack((np.concatenate((self.curr_ref_buff[0], pad)),
                                 np.concatenate((self.curr_ref_buff[1], pad)))),
                self.curr_ref_sr.value)
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
        elif e.char == 'r' and not self.is_playing and self.root.focus_get() != self.menu_component.preset_name_entry:
            if self.play_thread != None and self.play_thread.is_alive():
                self.play_thread.join()
            self.play_thread = threading.Thread(target=self.play_ref)
            self.play_thread.start()
        elif (e.char == ' ' or e.char == 'r') and self.is_playing and self.root.focus_get() != self.menu_component.preset_name_entry:
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