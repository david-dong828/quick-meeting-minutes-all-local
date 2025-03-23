import logging
import sys
from ollama import chat



def generate_outputs_ollama(audio_filepath, prompt,local_llm):
    try:
        response = chat(
            model=local_llm,
            messages=prompt
        )
        return response['message']['content']
    except Exception as e:
        logging.error(msg=f"generate_outputs: Cannot generate summary, keynotes and list of action items from audio '{audio_filepath}'. Error message: {e}")
        sys.exit(1) 