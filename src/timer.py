import time

def timer(wav_generation_done):
    start_time = time.time()
    spinner = "|/-\\"
    spin_count = 0

    while not wav_generation_done():
        elapsed_time = time.time() - start_time
        spin_symbol = spinner[spin_count % len(spinner)]
        print(f"\rElapsed time: {elapsed_time:.2f} seconds {spin_symbol}", end="")
        spin_count += 1
        time.sleep(1)

    print()  # Move to the next line after loop ends
