import os
import threading
from cli_helpers import CLIHelpers
from wav_generator import WAVGenerator
from IPython.display import Audio
import warnings
from datetime import datetime
import scipy.io.wavfile

class MainApp:
    def __init__(self):
        self.wav_generation_done_flag = False
        self.cli = CLIHelpers()
        self.wav_gen = None

    def wav_generation_done(self):
        return self.wav_generation_done_flag

    def run(self):
        warnings.filterwarnings('ignore', message='torch.nn.utils.weight_norm is deprecated')

        self.cli.display_logo()
        self.cli.print_green("Welcome to the AI WAV Generator!")

        while True:  # Loop starts here
            self.wav_generation_done_flag = False  # Reset the flag
            length, quality, bpm, musical_key, mood, artists, sound_type = self.cli.get_user_input()
            self.wav_gen = WAVGenerator(length, quality, bpm, musical_key, mood, artists, sound_type)

            if self.cli.confirm_and_generate(length, quality, bpm, musical_key, mood, artists, sound_type):
                # Start the animated pattern and timer thread
                pattern_timer_thread = threading.Thread(target=self.cli.display_animated_wave_with_timer, args=(self.wav_generation_done,), daemon=True)
                pattern_timer_thread.start()

                try:
                    self.wav_gen.generate()  # Generate audio and store it in WAVGenerator
                    self.wav_generation_done_flag = True

                    # Preview the generated audio
                    self.cli.print_green("\nPreviewing the generated audio...")
                    sampling_rate = self.wav_gen.generated_sampling_rate
                    Audio(self.wav_gen.generated_audio_data, rate=sampling_rate)
                    
                    # Ask the user if they want to save the audio
                    save_audio = self.cli.input_grey("Do you want to save this audio? (yes/no): ").strip().lower()
                    if save_audio == 'yes':
                        # Save the audio using the stored data and sampling rate
                        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                        sample_name = f"{self.wav_gen.musical_key}_{self.wav_gen.bpm}BPM_{self.wav_gen.length}_{self.wav_gen.mood}_{self.wav_gen.sound_type}_{timestamp}.wav"
                        output_path = os.path.join('output', sample_name)
                        scipy.io.wavfile.write(output_path, rate=self.wav_gen.generated_sampling_rate, data=self.wav_gen.generated_audio_data)
                    
                    self.cli.print_green("\nDone ✅")
                    
                except Exception as e:
                    self.cli.print_green(f"An error occurred: {e}")

                # Stop the animated pattern and timer thread
                pattern_timer_thread.join(0)

                # Prompt the user to continue or exit
                if not self.cli.prompt_continue_or_exit():
                    self.cli.print_green("Exiting the program. Goodbye! 👋")
                    break

if __name__ == "__main__":
    app = MainApp()
    app.run()
