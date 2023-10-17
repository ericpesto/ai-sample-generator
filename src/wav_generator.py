from transformers import AutoProcessor, MusicgenForConditionalGeneration
import numpy as np

class WAVGenerator:
    length_mapping = {
        "short": 64,
        "medium": 128,
        "long": 256
    }

    quality_mapping = {
        "low": "facebook/musicgen-small",
        "medium": "facebook/musicgen-medium",
        "high": "facebook/musicgen-large"
    }

    def __init__(self, length, quality, bpm, musical_key, mood, artists, sound_type):
        self.length = length
        self.quality = quality
        self.bpm = bpm
        self.musical_key = musical_key
        self.mood = mood
        self.artists = artists
        self.sound_type = sound_type
        self.generated_audio_data = None
        self.generated_sampling_rate = None

    def init_model(self):
        model_name = self.quality_mapping.get(self.quality.lower(), "facebook/musicgen-small")
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = MusicgenForConditionalGeneration.from_pretrained(model_name)

    def generate_text_description(self):
        return f"A loopable, performance-ready {self.mood} {self.sound_type} sample inspired by {self.artists}. This audio is engineered for seamless looping and it aims to be exactly {self.bpm}BPM and in the key of {self.musical_key}."

    def generate(self):
        self.init_model()
        text_description = self.generate_text_description()
        inputs = self.processor(text=[text_description], padding=True, return_tensors="pt")
        max_new_tokens_value = self.length_mapping.get(self.length.lower(), 64)
        audio_values = self.model.generate(**inputs, max_new_tokens=max_new_tokens_value)
        self.generated_audio_data = audio_values[0, 0].numpy().astype(np.float32)
        self.generated_sampling_rate = self.model.config.audio_encoder.sampling_rate
