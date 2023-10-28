from termcolor import colored
import time

class CLIHelpers:
    def __init__(self):
        self.stop_animated_pattern_flag = False

    def print_green(self, text, **kwargs):
        print(f"\033[32m{text}\033[0m", **kwargs)  # ANSI code for regular green is \033[32m

    def print_orange(self, text, **kwargs):
        print(f"\033[91m{text}\033[0m", **kwargs)
    
    def print_red(self, text, **kwargs):
        print(f"\033[91m{text}\033[0m", **kwargs)

    def print_cyan(self, text, **kwargs):
        print(f"\033[96m{text}\033[0m", **kwargs)

    def input_grey(self, prompt):
        print(f"\033[39m{prompt}\033[0m", end='')
        return input()

    def display_logo(self):
        print(" ")
        print("\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m\033[0m")
        print(" ")
        print("           \033[97mw  a  v  .  a  i\033[0m") 
        print(" ")
        print("\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m\033[0m")
        print(" ")

    def display_animated_wave_with_timer(self, wav_generation_done):
        start_time = time.time()
        base_wave_pattern = "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁"
        long_wave_pattern = base_wave_pattern * 3 
        wave_length = len(base_wave_pattern)
        wave_count = 0

        self.stop_animated_pattern_flag = False  # Reset the flag

        while not wav_generation_done.is_set() and not self.stop_animated_pattern_flag:
            elapsed_time = time.time() - start_time
            start_index = wave_count % wave_length
            end_index = start_index + wave_length
            wave = long_wave_pattern[start_index:end_index]
            print(f"\r\033[35mGenerating WAV...\033[0m \033[32m{wave}\033[0m \033[35m(Elapsed time: {elapsed_time:.2f} seconds)\033[0m", end='', flush=True)
            wave_count += 1
            time.sleep(0.2)

    def stop_animated_pattern(self):
        self.stop_animated_pattern_flag = True

    def get_user_input(self):
        valid_lengths = ['short', 'medium', 'long']
        valid_qualities = ['low', 'medium', 'high']

        length = ''
        while length not in valid_lengths:
            length = self.input_grey("What length do you want for your sample? (short/\033[1mmedium\033[0m\033[39m/long) ").lower() or 'medium'
            if length not in valid_lengths:
                self.print_orange("Invalid option. Please choose from 'short', 'medium', or 'long'.")

        quality = ''
        while quality not in valid_qualities:
            quality = self.input_grey("What quality do you want for your sample? (\033[1mlow\033[0m\033[39m/medium/high) ").lower() or 'low'
            if quality not in valid_qualities:
                self.print_orange("Invalid option. Please choose from 'low', 'medium', or 'high'.")

        mood = self.input_grey("What mood are you going for? (Default: beautiful lofi) ") or 'beautiful lofi'
        artists = self.input_grey("What artists would you like to sound like? (Default: boards of canada) ") or 'boards of canada'
        sound_type = self.input_grey("What type of sound would you like? (Default: synth pad) ") or 'synth pad'

        return length, quality, mood, artists, sound_type

    def confirm_and_generate(self, length, quality, mood, artists, sound_type):
        self.print_cyan(f"\nYou chose the following settings:")
        self.print_cyan(f"Length: {length}")
        self.print_cyan(f"Quality: {quality}")
        self.print_cyan(f"Mood: {mood}")
        self.print_cyan(f"Artists: {artists}")
        self.print_cyan(f"Type of Sound: {sound_type}")

        confirm = self.input_grey("\nDo you want to proceed with these settings? (yes/no) ").lower()
        return confirm == 'yes'
    