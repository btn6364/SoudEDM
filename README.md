# SoundEDM

A Desktop Music Player application.

## Supported features. 

1. Add and remove songs to and from playlist. 
2. Play/Pause/Unpause/Stop songs in the playlist.
3. Move forward and backward between songs in the playlist. 
4. Shuffle songs in the playlist using Fisher_Yates shuffle algorithm. 
5. Time slider allows users to see song's duration.  
6. Read and record songs in the SQLite database. 

## Usage

Create and activate a virtual environment in the project. 

```
python3 -m venv venv
source venv/bin/activate
```

Installed all the requirement packages. 

```
sudo apt-get install python3-tk
pip3 install pygame
pip3 install mutagen
```

Navigate to the project. Run the application.

```
cd MusicPlayer
python3 player.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)