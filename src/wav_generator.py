import os
from datetime import datetime
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile

class WAVGenerator:
    def __init__(self, mood, artists, sound_type, length, quality):
        self.mood = mood
        self.artists = artists
        self.sound_type = sound_type
        self.length = length
        self.quality = quality

        self.length_mapping = {
            "short": 64,
            "medium": 128,
            "long": 256
        }

        self.quality_mapping = {
            "low": "facebook/musicgen-small",
            "medium": "facebook/musicgen-medium",
            "high": "facebook/musicgen-large"  # Replace with the actual high-quality model name
        }

    def generate(self):
        model_name = self.quality_mapping.get(self.quality.lower(), "facebook/musicgen-small")
        processor = AutoProcessor.from_pretrained(model_name)
        model = MusicgenForConditionalGeneration.from_pretrained(model_name)
        
        text_description = f"A {self.mood} {self.sound_type} inspired by {self.artists}. This audio is designed to be loopable."
        inputs = processor(text=[text_description], padding=True, return_tensors="pt")

        max_new_tokens_value = self.length_mapping.get(self.length.lower(), 256)
        audio_values = model.generate(**inputs, max_new_tokens=max_new_tokens_value)

        if not os.path.exists('output'):
            os.makedirs('output')
        
        sampling_rate = model.config.audio_encoder.sampling_rate
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        sample_name = f"{self.length}_{self.mood}_{self.sound_type}_{timestamp}.wav"
        output_path = os.path.join('output', sample_name)
        scipy.io.wavfile.write(output_path, rate=sampling_rate, data=audio_values[0, 0].numpy())
