import os
from datetime import datetime
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile

def generate_wav(speed, mood, artists, sound_type):
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
    
    text_description = f"A {speed} {mood} {sound_type} inspired by {artists}."
    inputs = processor(text=[text_description], padding=True, return_tensors="pt")
    
    audio_values = model.generate(**inputs, max_new_tokens=256)
    
    if not os.path.exists('output'):
        os.makedirs('output')
    
    sampling_rate = model.config.audio_encoder.sampling_rate
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    sample_name = f"{speed}_{mood}_{sound_type}_{timestamp}.wav"
    output_path = os.path.join('output', sample_name)
    scipy.io.wavfile.write(output_path, rate=sampling_rate, data=audio_values[0, 0].numpy())
