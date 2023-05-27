import sys
sys.path.append('..')
from oscillator_params import WaveformParams, WaveformOscillatorParams, VolumeEnvParams, PitchEnvParams, HighpassParams, LowpassParams
from waveform_oscillator_component import WaveformOscillatorComponent
from note_name import NoteName
from util import FilterOrder
from synthesizer import Synthesizer

class WaveformOscillatorController:
    def __init__(self,
                 is_fundamental_osc: bool,
                 synthesizer: Synthesizer,
                 osc_component: WaveformOscillatorComponent,
                 len_s: float):
        self.is_fundamental_osc = is_fundamental_osc
        self.synthesizer = synthesizer
        self.osc_component = osc_component
        self.len_s = len_s

        # send callbacks to component
        self.osc_component.set_generate_buff_callback(self.generate_buff)
        self.osc_component.set_reapply_supps_callback(self.reapply_supps)

        # generate the init waveform
        self.generate_buff()

    def set_len_s_and_regen(self,
                  len_s: float) -> None:
        """
        Set the length of the oscillator and regenerate.

        - len_s: float
        """
        self.len_s = len_s
        self.generate_buff()

    def get_waveform_params(self) -> WaveformParams:
        """
        Internal helper function to retrieve the WaveformParams.
        """
        return WaveformParams(len_s=self.len_s,
                              mix=self.osc_component.waveform_mix.get(),
                              phase=self.osc_component.waveform_phase.get(),
                              fundamental=NoteName[self.osc_component.waveform_note.get()],
                              complexity=0) # NEED COMPLEXITY
    
    def get_pitch_env_params(self) -> PitchEnvParams:
        """
        Internal helper function to retrieve the PitchEnvParams.
        """
        return PitchEnvParams(range=self.osc_component.pitch_env_range.get(),
                              attack_s=self.osc_component.pitch_env_attack_len.get(), # NEED TO IMPLEMENT ON BACKEND
                              sharpness=self.osc_component.pitch_env_attack_sharpness.get())
    
    def get_volume_env_params(self) -> VolumeEnvParams:
        """
        Internal helper function to retrieve the VolumeEnvParams.
        """
        return VolumeEnvParams(attack_s=self.osc_component.volume_env_attack_len.get(),
                               attack_sharpness=self.osc_component.volume_env_attack_sharpness.get(),
                               decay_s=self.osc_component.volume_env_decay_len.get(),
                               decay_sharpness=self.osc_component.volume_env_decay_sharpness.get())
    
    def get_lowpass_params(self) -> LowpassParams:
        """
        Internal helper function to retrieve the LowpassParams.
        """
        return LowpassParams(mix=self.osc_component.lowpass_mix.get(),
                             cutoff=self.osc_component.lowpass_cutoff.get(),
                             order=FilterOrder(self.osc_component.lowpass_order.get()))
    
    def get_highpass_params(self) -> HighpassParams:
        """
        Internal helper function to retrieve the HighpassParams.
        """
        return HighpassParams(mix=self.osc_component.highpass_mix.get(),
                              cutoff=self.osc_component.highpass_cutoff.get(),
                              order=FilterOrder(self.osc_component.highpass_order.get()))
    
    def get_waveform_oscillator_params(self) -> WaveformOscillatorParams:
        """
        Internal helper function to retrieve the WaveformOscillatorParams.
        """
        return WaveformOscillatorParams(waveform_params=self.get_waveform_params(),
                                        volume_env_params=self.get_volume_env_params(),
                                        pitch_env_params=self.get_pitch_env_params(),
                                        lowpass_params=self.get_lowpass_params(),
                                        highpass_params=self.get_highpass_params())

    def generate_buff(self,) -> None:
        """
        Generate the entire buffer, including supplementaries (volume, filter).
        """
        waveform_osc_params = self.get_waveform_oscillator_params()
        
        if self.is_fundamental_osc:
            self.synthesizer.submit_new_fundamental(fundamental_params=waveform_osc_params)
        else:
            self.synthesizer.submit_new_floof(floof_params=waveform_osc_params)

    def reapply_supps(self,) -> None:
        """
        Use the previously-generated bare buffer to only apply supplementaries (volume, filter).
        """

        volume_env_params = self.get_volume_env_params()
        lowpass_params = self.get_lowpass_params()
        highpass_params = self.get_highpass_params()
        
        if self.is_fundamental_osc:
            self.synthesizer.submit_new_fundamental_supps(volume_env_params=volume_env_params,
                                                          lowpass_params=lowpass_params,
                                                          highpass_params=highpass_params)
        else:
            self.synthesizer.submit_new_floof_supps(volume_env_params=volume_env_params,
                                                    lowpass_params=lowpass_params,
                                                    highpass_params=highpass_params)