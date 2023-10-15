import os
from datetime import datetime
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile
import time

def generate_wav(speed, mood, artists, sound_type):
    start_time = time.time()  # Record the start time
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-medium")
    
    text_description = f"A {speed} {mood} {sound_type} inspired by {artists}. This audio is designed to be loopable."
    inputs = processor(text=[text_description], padding=True, return_tensors="pt")
    
    audio_values = model.generate(**inputs, max_new_tokens=256)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Sound generation took {elapsed_time:.2f} seconds.")  # Display the elapsed time
    
    if not os.path.exists('output'):
        os.makedirs('output')
    
    sampling_rate = model.config.audio_encoder.sampling_rate
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    sample_name = f"{speed}_{mood}_{sound_type}_{timestamp}.wav"
    output_path = os.path.join('output', sample_name)
    scipy.io.wavfile.write(output_path, rate=sampling_rate, data=audio_values[0, 0].numpy())
