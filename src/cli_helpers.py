from termcolor import colored
import time

class CLIHelpers:
    def __init__(self):
        self.stop_animated_pattern_flag = False

    def print_green(self, text, **kwargs):
        print(colored(text, 'green'), **kwargs)
    
    def print_cyan(self, text, **kwargs):
        print(colored(text, 'cyan'), **kwargs)

    def input_grey(self, prompt):
        print(colored(prompt, 'grey'), end='')
        return input()

    def display_logo(self):
        print(" ")
        print("\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m\033[0m")
        print(" ")
        print("         \033[90mw  a  v  .  a  i\033[0m")
        print(" ")
        print("\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m\033[0m")
        print(" ")

    def display_animated_wave_with_timer(self, wav_generation_done):
        start_time = time.time()
        base_wave_pattern = "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁"
        long_wave_pattern = base_wave_pattern * 3 
        wave_length = len(base_wave_pattern)
        wave_count = 0

        while not wav_generation_done():
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
        valid_keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        length = ''
        while length not in valid_lengths:
            length = self.input_grey("What length do you want for your sample? (short/\033[1mmedium\033[0m\033[90m/long) ").lower() or 'medium'
            if length not in valid_lengths:
                self.print_green("Invalid option. Please choose from 'short', 'medium', or 'long'.")

        quality = ''
        while quality not in valid_qualities:
            quality = self.input_grey("What quality do you want for your sample? (\033[1mlow\033[0m\033[90m/medium/high) ").lower() or 'low'
            if quality not in valid_qualities:
                self.print_green("Invalid option. Please choose from 'low', 'medium', or 'high'.")
        bpm = self.input_grey("What BPM do you want for your sample? (Default: 120) ") or '120'
        musical_key = ''
        while musical_key not in valid_keys:
            musical_key = self.input_grey("What musical key do you want for your sample? (Default: C) ").upper() or 'C'
            if musical_key not in valid_keys:
                self.print_green("Invalid option. Please choose a valid musical key.")

        mood = self.input_grey("What mood are you going for? (Default: beautiful) ") or 'beautiful'
        artists = self.input_grey("What artists would you like to sound like? (Default: boards of canada) ") or 'boards of canada'
        sound_type = self.input_grey("What type of sound would you like? (Default: synth pad) ") or 'synth pad'

        return length, quality, bpm, musical_key, mood, artists, sound_type

    def confirm_and_generate(self, length, quality, bpm, musical_key, mood, artists, sound_type):
        self.print_green(f"\nYou chose the following settings:")
        self.print_green(f"Length: {length}")
        self.print_green(f"Quality: {quality}")
        self.print_green(f"BPM: {bpm}")
        self.print_green(f"Musical Key: {musical_key}")
        self.print_green(f"Mood: {mood}")
        self.print_green(f"Artists: {artists}")
        self.print_green(f"Type of Sound: {sound_type}")

        confirm = self.input_grey("\nDo you want to proceed with these settings? (yes/no) ").lower()
        return confirm == 'yes'
    
    def prompt_continue_or_exit(self):
        print("")
        user_choice = self.input_grey("Do you want to generate another sample? (yes/no): ").strip().lower()
        return user_choice == 'yes'
