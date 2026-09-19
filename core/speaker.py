import asyncio
import edge_tts
import pygame
import os
import tempfile

# Initialize the audio player once when the module loads
pygame.mixer.init()

# The voice profile. 
# 'en-GB-RyanNeural' is a professional British male voice (JARVIS vibe).
# Alternatively, try 'en-US-ChristopherNeural' for an American voice.
VOICE = "en-GB-RyanNeural"

async def _generate_audio(text: str, output_path: str):
    """Asynchronously reaches out to Microsoft Edge to generate the audio file."""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)

def speak(text: str):
    """Generates the speech and plays it out loud synchronously."""
    print(f"Leo: {text}")
    
    # 1. Create a secure temporary file to hold our audio
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    
    try:
        # 2. Run the async generation (waits until the file is created)
        asyncio.run(_generate_audio(text, path))
        
        # 3. Load the generated audio into pygame and play it
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        
        # 4. Wait here while the audio is playing so the program doesn't exit early
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        # 5. Unload the file from memory so we can safely delete it
        pygame.mixer.music.unload()
        
    finally:
        # 6. Delete the temporary file to keep the PC clean
        try:
            os.remove(path)
        except OSError:
            pass

# This block allows us to test just this file by running it directly
if __name__ == "__main__":
    speak("Hello sir. All systems are online. I am Leo, your personal artificial intelligence.")

