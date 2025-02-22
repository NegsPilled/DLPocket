# DLPocket

**DLPocket** is a sleek, user-friendly YouTube downloader built with Python and PyQt5. It allows you to download videos and audio from YouTube in various qualities, including up to the highest available resolution and 60 FPS when supported. Featuring a custom dark-themed interface, DLPocket combines functionality with a modern aesthetic.

Started as a personal project, I adapted to share with friends, and the open-source community.

## Features
- Download YouTube videos in resolutions from 240p to 4K (or higher, if available).
- Supports 60 FPS for videos that offer it.
- Extract audio as MP3 (192 kbps).
- Custom title bar with a minimalist, dark design.
- Choose your download folder and manage multiple URLs at once.
- Outputs video files as `.mkv` for broad codec compatibility.

## Screenshot
*`![DLPocket Screenshot](screenshot.png)`)*

## Installation
### Prerequisites
- **Python 3.8+**: Required if running from source.
- **Dependencies**: Installed via `pip` (see below).
- **FFmpeg**: Automatically bundled in the executable release; otherwise, install manually for source usage (see instructions below).

### Option 1: Download the Executable (Windows)
1. Go to the [Releases](https://github.com/[YourUsername]/DLPocket/releases) page.
2. Download the latest `DLPocket.exe`.
3. Run the executable—no additional setup needed! FFmpeg and all dependencies are included.

### Option 2: Run from Source
1. Clone this repository:
   ```bash
   git clone https://github.com/[YourUsername]/DLPocket.git
   cd DLPocket
2. Install dependencies:
   ```bash
   pip install yt-dlp PyQt5
3. Install FFmpeg:
   - Windows: Download from [FFmpeg’s official site](https://ffmpeg.org/) and add it to your PATH (e.g., `C:/ffmpeg/bin)`.
   - Linux/macOS: Install via package manager (e.g., `sudo apt install ffmpeg` or `brew install ffmpeg`).
4. Run the app:
   ```bash
   python dlpocket.py

## Useage
1. Launch DLPocket.
2. Enter a YouTube URL in the "Enter Video URL" field.
3. Select a quality option (e.g., "Best Quality" for highest resolution and FPS, or "Audio Only (MP3)").
4. Click "Add URL" to queue it.
5. (Optional) Add more URLs or select a custom download folder with "Select Download Folder".
6. Click "Start Download" to begin.
7. Check your download folder for `.mkv` video files or `.mp3` audio files.

## Building the Executable
To create your own `.exe` (e.g., for testing or custom releases):
```bash
pip install pyinstaller
pyinstaller --add-binary "path/to/ffmpeg.exe;." --add-binary "path/to/ffprobe.exe;." -F dlpocket.py
```
- Replace `path/to/ffmpeg.exe` with the actual path to your FFmpeg binaries.
- The `-F` flag creates a single-file executable.

## License
DLPocket is licensed under the **GNU General Public License v3.0** (GPL v3). See the LICENSE file for details.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

## Dependencies Licensing
- **yt_dlp**: Unlicense (public domain).
- **PyQt5**: GNU GPL v3 (or commercial license; GPL applies here).
- **FFmpeg**: LGPL v2.1 (or GPL if compiled with certain features).

As required by GPL v3, the source code is provided in this repository. If you distribute DLPocket binaries, you must also provide the source code.

## Contact
Have questions or suggestions? Open an issue here on GitHub, or email at NegsPillled@proton.me




