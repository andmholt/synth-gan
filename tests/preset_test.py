import sys
sys.path.append('..')
from preset import PresetHandler, Preset

preset_handler = PresetHandler()

preset_handler.insert_init_preset(name='test_preset')

preset_handler.save_presets_to_disk(preset_file='test_presets.json')