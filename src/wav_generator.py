from transformers import AutoProcessor, MusicgenForConditionalGeneration
import numpy as np

class WAVGenerator:
    def __init__(self, length, quality, bpm, musical_key, mood, artists, sound_type):
        self.length = length
        self.quality = quality
        self.bpm = bpm
        self.musical_key = musical_key
        self.mood = mood
        self.artists = artists
        self.sound_type = sound_type

        self.length_mapping = {
            "short": 64,
            "medium": 128,
            "long": 256
        }

        self.quality_mapping = {
            "low": "facebook/musicgen-small",
            "medium": "facebook/musicgen-medium",
            "high": "facebook/musicgen-large"
        }

        self.generated_audio_data = None  # Store generated audio data
        self.generated_sampling_rate = None  # Store generated audio sampling rate

    def generate(self):
        model_name = self.quality_mapping.get(self.quality.lower(), "facebook/musicgen-small")
        processor = AutoProcessor.from_pretrained(model_name)
        model = MusicgenForConditionalGeneration.from_pretrained(model_name)
        
        # text_description = f"A loopable, performance-ready {self.mood} {self.sound_type} sample inspired by {self.artists}. This audio is designed for seamless looping for integration into live sets and compositions so it must be exactly {self.bpm}BPM and in the exact key of {self.musical_key}."
        text_description = f"A loopable, performance-ready {self.mood} {self.sound_type} sample inspired by {self.artists}. This audio is engineered for seamless looping and is optimized for integration into live sets and compositions. It aims to be exactly {self.bpm}BPM and in the key of {self.musical_key}. Note: For critical applications, both the BPM and musical key should be manually verified."
        inputs = processor(text=[text_description], padding=True, return_tensors="pt")

        max_new_tokens_value = self.length_mapping.get(self.length.lower(), 64)
        audio_values = model.generate(**inputs, max_new_tokens=max_new_tokens_value)

        # Store the generated audio data and sampling rate as class attributes
        self.generated_audio_data = audio_values[0, 0].numpy().astype(np.float32)
        self.generated_sampling_rate = model.config.audio_encoder.sampling_rate
