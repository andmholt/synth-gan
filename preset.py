import json
from typing import Tuple, Dict
import uuid
import copy
from uuid import UUID
from oscillator_params import WaveformOscillatorParams, WaveformParams, VolumeEnvParams, PitchEnvParams, LowpassParams, HighpassParams
from note_name import NoteName

class Preset:
    def __init__(self,
                 fundamental_params: WaveformOscillatorParams,
                 floof_params: WaveformOscillatorParams,
                 name: str,
                 ref_path: str):
        self.fundamental_params = fundamental_params
        self.floof_params = floof_params
        self.name = name
        self.ref_path = ref_path
        self.id = uuid.uuid1()

class PresetHandler:
    def __init__(self):
        self.presets = {}

    def insert_init_and_load_all(self,
                                 name: str='',
                                 ref_path: str='') -> Dict[UUID, Preset]:

        # init preset
        fundamental_waveform_params = WaveformParams(len_s=2,
                                                     mix=1,
                                                     phase=0,
                                                     fundamental=NoteName.F_3,
                                                     complexity=0)
        fundamental_volume_env_params = VolumeEnvParams(attack_s=0,
                                                        attack_sharpness=1,
                                                        decay_s=0,
                                                        decay_sharpness=1)
        fundamental_pitch_env_params = PitchEnvParams(range=0,
                                                      attack_s=0,
                                                      sharpness=1)
        fundamental_lowpass_params = LowpassParams(mix=1,
                                                   cutoff=20000,
                                                   order=4)
        fundamental_highpass_params = HighpassParams(mix=1,
                                                     cutoff=100,
                                                     order=4)
        fundamental_oscillator_params = WaveformOscillatorParams(waveform_params=fundamental_waveform_params,
                                                                 volume_env_params=fundamental_volume_env_params,
                                                                 pitch_env_params=fundamental_pitch_env_params,
                                                                 lowpass_params=fundamental_lowpass_params,
                                                                 highpass_params=fundamental_highpass_params)
        
        floof_waveform_params = WaveformParams(len_s=2,
                                               mix=1,
                                               phase=0,
                                               fundamental=NoteName.F_3,
                                               complexity=0)
        floof_volume_env_params = VolumeEnvParams(attack_s=0,
                                                  attack_sharpness=1,
                                                  decay_s=0,
                                                  decay_sharpness=1)
        floof_pitch_env_params = PitchEnvParams(range=0,
                                                attack_s=0,
                                                sharpness=1)
        floof_lowpass_params = LowpassParams(mix=1,
                                             cutoff=20000,
                                             order=4)
        floof_highpass_params = HighpassParams(mix=1,
                                               cutoff=100,
                                               order=4)
        floof_oscillator_params = WaveformOscillatorParams(waveform_params=floof_waveform_params,
                                                           volume_env_params=floof_volume_env_params,
                                                           pitch_env_params=floof_pitch_env_params,
                                                           lowpass_params=floof_lowpass_params,
                                                           highpass_params=floof_highpass_params)
        
        preset = Preset(fundamental_params=fundamental_oscillator_params,
                        floof_params=floof_oscillator_params,
                        name=name,
                        ref_path=ref_path)
        
        self.presets[preset.id] = preset

        return copy.deepcopy(self.presets)

    def load_all_from_disk(self,
                           preset_file: str) -> Dict[UUID, Preset]:
        """
        Loads all presets from the specified preset file.

        - preset_file: str

        returns -> [Preset]
        """
        with open(preset_file) as preset_file_opened:
            file_contents = preset_file_opened.read()

            json_presets = json.loads(file_contents)
            self.presets = {}
            for json_preset in json_presets:
                loaded_preset = self.json_to_preset(json.loads(json_preset))
                self.presets[loaded_preset.id] = loaded_preset

            return copy.deepcopy(self.presets)

    def json_to_preset(self,
                       json_preset: any) -> Preset:
        """
        Converts json preset to Preset.

        - json_preset: json object

        returns -> Preset
        """

        json_fundamental_osc = json_preset['fundamental_osc']

        json_fundamental_waveform = json_fundamental_osc['waveform']
        fundamental_waveform_params = WaveformParams(len_s=json_fundamental_waveform['len_s'],
                                                     mix=json_fundamental_waveform['mix'],
                                                     phase=json_fundamental_waveform['mix'],
                                                     fundamental=NoteName(json_fundamental_waveform['fundamental']),
                                                     complexity=json_fundamental_waveform['complexity'])
        
        json_fundamental_volume_env = json_fundamental_osc['volume_env']
        fundamental_volume_env_params = VolumeEnvParams(attack_s=json_fundamental_volume_env['attack_s'],
                                                        attack_sharpness=json_fundamental_volume_env['attack_sharpness'],
                                                        decay_s=json_fundamental_volume_env['decay_s'],
                                                        decay_sharpness=json_fundamental_volume_env['decay_sharpness'])
        
        json_fundamental_pitch_env = json_fundamental_osc['pitch_env']
        fundamental_pitch_env_params = PitchEnvParams(range=json_fundamental_pitch_env['range'],
                                                      attack_s=json_fundamental_pitch_env['attack_s'],
                                                      attack_sharpness=json_fundamental_pitch_env['attack_sharpness'])
        
        json_fundamental_lowpass = json_fundamental_osc['lowpass']
        fundamental_lowpass_params = LowpassParams(mix=json_fundamental_lowpass['mix'],
                                                   cutoff=json_fundamental_lowpass['cutoff'],
                                                   order=json_fundamental_lowpass['order'])
        
        json_fundamental_highpass = json_fundamental_osc['highpass']
        fundamental_lowpass_params = HighpassParams(mix=json_fundamental_highpass['mix'],
                                                    cutoff=json_fundamental_highpass['cutoff'],
                                                    order=json_fundamental_highpass['order'])
        
        fundamental_osc_params = WaveformOscillatorParams(waveform_params=fundamental_waveform_params,
                                                          volume_env_params=fundamental_volume_env_params,
                                                          pitch_env_params=fundamental_pitch_env_params,
                                                          lowpass_params=fundamental_lowpass_params,
                                                          highpass_params=json_fundamental_highpass)
        
        json_floof_osc = json_preset['floof_osc']

        json_floof_waveform = json_floof_osc['waveform']
        floof_waveform_params = WaveformParams(len_s=json_floof_waveform['len_s'],
                                               mix=json_floof_waveform['mix'],
                                               phase=json_floof_waveform['mix'],
                                               fundamental=NoteName(json_floof_waveform['fundamental']),
                                               complexity=json_floof_waveform['complexity'])
        
        json_floof_volume_env = json_floof_osc['volume_env']
        floof_volume_env_params = VolumeEnvParams(attack_s=json_floof_volume_env['attack_s'],
                                                  attack_sharpness=json_floof_volume_env['attack_sharpness'],
                                                  decay_s=json_floof_volume_env['decay_s'],
                                                  decay_sharpness=json_floof_volume_env['decay_sharpness'])
        
        json_floof_pitch_env = json_floof_osc['pitch_env']
        floof_pitch_env_params = PitchEnvParams(range=json_floof_pitch_env['range'],
                                                attack_s=json_floof_pitch_env['attack_s'],
                                                attack_sharpness=json_floof_pitch_env['attack_sharpness'])
        
        json_floof_lowpass = json_floof_osc['lowpass']
        floof_lowpass_params = LowpassParams(mix=json_floof_lowpass['mix'],
                                             cutoff=json_floof_lowpass['cutoff'],
                                             order=json_floof_lowpass['order'])
        
        json_floof_highpass = json_floof_osc['highpass']
        floof_lowpass_params = HighpassParams(mix=json_floof_highpass['mix'],
                                              cutoff=json_floof_highpass['cutoff'],
                                              order=json_floof_highpass['order'])
        
        floof_osc_params = WaveformOscillatorParams(waveform_params=floof_waveform_params,
                                                    volume_env_params=floof_volume_env_params,
                                                    pitch_env_params=floof_pitch_env_params,
                                                    lowpass_params=floof_lowpass_params,
                                                    highpass_params=json_floof_highpass)
        
        return Preset(fundamental_params=fundamental_osc_params,
                      floof_params=floof_osc_params,
                      name=json_preset['name'],
                      ref_path=json_preset['ref_path'])

    def save_presets_to_disk(self,
                             preset_file: str,
                             presets: Dict[UUID, Preset]) -> None:
        
        self.presets = copy.deepcopy(presets)
        json_presets = []
        for preset_id in self.presets:
            json_presets.append(self.preset_to_json(self.presets[preset_id]))

        with open(preset_file, 'w') as outfile:
            outfile.write(json.dumps(json_presets))

    def preset_to_json(self,
                       preset: Preset) -> object:
        
        json_preset = {
            'name': preset.name,
            'ref_path': preset.ref_path,
            'fundamental_osc': {
                'waveform': {
                    'len_s': preset.fundamental_params.waveform_params.len_s,
                    'mix': preset.fundamental_params.waveform_params.mix,
                    'phase': preset.fundamental_params.waveform_params.phase,
                    'fundamental': preset.fundamental_params.waveform_params.fundamental.value,
                    'complexity': preset.fundamental_params.waveform_params.complexity
                },
                'volume_env': {
                    'attack_s': preset.fundamental_params.volume_env_params.attack_s,
                    'attack_sharpness': preset.fundamental_params.volume_env_params.attack_sharpness,
                    'decay_s': preset.fundamental_params.volume_env_params.decay_s,
                    'decay_sharpness': preset.fundamental_params.volume_env_params.decay_sharpness
                },
                'pitch_env': {
                    'range': preset.fundamental_params.pitch_env_params.range,
                    'attack_s': preset.fundamental_params.pitch_env_params.attack_s,
                    'attack_sharpness': preset.fundamental_params.pitch_env_params.attack_sharpness
                },
                'lowpass': {
                    'mix': preset.fundamental_params.lowpass_params.mix,
                    'cutoff': preset.fundamental_params.lowpass_params.cutoff,
                    'order': preset.fundamental_params.lowpass_params.order
                },
                'highpass': {
                    'mix': preset.fundamental_params.highpass_params.mix,
                    'cutoff': preset.fundamental_params.highpass_params.cutoff,
                    'order': preset.fundamental_params.highpass_params.order
                }
            },
            'floof_osc': {
                'waveform': {
                    'len_s': preset.floof_params.waveform_params.len_s,
                    'mix': preset.floof_params.waveform_params.mix,
                    'phase': preset.floof_params.waveform_params.phase,
                    'fundamental': preset.floof_params.waveform_params.fundamental.value,
                    'complexity': preset.floof_params.waveform_params.complexity
                },
                'volume_env': {
                    'attack_s': preset.floof_params.volume_env_params.attack_s,
                    'attack_sharpness': preset.floof_params.volume_env_params.attack_sharpness,
                    'decay_s': preset.floof_params.volume_env_params.decay_s,
                    'decay_sharpness': preset.floof_params.volume_env_params.decay_sharpness
                },
                'pitch_env': {
                    'range': preset.floof_params.pitch_env_params.range,
                    'attack_s': preset.floof_params.pitch_env_params.attack_s,
                    'attack_sharpness': preset.floof_params.pitch_env_params.attack_sharpness
                },
                'lowpass': {
                    'mix': preset.floof_params.lowpass_params.mix,
                    'cutoff': preset.floof_params.lowpass_params.cutoff,
                    'order': preset.floof_params.lowpass_params.order
                },
                'highpass': {
                    'mix': preset.floof_params.highpass_params.mix,
                    'cutoff': preset.floof_params.highpass_params.cutoff,
                    'order': preset.floof_params.highpass_params.order
                }
            }
        }
    
        return json.dumps(json_preset)
