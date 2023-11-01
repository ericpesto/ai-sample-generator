from transformers import AutoProcessor, MusicgenForConditionalGeneration
import numpy as np

class WAVGenerator:
    length_mapping = {
        "short": 128,
        "medium": 256,
        "long": 512
    }

    quality_mapping = {
        "low": "facebook/musicgen-small",
        "medium": "facebook/musicgen-medium",
        "high": "facebook/musicgen-large"
    }

    def __init__(self, length, quality, mood, genre, sound_type):
        self.length = length
        self.quality = quality
        self.mood = mood
        self.genre = genre
        self.sound_type = sound_type
        self.generated_audio_data = None
        self.generated_sampling_rate = None

    def init_model(self):
        model_name = self.quality_mapping.get(self.quality.lower(), "facebook/musicgen-small")
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = MusicgenForConditionalGeneration.from_pretrained(model_name)

    def generate_text_description(self):
        return f"A loopable, performance-ready {self.mood} {self.genre} {self.sound_type} sample."

    def generate(self):
        self.init_model()
        text_description = self.generate_text_description()
        inputs = self.processor(text=[text_description], padding=True, return_tensors="pt")
        max_new_tokens_value = self.length_mapping.get(self.length.lower(), 64)
        audio_values = self.model.generate(**inputs, max_new_tokens=max_new_tokens_value)
        self.generated_audio_data = audio_values[0, 0].numpy().astype(np.float32)
        self.generated_sampling_rate = self.model.config.audio_encoder.sampling_rate
