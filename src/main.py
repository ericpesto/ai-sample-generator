from wav_generator import generate_wav

def main():
    print("Welcome to the AI WAV Generator!")
    
    # Collect parameters through a Q/A dialogue
    speed = input("How fast do you want your sound? (Default: slow) ") or 'slow'
    mood = input("What mood are you going for? (Default: beautiful) ") or 'beautiful'
    artists = input("What artists would you like to sound like? (Default: boards of canada) ") or 'boards of canada'
    sound_type = input("What type of sound would you like? (Default: synth pad) ") or 'synth pad'
    
    # Print a summary of the user's choices
    print(f"\nYou chose the following settings:")
    print(f"Speed: {speed}")
    print(f"Mood: {mood}")
    print(f"Artists: {artists}")
    print(f"Type of Sound: {sound_type}")
    # musical key?
    # effects?
    
    # Confirm before generating
    confirm = input("\nDo you want to proceed with these settings? (yes/no) ").lower()
    if confirm == 'yes':
        # Call your core functionality here
        generate_wav(speed=speed, mood=mood, artists=artists, sound_type=sound_type)
        print("Generating WAV file...")
    else:
        print("Aborted. Run the program again to try different settings.")

if __name__ == "__main__":
    main()
