import tkinter as tk
from datetime import datetime
import sounddevice as sd
import soundfile as sf
import os
import threading
from pathlib import Path

"""
GUI module for audio recording.

This module provides a graphical user interface for recording audio files.
"""

class AudioRecorderGUI:
    """
    A GUI class for recording audio.
    
    This class provides a simple interface with start and stop buttons
    for recording audio through the system's microphone.
    """
    
    def __init__(self, master):
        """
        Initialize the AudioRecorderGUI.
        
        Args:
            master: The tkinter root window
        """
        self.master = master
        self.master.title("Audio Recorder")

        self.recording = False
        self.audio_data = []
        self.sample_rate = 16000
        self.channels = 1
        self.saved_filepath = None  

        self.start_button = tk.Button(master, text="Start Recording", command=self.start_recording, width=20, height=2, bg="green", fg="white")
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording, width=20, height=2, bg="red", fg="white", state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(master, text="", fg="blue")
        self.status_label.pack()

    def start_recording(self):
        """Start recording audio from the microphone."""
        self.status_label.config(text="Recording...")
        self.recording = True
        self.audio_data = []
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Start recording in a new thread so GUI doesn't freeze
        threading.Thread(target=self.record_audio, daemon=True).start()

    def stop_recording(self):
        """Stop recording audio."""
        self.status_label.config(text="Recording stopped.")
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text='Stopped. Saving...')

    def record_audio(self):
        """Record audio in a separate thread."""
        with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, dtype='int16', callback=self.callback):
            while self.recording:
                sd.sleep(100)

        self.save_audio()
        self.master.destroy() # Close the GUI after saving

    def callback(self, indata, frames, time, status):
        """Callback function for the audio stream."""
        if self.recording:
            self.audio_data.append(indata.copy())

    def save_audio(self):
        """Save the recorded audio to a file."""
        if not self.audio_data:
            self.status_label.config(text="No audio recorded.")
            return
        
        import numpy as np
        audio_array = np.concatenate(self.audio_data)

        # Save to ../files
        output_dir = os.path.join(
            Path(os.path.join(Path(__file__).parent.parent)).parent.absolute(),
            'audios')
        os.makedirs(output_dir, exist_ok=True)
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M") + ".wav"
        filepath = os.path.join(output_dir, filename)

        sf.write(filepath, audio_array, self.sample_rate)
        self.saved_filepath = filepath
        self.status_label.config(text=f" Audio saved to: {filepath}")


def record_return_filepath():
    """
    Launch the audio recorder GUI and return the path to the saved audio file.
    
    Returns:
        str: Path to the saved audio file, or None if recording failed
    """
    root = tk.Tk()
    root.title('Meeting Minutes Audio Recorder')
    app = AudioRecorderGUI(root)
    root.mainloop()
    return app.saved_filepath

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorderGUI(root)
    root.mainloop()
