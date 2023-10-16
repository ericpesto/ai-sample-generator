from termcolor import colored

class CLIHelpers:
    def print_green(self, text, **kwargs):
        print(colored(text, 'green'), **kwargs)

    def input_grey(self, prompt):
        print(colored(prompt, 'grey'), end='')
        return input()

    def display_logo(self):
        print(" ")
        print("\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m\033[0m")
        print("         \033[90mW  A  V  .  A  I\033[0m")  # Grey text
        print("\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m \\\033[0m\033[92m \\\033[0m\033[93m \\\033[0m\033[95m \\\033[0m\033[96m \\\033[0m\033[91m \\\033[0m\033[94m\033[0m")
        print(" ")

    def get_user_input(self):
        valid_lengths = ['short', 'medium', 'long']
        valid_qualities = ['low', 'medium', 'high']

        length = ''
        while length not in valid_lengths:
            length = self.input_grey("What length do you want for your sample? (\033[1mshort\033[0m\033[90m/medium/long) ").lower() or 'short'
            if length not in valid_lengths:
                self.print_green("Invalid option. Please choose from 'short', 'medium', or 'long'.")

        quality = ''
        while quality not in valid_qualities:
            quality = self.input_grey("What quality do you want for your sample? (\033[1mlow\033[0m\033[90m/medium/high) ").lower() or 'low'
            if quality not in valid_qualities:
                self.print_green("Invalid option. Please choose from 'low', 'medium', or 'high'.")

        mood = self.input_grey("What mood are you going for? (Default: beautiful) ") or 'beautiful'
        artists = self.input_grey("What artists would you like to sound like? (Default: boards of canada) ") or 'boards of canada'
        sound_type = self.input_grey("What type of sound would you like? (Default: synth pad) ") or 'synth pad'

        return length, quality, mood, artists, sound_type

    def confirm_and_generate(self, length, quality, mood, artists, sound_type):
        self.print_green(f"\nYou chose the following settings:")
        self.print_green(f"Length: {length}")
        self.print_green(f"Quality: {quality}")
        self.print_green(f"Mood: {mood}")
        self.print_green(f"Artists: {artists}")
        self.print_green(f"Type of Sound: {sound_type}")

        confirm = self.input_grey("\nDo you want to proceed with these settings? (yes/no) ").lower()
        return confirm == 'yes'
