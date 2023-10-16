import os
import threading
from cli_helpers import CLIHelpers
import warnings
from datetime import datetime
import scipy.io.wavfile
from wav_generator import WAVGenerator
import sounddevice as sd

class MainApp:
    def __init__(self):
        self.wav_generation_done_flag = threading.Event()
        self.cli = CLIHelpers()
        self.wav_gen = None

    def run(self):
        warnings.filterwarnings('ignore', message='torch.nn.utils.weight_norm is deprecated')

        self.cli.display_logo()
        self.cli.print_green("Welcome to the AI WAV Generator!")

        running = True

        while running:
            self.wav_generation_done_flag.clear()
            length, quality, bpm, musical_key, mood, artists, sound_type = self.cli.get_user_input()

            proceed = self.cli.confirm_and_generate(length, quality, bpm, musical_key, mood, artists, sound_type)
            
            if not proceed:
                user_input = self.cli.input_grey("Do you want to generate another sample? (yes/no): ").strip().lower()
                if user_input != 'yes':
                    running = False
                    break
                else:
                    continue

            self.wav_gen = WAVGenerator(length, quality, bpm, musical_key, mood, artists, sound_type)
            pattern_timer_thread = threading.Thread(target=self.cli.display_animated_wave_with_timer, args=(self.wav_generation_done_flag,), daemon=True)
            pattern_timer_thread.start()

            try:
                self.wav_gen.generate()
                self.wav_generation_done_flag.set()

                self.cli.print_green("\nPreviewing the generated audio... 🔊")
                sd.play(self.wav_gen.generated_audio_data, samplerate=self.wav_gen.generated_sampling_rate)
                sd.wait()

                save_audio = self.cli.input_grey("Do you want to save this audio? (yes/no): ").strip().lower()
                if save_audio == 'yes':
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    sample_name = f"{self.wav_gen.musical_key}_{self.wav_gen.bpm}BPM_{self.wav_gen.length}_{self.wav_gen.mood}_{self.wav_gen.sound_type}_{timestamp}.wav"
                    output_path = os.path.join('output', sample_name)
                    scipy.io.wavfile.write(output_path, rate=self.wav_gen.generated_sampling_rate, data=self.wav_gen.generated_audio_data)
                    self.cli.print_green(f"Saved in './{output_path}' 💾")

            except Exception as e:
                self.cli.print_red(f"An error occurred: {e}")

            pattern_timer_thread.join()

            user_input = self.cli.input_grey("Do you want to generate another sample? (yes/no): ").strip().lower()
            if user_input != 'yes':
                running = False

        self.cli.print_green("Exiting the program. Goodbye! 👋")

if __name__ == "__main__":
    app = MainApp()
    app.run()
