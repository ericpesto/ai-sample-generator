import time
from cli_helpers import CLIHelpers

class Timer:
    def __init__(self, wav_generation_done):
        self.wav_generation_done = wav_generation_done
        self.cli_helper = CLIHelpers()

    def start_timer(self):
        start_time = time.time()
        spinner = "|/-\\"
        spin_count = 0

        while not self.wav_generation_done():
            elapsed_time = time.time() - start_time
            spin_symbol = spinner[spin_count % len(spinner)]
            self.cli_helper.print_green(f"\rElapsed time: {elapsed_time:.2f} seconds {spin_symbol}", end="")
            spin_count += 1
            time.sleep(1)

        print()
