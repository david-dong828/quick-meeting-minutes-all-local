# QuickMeetingMinutes - A Local Automated Meeting Minutes Generator Running on CPU

QuickMeetingMinutes is a Python application that automatically generates meeting minutes from audio recordings. It transcribes audio files using Whisper and then summarizes the content using Llama 3.1 to produce structured meeting minutes with summaries, key points, and action items. **All processing is done Locally**, without any need for an internet connection, and can be run on any Windows with **CPU**.

## Features

- Record audio directly through a simple GUI interface
- Process existing audio files
- Transcribe speech to text using OpenAI's Whisper model (locally)
- Generate structured meeting minutes using Llama 3.1 (via Ollama)
- Save transcripts and meeting minutes as text files

## Prerequisites

- Python 3.10+
- Ollama with Llama 3.1 model installed
- Local installation of OpenAI Whisper

## Installation

1. Clone the repository:

```bash
git clone https://github.com/david-dong828/quick-meeting-minutes-all-local.git
cd quick-meeting-minutes-all-local
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Make sure you have Ollama installed with the Llama 3.1 model:
```bash
ollama pull llama3.1
```

## Usage

### Recording a new meeting

```bash
cd src
python main.py --record
```

This will open a GUI where you can record your meeting audio.

### Processing an existing audio file

```bash
python src/main.py --audio_filepath /path/to/your/audio/file.wav
```

### Output

The application generates one audio file in the `audios` directory and two files in the `files` directory:
- A transcript file (`transcript_local_YYYY-MM-DD_HH-MM.txt`)
- A markdown file with meeting minutes (`Meeting Minutes_YYYY-MM-DD_HH-MM.md`)

## Project Structure

- `src/main.py`: Main application entry point
- `src/utils/file_processor.py`: Handles audio transcription and file operations
- `src/utils/record_gui.py`: GUI for recording audio
- `src/models/llama3.py`: Interface to the Llama 3.1 model via Ollama

## License

[MIT](LICENSE)

