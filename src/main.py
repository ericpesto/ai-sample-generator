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

    def setup(self):
        warnings.filterwarnings('ignore', message='torch.nn.utils.weight_norm is deprecated')
        self.cli.display_logo()
        self.cli.print_green("Welcome to the AI WAV Generator!")

    def get_user_decision(self):
        user_input = self.cli.input_grey("Do you want to generate another sample? (yes/no): ").strip().lower()
        print(" ")
        return user_input == 'yes'

    def generate_and_preview_audio(self):
        self.wav_gen.generate()
        self.wav_generation_done_flag.set()
        self.cli.print_green("\nPreviewing the generated audio... 🔊")
        
        def play_audio():
            sd.play(self.wav_gen.generated_audio_data, samplerate=self.wav_gen.generated_sampling_rate)
            sd.wait()

        play_audio()  # Play the audio for the first time

        while True:
            replay = self.cli.input_grey("Press 'p' to replay or any other key to continue: ").strip().lower()
            if replay == 'p':
                play_audio()
            else:
                break

    def save_generated_audio(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        sample_name = f"{self.wav_gen.mood}_{self.wav_gen.genre}_{self.wav_gen.sound_type}_{self.wav_gen.length}_{timestamp}.wav"
        output_path = os.path.join('output', sample_name)
        scipy.io.wavfile.write(output_path, rate=self.wav_gen.generated_sampling_rate, data=self.wav_gen.generated_audio_data)
        self.cli.print_green(f"Saved in './{output_path}' 💾")

    def run(self):
        self.setup()
        running = True
        while running:
            self.wav_generation_done_flag.clear()
            user_params = self.cli.get_user_input()
            proceed = self.cli.confirm_and_generate(*user_params)
            
            if not proceed:
                running = self.get_user_decision()
                continue

            self.wav_gen = WAVGenerator(*user_params)

            wave_thread = threading.Thread(target=self.cli.display_animated_wave_with_timer, args=(self.wav_generation_done_flag,))
            wave_thread.start()

            try:
                self.generate_and_preview_audio()
                self.wav_generation_done_flag.set()
                save_audio = self.cli.input_grey("Do you want to save this audio? (yes/no): ").strip().lower()
                if save_audio == 'yes':
                    self.save_generated_audio()
                
                running = self.get_user_decision()
            except Exception as e:
                self.cli.print_red(f"An error occurred: {e}")
                self.wav_generation_done_flag.set()

        self.cli.print_green("Exiting the program. Goodbye! 👋")

if __name__ == "__main__":
    app = MainApp()
    app.run()
