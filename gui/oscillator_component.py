import tkinter as tk
from tkinter import ttk
from app_theme import AppTheme

class OscillatorComponent:
    def __init__(self,
                 app_theme: AppTheme,
                 column: int,
                 row: int,
                 padx: int,
                 pady: int,
                 title: str,
                 parent):

        # vars
        self.waveform_mix = tk.IntVar(parent, 100)
        self.waveform_phase = tk.IntVar(parent, 0)
        self.waveform_complexity = tk.IntVar(parent, 0)

        self.volume_env_attack = tk.IntVar(parent, 0)
        self.volume_env_decay = tk.IntVar(parent, 0)

        self.pitch_env_range = tk.IntVar(parent, 0)
        self.pitch_env_attack = tk.IntVar(parent, 0)
        self.pitch_env_decay = tk.IntVar(parent, 0)

        self.lowpass_mix = tk.IntVar(parent, 0)
        self.lowpass_cutoff = tk.IntVar(parent, 0)
        self.lowpass_order = tk.IntVar(parent, 4)

        self.highpass_mix = tk.IntVar(parent, 0)
        self.highpass_cutoff = tk.IntVar(parent, 0)
        self.highpass_order = tk.IntVar(parent, 4)

        # frame
        osc_frame = ttk.Labelframe(parent, text=title)
        osc_frame.grid(column=column, row=row, padx=padx, pady=pady)

        # waveform
        ttk.Label(osc_frame, text='Waveform').grid(column=0, row=0, columnspan=2, padx=app_theme.title_pad_x, pady=app_theme.title_pad_y)

        ttk.Label(osc_frame, text='Mix (%)').grid(column=0, row=1, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        mix_scale = tk.Scale(osc_frame, from_=0.0, to=100.0, orient='horizontal', variable=self.waveform_mix, command=lambda _: print(self.waveform_phase.get()))
        mix_scale.grid(column=1, row=1, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Phase (°)').grid(column=0, row=2, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        phase_scale = tk.Scale(osc_frame, from_=0, to=359, orient='horizontal', variable=self.waveform_phase)
        phase_scale.grid(column=1, row=2, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        ttk.Label(osc_frame, text='Complexity').grid(column=0, row=4, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        complexity_scale = tk.Scale(osc_frame, from_=0, to=42, orient='horizontal', variable=self.waveform_complexity)
        complexity_scale.grid(column=1, row=4, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        ttk.Label(osc_frame, text='----------------------------------------').grid(column=0, row=5, columnspan=2, padx=10)

        # volume
        ttk.Label(osc_frame, text='Volume').grid(column=0, row=6, columnspan=2, pady=5)

        ttk.Label(osc_frame, text='Attack').grid(column=0, row=7, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        volume_env_attack_scale = tk.Scale(osc_frame, from_=0, to=42, orient='horizontal', variable=self.volume_env_attack)
        volume_env_attack_scale.grid(column=1, row=7, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Decay').grid(column=0, row=8, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        volume_env_decay_scale = tk.Scale(osc_frame, from_=0, to=42, orient='horizontal', variable=self.volume_env_decay)
        volume_env_decay_scale.grid(column=1, row=8, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        ttk.Label(osc_frame, text='----------------------------------------').grid(column=0, row=9, columnspan=2, padx=10)

        # volume
        ttk.Label(osc_frame, text='Pitch').grid(column=0, row=10, columnspan=2, padx=app_theme.title_pad_x, pady=app_theme.title_pad_y)

        ttk.Label(osc_frame, text='Range').grid(column=0, row=11, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        pitch_env_range_scale = tk.Scale(osc_frame, from_=0, to=36, orient='horizontal', variable=self.pitch_env_range)
        pitch_env_range_scale.grid(column=1, row=11, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Attack').grid(column=0, row=12, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        pitch_env_attack_scale = tk.Scale(osc_frame, from_=0, to=42, orient='horizontal', variable=self.pitch_env_attack)
        pitch_env_attack_scale.grid(column=1, row=12, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Decay').grid(column=0, row=13, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        pitch_env_decay_scale = tk.Scale(osc_frame, from_=0, to=42, orient='horizontal', variable=self.pitch_env_decay)
        pitch_env_decay_scale.grid(column=1, row=13, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        ttk.Label(osc_frame, text='----------------------------------------').grid(column=0, row=14, columnspan=2, padx=10)

        # filter
        ttk.Label(osc_frame, text='Filter').grid(column=0, row=15, columnspan=2, padx=app_theme.title_pad_x, pady=app_theme.title_pad_y)

        ttk.Label(osc_frame, text='Highpass Mix (%)').grid(column=0, row=18, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        highpass_mix_scale = tk.Scale(osc_frame, from_=0, to=100, orient='horizontal', variable=self.highpass_mix)
        highpass_mix_scale.grid(column=1, row=18, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        ttk.Label(osc_frame, text='Highpass Cutoff (Hz)').grid(column=0, row=16, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        highpass_cutoff_scale = tk.Scale(osc_frame, from_=0, to=20000, orient='horizontal', variable=self.highpass_cutoff)
        highpass_cutoff_scale.grid(column=1, row=16, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Highpass Order').grid(column=0, row=17, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        highpass_order_scale = tk.Scale(osc_frame, from_=0, to=5, orient='horizontal', variable=self.highpass_order)
        highpass_order_scale.grid(column=1, row=17, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Lowpass Mix (%)').grid(column=0, row=21, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        lowpass_mix_scale = tk.Scale(osc_frame, from_=0, to=100, orient='horizontal', variable=self.lowpass_mix)
        lowpass_mix_scale.grid(column=1, row=21, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E))

        ttk.Label(osc_frame, text='Lowpass Cutoff (Hz)').grid(column=0, row=19, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        lowpass_cutoff_scale = tk.Scale(osc_frame, from_=0, to=20000, orient='horizontal', variable=self.lowpass_cutoff)
        lowpass_cutoff_scale.grid(column=1, row=19, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)

        ttk.Label(osc_frame, text='Lowpass Order').grid(column=0, row=20, padx=app_theme.label_pad_x, pady=app_theme.label_pad_y)
        lowpass_order_scale = tk.Scale(osc_frame, from_=0, to=5, orient='horizontal', variable=self.lowpass_order)
        lowpass_order_scale.grid(column=1, row=20, padx=app_theme.control_pad_x, pady=app_theme.control_pad_y, sticky=(tk.W, tk.E),)