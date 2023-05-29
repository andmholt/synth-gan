import tkinter as tk
from tkinter import ttk
from app_theme import AppTheme
from typing import Callable
from note_name import NoteName

class WaveformOscillatorComponent:
    def __init__(self,
                 app_theme: AppTheme,
                 column: int,
                 row: int,
                 padx: int,
                 pady: int,
                 title: str,
                 synthesizer_len_s: float,
                 parent):
        
        # callbacks
        self.generate_buff_callback = None
        self.reapply_supps_callback = None

        # vars
        self.waveform_mix = tk.DoubleVar(parent, 1)
        self.waveform_phase = tk.IntVar(parent, 0)
        self.waveform_note = tk.StringVar(parent, 'F_3')
        self.waveform_complexity = tk.IntVar(parent, 0)

        self.volume_env_attack_len = tk.DoubleVar(parent, 0)
        self.volume_env_attack_sharpness = tk.DoubleVar(parent, 1)
        self.volume_env_decay_len = tk.DoubleVar(parent, 1)
        self.volume_env_decay_sharpness = tk.DoubleVar(parent, 1)

        self.pitch_env_range = tk.IntVar(parent, -24)
        self.pitch_env_attack_len = tk.DoubleVar(parent, 0.5)
        self.pitch_env_attack_sharpness = tk.DoubleVar(parent, 1)

        self.lowpass_mix = tk.DoubleVar(parent, 0)
        self.lowpass_cutoff = tk.IntVar(parent, 20000)
        self.lowpass_order = tk.IntVar(parent, 4)

        self.highpass_mix = tk.DoubleVar(parent, 0)
        self.highpass_cutoff = tk.IntVar(parent, 1)
        self.highpass_order = tk.IntVar(parent, 4)

        # frame
        osc_frame = ttk.Labelframe(parent, text=title)
        osc_frame.grid(column=column, row=row, padx=padx, pady=pady)

        # waveform
        ttk.Label(osc_frame, text='Waveform').grid(column=0, row=0, columnspan=2, padx=app_theme.title_pad_x, pady=app_theme.title_pad_y)

        ttk.Label(osc_frame, text='Mix (%)').grid(column=0, row=1, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        mix_scale = tk.Scale(osc_frame, from_=0, to=1, orient='horizontal', variable=self.waveform_mix, resolution=0.01)
        mix_scale.bind('<ButtonRelease-1>', lambda _: self.generate_buff())
        mix_scale.grid(column=1, row=1, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Phase (°)').grid(column=0, row=2, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        phase_scale = tk.Scale(osc_frame, from_=0, to=359, orient='horizontal', variable=self.waveform_phase)
        phase_scale.bind('<ButtonRelease-1>', lambda _: self.generate_buff())
        phase_scale.grid(column=1, row=2, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        ttk.Label(osc_frame, text='Note').grid(column=0, row=3, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        note_combo = ttk.Combobox(osc_frame, textvariable=self.waveform_note)
        # note_combo['values'] = ('C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B')
        note_combo['values'] = [note_name.name for note_name in NoteName]
        note_combo.state(['readonly'])
        note_combo.bind('<<ComboboxSelected>>', lambda _: self.generate_buff())
        note_combo.grid(column=1, row=3, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))
        note_combo['foreground'] = '#000000'

        # ttk.Label(osc_frame, text='Complexity').grid(column=0, row=3, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        # complexity_scale = tk.Scale(osc_frame, from_=0, to=42, orient='horizontal', variable=self.waveform_complexity)
        # complexity_scale.bind('<ButtonRelease-1>', lambda _: self.generate_buff())
        # complexity_scale.grid(column=1, row=3, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        ttk.Label(osc_frame, text='----------------------------------------').grid(column=0, row=4, columnspan=2, padx=10)

        # pitch
        ttk.Label(osc_frame, text='Pitch').grid(column=0, row=5, columnspan=2, padx=app_theme.title_pad_x, pady=app_theme.title_pad_y)

        ttk.Label(osc_frame, text='Range').grid(column=0, row=6, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        pitch_env_range_scale = tk.Scale(osc_frame, from_=-36, to=36, orient='horizontal', variable=self.pitch_env_range)
        pitch_env_range_scale.bind('<ButtonRelease-1>', lambda _: self.generate_buff())
        pitch_env_range_scale.grid(column=1, row=6, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Attack Length (%)').grid(column=0, row=7, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        pitch_env_attack_len_scale = tk.Scale(osc_frame, from_=0, to=1, orient='horizontal', variable=self.pitch_env_attack_len, resolution=0.1)
        pitch_env_attack_len_scale.bind('<ButtonRelease-1>', lambda _: self.generate_buff())
        pitch_env_attack_len_scale.grid(column=1, row=7, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Attack Sharpness').grid(column=0, row=8, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        pitch_env_attack_sharpness_scale = tk.Scale(osc_frame, from_=0, to=10, orient='horizontal', variable=self.pitch_env_attack_sharpness, resolution=0.1)
        pitch_env_attack_sharpness_scale.bind('<ButtonRelease-1>', lambda _: self.generate_buff())
        pitch_env_attack_sharpness_scale.grid(column=1, row=8, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        ttk.Label(osc_frame, text='----------------------------------------').grid(column=0, row=9, columnspan=2, padx=10)

        # volume
        ttk.Label(osc_frame, text='Volume').grid(column=0, row=10, columnspan=2, pady=5)

        ttk.Label(osc_frame, text='Attack Length (%)').grid(column=0, row=11, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        volume_env_attack_len_scale = tk.Scale(osc_frame, from_=0, to=1, orient='horizontal', variable=self.volume_env_attack_len, resolution=0.1)
        volume_env_attack_len_scale.bind('<ButtonRelease-1>', lambda _: self.reapply_supps())
        volume_env_attack_len_scale.grid(column=1, row=11, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Attack Sharpness').grid(column=0, row=12, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        volume_env_attack_sharpness_scale = tk.Scale(osc_frame, from_=0, to=10, orient='horizontal', variable=self.volume_env_attack_sharpness, resolution=0.1)
        volume_env_attack_sharpness_scale.bind('<ButtonRelease-1>', lambda _: self.reapply_supps())
        volume_env_attack_sharpness_scale.grid(column=1, row=12, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Decay Length (%)').grid(column=0, row=13, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        volume_env_decay_len_scale = tk.Scale(osc_frame, from_=0, to=1, orient='horizontal', variable=self.volume_env_decay_len, resolution=0.1)
        volume_env_decay_len_scale.bind('<ButtonRelease-1>', lambda _: self.reapply_supps())
        volume_env_decay_len_scale.grid(column=1, row=13, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        ttk.Label(osc_frame, text='Decay Sharpness').grid(column=0, row=14, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        volume_env_decay_sharpness_scale = tk.Scale(osc_frame, from_=0, to=10, orient='horizontal', variable=self.volume_env_decay_sharpness, resolution=0.1)
        volume_env_decay_sharpness_scale.bind('<ButtonRelease-1>', lambda _: self.reapply_supps())
        volume_env_decay_sharpness_scale.grid(column=1, row=14, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        ttk.Label(osc_frame, text='----------------------------------------').grid(column=0, row=15, columnspan=2, padx=10)

        # filter
        ttk.Label(osc_frame, text='Filter').grid(column=0, row=16, columnspan=2, padx=app_theme.title_pad_x, pady=app_theme.title_pad_y)

        ttk.Label(osc_frame, text='Highpass Mix (%)').grid(column=0, row=17, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        highpass_mix_scale = tk.Scale(osc_frame, from_=0, to=1, orient='horizontal', variable=self.highpass_mix, resolution=0.01)
        highpass_mix_scale.bind('<ButtonRelease-1>', lambda _: self.reapply_supps())
        highpass_mix_scale.grid(column=1, row=17, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        ttk.Label(osc_frame, text='Highpass Cutoff (Hz)').grid(column=0, row=18, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        highpass_cutoff_scale = tk.Scale(osc_frame, from_=0, to=20000, orient='horizontal', variable=self.highpass_cutoff, resolution=100)
        highpass_cutoff_scale.bind('<ButtonRelease-1>', lambda _: self.reapply_supps())
        highpass_cutoff_scale.grid(column=1, row=18, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Highpass Order').grid(column=0, row=19, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        highpass_order_scale = tk.Scale(osc_frame, from_=0, to=5, orient='horizontal', variable=self.highpass_order)
        highpass_order_scale.bind('<ButtonRelease-1>', lambda _: self.reapply_supps())
        highpass_order_scale.grid(column=1, row=19, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Lowpass Mix (%)').grid(column=0, row=20, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        lowpass_mix_scale = tk.Scale(osc_frame, from_=0, to=1, orient='horizontal', variable=self.lowpass_mix, resolution=0.01)
        lowpass_mix_scale.bind('<ButtonRelease-1>', lambda _: self.reapply_supps())
        lowpass_mix_scale.grid(column=1, row=20, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        ttk.Label(osc_frame, text='Lowpass Cutoff (Hz)').grid(column=0, row=21, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        lowpass_cutoff_scale = tk.Scale(osc_frame, from_=0, to=20000, orient='horizontal', variable=self.lowpass_cutoff, resolution=100)
        lowpass_cutoff_scale.bind('<ButtonRelease-1>', lambda _: self.reapply_supps())
        lowpass_cutoff_scale.grid(column=1, row=21, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Lowpass Order').grid(column=0, row=22, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        lowpass_order_scale = tk.Scale(osc_frame, from_=0, to=5, orient='horizontal', variable=self.lowpass_order)
        lowpass_order_scale.bind('<ButtonRelease-1>', lambda _: self.reapply_supps())
        lowpass_order_scale.grid(column=1, row=22, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

    def set_generate_buff_callback(self,
                                   generate_buff_callback: Callable) -> None:
        self.generate_buff_callback = generate_buff_callback

    def set_reapply_supps_callback(self,
                                   reapply_supps_callback: Callable) -> None:
        self.reapply_supps_callback = reapply_supps_callback

    def generate_buff(self) -> None:
        self.generate_buff_callback()

    def reapply_supps(self) -> None:
        self.reapply_supps_callback()