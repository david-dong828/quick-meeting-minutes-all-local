import argparse
import os
import sys
from utils.file_processor import generate_output_file,process_audio_file_local_model
from utils.record_gui import record_return_filepath
from models.llama3 import generate_outputs_ollama
from pathlib import Path
from datetime import datetime

"""
Main module for the QuickMeet application.

This module provides the main functionality for the QuickMeet application,
which transcribes audio recordings and generates meeting minutes.
"""

def stt_summary(audio_filepath, savedTransactionFile, local_llm, output_filepath):
    """
    Process an audio file to generate meeting minutes.
    
    Args:
        audio_filepath (str): Path to the audio file to process
        savedTransactionFile (str): Path where the transcript will be saved
        local_llm (str): Name of the local LLM model to use
        output_filepath (str): Path where the meeting minutes will be saved
    """
    
    if not os.path.isfile(savedTransactionFile):
        # use local whisper model 
        transcript = process_audio_file_local_model(
            audio_filepath=audio_filepath
        )
        # Save the transcript
        generate_output_file(filepath = savedTransactionFile, output=transcript) 
    else:
        with open(savedTransactionFile,'r') as f:
            transcript = f.read()

    # Set up prompt
    system_msg = "I am an assistant that takes in an audio transcript and then provides summary, key discussion points, takeaways and list of action items"
    user_prompt = f"Here is a meeting audio transcript. Please provide the location, date and summary of the meeting with attendees, and list of action items accoridingly: \n\n {transcript}"
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_prompt}
    ]

    # Update: Using Ollama instead 
    outputs = generate_outputs_ollama(
        audio_filepath,
        messages,
        local_llm
    )

    
    # Write outputs to Markdown file
    generate_output_file(filepath=output_filepath, output=outputs)


def main():
    """
    Main entry point for the QuickMeet application.
    
    Parses command line arguments and initiates the audio processing workflow.
    """

    # Get arguments from script command execution
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio_filepath", "-f", help="Path to the audio file.")
    parser.add_argument("--record", action='store_true', help='Launch GUI to record new audio')
    args = parser.parse_args()
   

    if args.record:
        print("Launching GUI recorder ...")
        filePath = record_return_filepath()
        
        if not filePath:
            print("Recording failed or canceled.")
            sys.exit(1)
        audio_filepath = filePath
    else:
        if not args.audio_filepath:
            print("Please provide --audio_filepath or use --record")
            sys.exit(1)
        audio_filepath = args.audio_filepath
    # Initialize required variables

    output_dir = os.path.join(
            Path(os.path.join(Path(__file__).parent)).parent.absolute(),
            'files')
    os.makedirs(output_dir, exist_ok=True)
    
    output_fileName = 'Meeting Minutes_' + datetime.now().strftime("%Y-%m-%d_%H-%M") + ".md"
    savedTransactionFileName= 'transcript_local_' + datetime.now().strftime("%Y-%m-%d_%H-%M") + '.txt'

    output_filepath = os.path.join(output_dir, output_fileName)
    savedTransactionFilePath = os.path.join(output_dir, savedTransactionFileName)

    local_llm='llama3.1'
   
    # QuickMeet Streamline
    stt_summary(
        audio_filepath,
        savedTransactionFilePath,
        local_llm,
        output_filepath
    )


if __name__ == "__main__":
    main()
