import os
from datetime import datetime
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile

length_mapping = {
    "short": 64,
    "medium": 128,
    "long": 256
}

quality_mapping = {
    "low": "facebook/musicgen-small",
    "medium": "facebook/musicgen-medium",
    "high": "facebook/musicgen-large"  # Replace with the actual high-quality model name
}

def generate_wav(mood, artists, sound_type, length, quality):
    model_name = quality_mapping.get(quality.lower(), "facebook/musicgen-small")  # Default to "low" if the choice is invalid
    processor = AutoProcessor.from_pretrained(model_name)
    model = MusicgenForConditionalGeneration.from_pretrained(model_name)
    
    text_description = f"A {mood} {sound_type} inspired by {artists}. This audio is designed to be loopable."
    inputs = processor(text=[text_description], padding=True, return_tensors="pt")

    max_new_tokens_value = length_mapping.get(length.lower(), 256)  # Default to 256 if the choice is invalid
    audio_values = model.generate(**inputs, max_new_tokens=max_new_tokens_value)

    if not os.path.exists('output'):
        os.makedirs('output')
    
    sampling_rate = model.config.audio_encoder.sampling_rate
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    sample_name = f"{length}_{mood}_{sound_type}_{timestamp}.wav"
    output_path = os.path.join('output', sample_name)
    scipy.io.wavfile.write(output_path, rate=sampling_rate, data=audio_values[0, 0].numpy())
