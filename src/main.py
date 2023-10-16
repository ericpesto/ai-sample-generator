from cli_helpers import CLIHelpers
from timer import Timer
from wav_generator import WAVGenerator
import threading
import warnings

class MainApp:
    def __init__(self):
        self.wav_generation_done_flag = False
        self.cli = CLIHelpers()
        self.timer = Timer(self.wav_generation_done)
        self.wav_gen = None

    def wav_generation_done(self):
        return self.wav_generation_done_flag

    def run(self):
        warnings.filterwarnings('ignore', message='torch.nn.utils.weight_norm is deprecated')

        self.cli.display_logo()
        self.cli.print_green("Welcome to the AI WAV Generator!")
        
        length, quality, bpm, musical_key, mood, artists, sound_type = self.cli.get_user_input()  # Include bpm here
        self.wav_gen = WAVGenerator(length, quality, bpm, musical_key, mood, artists, sound_type)
        
        if self.cli.confirm_and_generate(length, quality, bpm, musical_key, mood, artists, sound_type):
            self.cli.print_green("Starting WAV generation... 🔊")
            
            # Start the timer thread only when the user has confirmed and just before starting the WAV generation
            timer_thread = threading.Thread(target=self.timer.start_timer)
            timer_thread.start()
            
            try:
                self.wav_gen.generate()
                self.wav_generation_done_flag = True
            except Exception as e:
                self.cli.print_green(f"An error occurred: {e}")
            
            # Wait for the timer thread to finish
            timer_thread.join()
            
            self.cli.print_green("Done ✅")

if __name__ == "__main__":
    app = MainApp()
    app.run()

