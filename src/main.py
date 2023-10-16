import threading
from cli_helpers import CLIHelpers  # Make sure CLIHelpers includes the new display_animated_wave_with_timer method
from wav_generator import WAVGenerator
import warnings

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
                    self.wav_gen.generate()
                    self.wav_generation_done_flag = True
                except Exception as e:
                    self.cli.print_green(f"An error occurred: {e}")

                # Stop the animated pattern and timer thread
                pattern_timer_thread.join(0)

                self.cli.print_green("\nDone ✅")

            # Prompt the user to continue or exit
            if not self.cli.prompt_continue_or_exit():
                self.cli.print_green("Exiting the program. Goodbye! 👋")
                break

if __name__ == "__main__":
    app = MainApp()
    app.run()
