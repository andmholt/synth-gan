import tkinter as tk
from tkinter import ttk

TITLE_PAD_X = 0
TITLE_PAD_Y = 5

LABEL_PAD_X = 0
LABEL_PAD_Y = 0

CONTROL_PAD_X = 10
CONTROL_PAD_Y = 2

# init tk
root = tk.Tk()
root.title('synth-gan admin')

# main frame
mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# init frames
fundamental_osc = ttk.Labelframe(root, text='Fundamental Oscillator')
fundamental_osc.grid(column=0, row=0, padx=20, pady=20, stick=tk.N)

floof_osc = ttk.Labelframe(root, text='Floof Oscillator')
floof_osc.grid(column=1, row=0, padx=20, pady=20, stick=tk.N)

attack_osc = ttk.Labelframe(root, text='Fundamental Oscillator')
attack_osc.grid(column=2, row=0, padx=20, pady=20, stick=tk.N)

noise_osc = ttk.Labelframe(root, text='Fundamental Oscillator')
noise_osc.grid(column=3, row=0, padx=20, pady=20, stick=tk.N)

# ===== fundamental osc =====

# waveform
ttk.Label(fundamental_osc, text='Waveform').grid(column=0, row=0, columnspan=2, padx=TITLE_PAD_X, pady=TITLE_PAD_Y)

ttk.Label(fundamental_osc, text='Mix (%)').grid(column=0, row=1, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
fund_mix_scale = tk.Scale(fundamental_osc, from_=0, to=42, orient='horizontal')
fund_mix_scale.grid(column=1, row=1, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(fundamental_osc, text='Phase (°)').grid(column=0, row=2, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
fund_phase_scale = tk.Scale(fundamental_osc, from_=0, to=42, orient='horizontal')
fund_phase_scale.grid(column=1, row=2, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E))

ttk.Label(fundamental_osc, text='Note').grid(column=0, row=3, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
note_var = tk.StringVar()
note_combo = ttk.Combobox(fundamental_osc, textvariable=note_var)
note_combo.grid(column=1, row=3, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E))
note_combo['values'] = ('C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B')
note_combo.state(['readonly'])

ttk.Label(fundamental_osc, text='Complexity').grid(column=0, row=4, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
fund_complexity_scale = tk.Scale(fundamental_osc, from_=0, to=42, orient='horizontal')
fund_complexity_scale.grid(column=1, row=4, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E))

ttk.Label(fundamental_osc, text='----------------------------------------').grid(column=0, row=5, columnspan=2, padx=10)

# volume
ttk.Label(fundamental_osc, text='Volume').grid(column=0, row=6, columnspan=2, pady=5)

ttk.Label(fundamental_osc, text='Attack').grid(column=0, row=7, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
fund_volume_env_attack_scale = tk.Scale(fundamental_osc, from_=0, to=42, orient='horizontal')
fund_volume_env_attack_scale.grid(column=1, row=7, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(fundamental_osc, text='Decay').grid(column=0, row=8, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
fund_volume_env_decay_scale = tk.Scale(fundamental_osc, from_=0, to=42, orient='horizontal')
fund_volume_env_decay_scale.grid(column=1, row=8, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E))

ttk.Label(fundamental_osc, text='----------------------------------------').grid(column=0, row=9, columnspan=2, padx=10)

# volume
ttk.Label(fundamental_osc, text='Pitch').grid(column=0, row=10, columnspan=2, padx=TITLE_PAD_X, pady=TITLE_PAD_Y)

ttk.Label(fundamental_osc, text='Range').grid(column=0, row=11, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
fund_pitch_env_range_scale = tk.Scale(fundamental_osc, from_=0, to=42, orient='horizontal')
fund_pitch_env_range_scale.grid(column=1, row=11, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(fundamental_osc, text='Attack').grid(column=0, row=12, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
fund_pitch_env_attack_scale = tk.Scale(fundamental_osc, from_=0, to=42, orient='horizontal')
fund_pitch_env_attack_scale.grid(column=1, row=12, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(fundamental_osc, text='Decay').grid(column=0, row=13, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
fund_pitch_env_decay_scale = tk.Scale(fundamental_osc, from_=0, to=42, orient='horizontal')
fund_pitch_env_decay_scale.grid(column=1, row=13, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E))

ttk.Label(fundamental_osc, text='----------------------------------------').grid(column=0, row=14, columnspan=2, padx=10)

# filter
ttk.Label(fundamental_osc, text='Filter').grid(column=0, row=15, columnspan=2, padx=TITLE_PAD_X, pady=TITLE_PAD_Y)

ttk.Label(fundamental_osc, text='Highpass Cutoff (Hz)').grid(column=0, row=16, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
fund_lowpass_cutoff_scale = tk.Scale(fundamental_osc, from_=0, to=42, orient='horizontal')
fund_lowpass_cutoff_scale.grid(column=1, row=16, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(fundamental_osc, text='Highpass Order').grid(column=0, row=17, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
fund_lowpass_order_scale = tk.Scale(fundamental_osc, from_=0, to=42, orient='horizontal')
fund_lowpass_order_scale.grid(column=1, row=17, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(fundamental_osc, text='Highpass Mix (%)').grid(column=0, row=18, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
fund_lowpass_mix_scale = tk.Scale(fundamental_osc, from_=0, to=42, orient='horizontal')
fund_lowpass_mix_scale.grid(column=1, row=18, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E))

ttk.Label(fundamental_osc, text='Lowpass Cutoff (Hz)').grid(column=0, row=19, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
fund_highpass_cutoff_scale = tk.Scale(fundamental_osc, from_=0, to=42, orient='horizontal')
fund_highpass_cutoff_scale.grid(column=1, row=19, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(fundamental_osc, text='Lowpass Order').grid(column=0, row=20, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
fund_highpass_order_scale = tk.Scale(fundamental_osc, from_=0, to=42, orient='horizontal')
fund_highpass_order_scale.grid(column=1, row=20, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(fundamental_osc, text='Lowpass Mix (%)').grid(column=0, row=21, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
fund_highpass_mix_scale = tk.Scale(fundamental_osc, from_=0, to=42, orient='horizontal')
fund_highpass_mix_scale.grid(column=1, row=21, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E))

# ===== floof osc =====

# waveform
ttk.Label(floof_osc, text='Waveform').grid(column=0, row=0, columnspan=2, padx=TITLE_PAD_X, pady=TITLE_PAD_Y)

ttk.Label(floof_osc, text='Mix (%)').grid(column=0, row=1, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
floof_mix_scale = tk.Scale(floof_osc, from_=0, to=42, orient='horizontal')
floof_mix_scale.grid(column=1, row=1, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(floof_osc, text='Phase (°)').grid(column=0, row=2, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
floof_phase_scale = tk.Scale(floof_osc, from_=0, to=42, orient='horizontal')
floof_phase_scale.grid(column=1, row=2, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E))

ttk.Label(floof_osc, text='Complexity').grid(column=0, row=4, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
floof_complexity_scale = tk.Scale(floof_osc, from_=0, to=42, orient='horizontal')
floof_complexity_scale.grid(column=1, row=4, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E))

ttk.Label(floof_osc, text='----------------------------------------').grid(column=0, row=5, columnspan=2, padx=10)

# volume
ttk.Label(floof_osc, text='Volume').grid(column=0, row=6, columnspan=2, pady=5)

ttk.Label(floof_osc, text='Attack').grid(column=0, row=7, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
floof_volume_env_attack_scale = tk.Scale(floof_osc, from_=0, to=42, orient='horizontal')
floof_volume_env_attack_scale.grid(column=1, row=7, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(floof_osc, text='Decay').grid(column=0, row=8, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
floof_volume_env_decay_scale = tk.Scale(floof_osc, from_=0, to=42, orient='horizontal')
floof_volume_env_decay_scale.grid(column=1, row=8, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E))

ttk.Label(floof_osc, text='----------------------------------------').grid(column=0, row=9, columnspan=2, padx=10)

# volume
ttk.Label(floof_osc, text='Pitch').grid(column=0, row=10, columnspan=2, padx=TITLE_PAD_X, pady=TITLE_PAD_Y)

ttk.Label(floof_osc, text='Range').grid(column=0, row=11, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
floof_pitch_env_range_scale = tk.Scale(floof_osc, from_=0, to=42, orient='horizontal')
floof_pitch_env_range_scale.grid(column=1, row=11, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(floof_osc, text='Attack').grid(column=0, row=12, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
floof_pitch_env_attack_scale = tk.Scale(floof_osc, from_=0, to=42, orient='horizontal')
floof_pitch_env_attack_scale.grid(column=1, row=12, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(floof_osc, text='Decay').grid(column=0, row=13, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
floof_pitch_env_decay_scale = tk.Scale(floof_osc, from_=0, to=42, orient='horizontal')
floof_pitch_env_decay_scale.grid(column=1, row=13, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E))

ttk.Label(floof_osc, text='----------------------------------------').grid(column=0, row=14, columnspan=2, padx=10)

# filter
ttk.Label(floof_osc, text='Filter').grid(column=0, row=15, columnspan=2, padx=TITLE_PAD_X, pady=TITLE_PAD_Y)

ttk.Label(floof_osc, text='Highpass Cutoff (Hz)').grid(column=0, row=16, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
floof_lowpass_cutoff_scale = tk.Scale(floof_osc, from_=0, to=42, orient='horizontal')
floof_lowpass_cutoff_scale.grid(column=1, row=16, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(floof_osc, text='Highpass Order').grid(column=0, row=17, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
floof_lowpass_order_scale = tk.Scale(floof_osc, from_=0, to=42, orient='horizontal')
floof_lowpass_order_scale.grid(column=1, row=17, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(floof_osc, text='Highpass Mix (%)').grid(column=0, row=18, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
floof_lowpass_mix_scale = tk.Scale(floof_osc, from_=0, to=42, orient='horizontal')
floof_lowpass_mix_scale.grid(column=1, row=18, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E))

ttk.Label(floof_osc, text='Lowpass Cutoff (Hz)').grid(column=0, row=19, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
floof_highpass_cutoff_scale = tk.Scale(floof_osc, from_=0, to=42, orient='horizontal')
floof_highpass_cutoff_scale.grid(column=1, row=19, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(floof_osc, text='Lowpass Order').grid(column=0, row=20, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
floof_highpass_order_scale = tk.Scale(floof_osc, from_=0, to=42, orient='horizontal')
floof_highpass_order_scale.grid(column=1, row=20, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E),)

ttk.Label(floof_osc, text='Lowpass Mix (%)').grid(column=0, row=21, padx=LABEL_PAD_X, pady=LABEL_PAD_Y)
floof_highpass_mix_scale = tk.Scale(floof_osc, from_=0, to=42, orient='horizontal')
floof_highpass_mix_scale.grid(column=1, row=21, padx=CONTROL_PAD_X, pady=CONTROL_PAD_Y, sticky=(tk.W, tk.E))

root.bind("<Return>")

root.mainloop()