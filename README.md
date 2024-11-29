# Trivia Video Generator (Source Code)

<p align="center">
  <img src="https://raw.githubusercontent.com/itsaqibdev/Trivia-Video-Generator-Bot/main/ico.ico" alt="App Icon" width="128" height="128">
</p>

A Python application that automatically generates engaging "Did You Know?" trivia videos perfect for YouTube Shorts. This repository contains the source code for developers who want to run or modify the application.

## Screenshots

<div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
  <div style="flex: 1; margin-right: 10px;">
    <img src="https://raw.githubusercontent.com/itsaqibdev/Trivia-Video-Generator-Bot/main/1.PNG" alt="Home Tab" width="400">
    <p align="center"><em>Home Tab - Select category and generate videos</em></p>
  </div>
  <div style="flex: 1; margin-left: 10px;">
    <img src="https://raw.githubusercontent.com/itsaqibdev/Trivia-Video-Generator-Bot/main/2.PNG" alt="About Tab" width="400">
    <p align="center"><em>About Tab - Developer information</em></p>
  </div>
</div>

## Demo Video

<video width="100%" controls>
  <source src="https://raw.githubusercontent.com/itsaqibdev/Trivia-Video-Generator-Bot/main/trivia_video_20241128_202547.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

[📥 Download Demo Video](https://raw.githubusercontent.com/itsaqibdev/Trivia-Video-Generator-Bot/main/trivia_video_20241128_202547.mp4)

## Prerequisites

- Python 3.11.9 or later
- pip (Python package installer)
- Windows OS (for running the GUI version)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/itsaqibdev/Trivia-Video-Generator-Bot.git
cd Trivia-Video-Generator-Bot
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Run the GUI version:
```bash
python trivia_gui.py
```

2. Or import the video generator in your own code:
```python
from trivia_shorts_generator import generate_video

# Generate a video with custom parameters
generate_video(category="9", num_questions=3)
```

## Project Structure

- `trivia_gui.py`: Main GUI application using tkinter
- `trivia_shorts_generator.py`: Core video generation logic
- `requirements.txt`: List of Python dependencies
- `think.gif`: Loading animation asset
- `ico.ico`: Application icon

## Features

- 🎥 Creates YouTube Shorts-ready videos (1080x1920)
- 📚 Multiple trivia categories to choose from
- 🎯 Customizable number of questions
- ⏱️ Progress tracking while generating
- 🎨 Professional animations and transitions
- 💾 Automatic video saving with timestamps
- 🌙 Modern dark theme interface

## Dependencies

Main packages used:
- `moviepy`: Video creation and editing
- `Pillow`: Image processing
- `requests`: API calls
- `tkinter`: GUI framework
- `numpy`: Numerical computations
- `pygame`: Required by moviepy for audio

## Development

To modify the video generation:
1. Edit `trivia_shorts_generator.py` for video logic
2. Edit `trivia_gui.py` for UI changes
3. Test changes by running the GUI

## Building Executable (Optional)

To create a standalone executable:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller trivia_app.spec
```

The executable will be created in the `dist` folder.

## API Used

This project uses the [Open Trivia Database](https://opentdb.com/) API for fetching trivia questions.

## Support

Need help? Found a bug? Have a suggestion? Contact the developer through the social links in the About tab of the application.

## Credits

- Trivia questions provided by [Open Trivia Database](https://opentdb.com/)
- Application developed by Muhammad Saqib
- Icon and animations created by Muhammad Saqib
