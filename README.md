# Music Player Application

![Music Player Screenshot](images/screenshot.png)

## Description
A modern music player application built with Python using CustomTkinter for the GUI and Pygame for audio playback. This player supports MP3 files, displays album art, and provides standard music player controls.

## Features
- Play, pause, stop, next, and previous track controls
- Volume control with mouse wheel support
- Playlist management (add/remove songs)
- Album art display
- Track progress slider
- Current and total time display
- Dark mode UI

## Requirements
- Python 3.7+
- Required packages (install via pip):
  ```
  pip install customtkinter CTkListbox pillow music-tag pygame
  ```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/music-player.git
   cd music-player
   ```
2. Create a `play_list` folder in the project directory for your music files
3. Place your MP3 files in the `play_list` folder
4. Run the application:
   ```
   python main.py
   ```

## Usage
1. **Adding Songs**: Click the "+" button to add MP3 files to your playlist
2. **Removing Songs**: Select a song and click the "-" button to remove it
3. **Playback Controls**:
   - Play/Pause: Middle button
   - Stop: Left button
   - Previous/Next: Outer buttons
4. **Volume Control**: Use the slider or mouse wheel to adjust volume
5. **Track Progress**: Drag the slider to seek through the current track

## File Structure
```
music-player/
├── main.py                # Main application file
├── play_list/             # Directory for music files
├── images/                # Directory for application images
│   ├── album.jpeg         # Default album art
│   ├── play.png           # Play button icon
│   ├── pause.png          # Pause button icon
│   ├── stop.png           # Stop button icon
│   ├── next.png           # Next button icon
│   ├── previous.png       # Previous button icon
│   ├── add_music.png      # Add music button icon
│   └── remove_music.png   # Remove music button icon
└── README.md              # This file
```

## Notes
- The application will automatically create a temporary image file (`new_image.jpg`) in the images folder to display album art
- Only MP3 files are supported
- The playlist is loaded from the `play_list` directory at startup

## License
This project is open source and available under the [MIT License](LICENSE).

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.