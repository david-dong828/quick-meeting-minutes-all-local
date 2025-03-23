import logging
import sys
import whisper

"""
Utility module for file processing operations.

This module provides functions for processing audio files and generating output files.
"""

def generate_output_file(filepath, output):
    """
    Write output content to a file.
    
    Args:
        filepath (str): Path where the output will be saved
        output (str): Content to write to the file
    """
    with open(filepath, "w") as f:
        f.write(output)

def process_audio_file_local_model(audio_filepath):
    """
    Transcribe an audio file using the local Whisper model.
    
    Args:
        audio_filepath (str): Path to the audio file to transcribe
        
    Returns:
        str: The transcribed text
        
    Raises:
        SystemExit: If transcription fails
    """
    try:
        logging.info(msg=f"process_audio_file: Processing the audio file '{audio_filepath}'...")
        model = whisper.load_model('base')
        result = model.transcribe(audio_filepath)
        transcript = result['text']
        logging.info(msg=f"process_audio_file: Successfully generated transcription from the audio file '{audio_filepath}'...") 
        return transcript
    except Exception as e:
        logging.critical(msg=f"process_audio_file: Cannot generate transcript from audio file '{audio_filepath}'. Error message: {e}")
        sys.exit(-1)

if __name__=='__main()__':
    process_audio_file_local_model()