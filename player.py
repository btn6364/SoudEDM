# Importing Required Modules & libraries
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk 
import pygame
import os
import time
from mutagen.mp3 import MP3

#Import utils
from constants import *
from utils.Fisher_Yates_shuffle import Fisher_Yates_randomize

#Import Database
from database import Database

# Defining MusicPlayer Class
class MusicPlayer:

  # Defining Constructor
    def __init__(self,root):
        #The root container
        self.root = root

        # Title of the window
        self.root.title("SoundEDM")

        # Window Geometry
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        # Initiating Pygame
        pygame.init()

        # Initiating Pygame Mixer
        pygame.mixer.init()

        # Declaring track Variable
        self.track = StringVar()

        # Declaring Status Variable
        self.status = StringVar()

        #declare if the player is paused
        self.paused = False

        #declare the current audio
        self.audio = None

        #create menu
        self.createMenu()

        #draw track frame
        self.createTrackFrame()

        #draw a button frame
        self.createButtonFrame()

        #create playlist frame
        self.createPlaylistFrame()

        #create database connection
        self.database = Database()

        #create the playlist from the existing database
        self.createPlaylist()

    """
    Fetch the song playlist from the database. 
    """
    def createPlaylist(self):
        #Insert song title into play list 
        songs = self.database.getSongCollection()
        for id, song_title, song_dir in songs:
            self.playlist.insert(END, song_title)

    """
        Update the playlist. Erase everthing in the list box and create a new list. 
    """
    def updatePlaylist(self, song_titles):
        self.playlist.delete(0, END)
        for song_title in song_titles:
            self.playlist.insert(END, song_title)

    """
    Get the recent playlist using LRU Cache.
    """
    def recentPlaylist(self):
        pass

    """
    Create the action menu. 
    """
    def createMenu(self):
        #create the menu bar
        main_menu = Menu(self.root)
        self.root.config(menu=main_menu)
        action_menu = Menu(main_menu)
        main_menu.add_cascade(label="Action", menu=action_menu)
        action_menu.add_command(label="Add song", command=self.addSong)
        action_menu.add_command(label="Remove song", command=self.removeSong)

    """
    Create the track frame contains all the information about the current playing song. 
    """
    def createTrackFrame(self):
        # Creating Track Frame for Song label & status label
        trackframe = LabelFrame(self.root,text="Song Track",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
        trackframe.place(x=0,y=0,width=WINDOW_WIDTH * 0.6,height=WINDOW_HEIGHT * 0.5)
        # Inserting Song Track and Track Status label. 
        song_track = Label(trackframe,textvariable=self.track,width=20,font=("times new roman",24,"bold"),bg="grey",fg="gold")
        song_track.pack(fill=X, side=TOP)

        #create time slider
        self.time_slider = ttk.Scale(trackframe, from_=0, to=100, orient=HORIZONTAL, value=0)
        self.time_slider.pack(fill=X, side=TOP)

        #create time bar
        self.time_bar = Label(trackframe, text="", bd=1, relief=GROOVE, anchor=E)
        self.time_bar.pack(fill=X, side=BOTTOM, ipady=0.5)

    """
    Create the control panel. 
    """
    def createButtonFrame(self):
        # Creating Button Frame
        buttonframe = LabelFrame(self.root,text="Control Panel",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
        buttonframe.place(x=0,y=WINDOW_HEIGHT * 0.5,width=WINDOW_WIDTH * 0.6,height=WINDOW_HEIGHT * 0.5)
        #Insert Play, Pause, Unpause, Stop buttons
        play_button = Button(buttonframe,text="PLAY",command=self.playSong,width=4,height=1,font=("times new roman",14,"bold"),fg="navyblue",bg="gold").grid(row=0,column=0,padx=5,pady=5)
        pause_button = Button(buttonframe,text="PAUSE",command=self.pauseSong,width=5,height=1,font=("times new roman",14,"bold"),fg="navyblue",bg="gold").grid(row=0,column=1,padx=5,pady=5)
        stop_button = Button(buttonframe,text="STOP",command=self.stopSong,width=4,height=1,font=("times new roman",14,"bold"),fg="navyblue",bg="gold").grid(row=0,column=2,padx=5,pady=5)
        forward_button = Button(buttonframe,text="NEXT",command=self.nextSong,width=4,height=1,font=("times new roman",14,"bold"),fg="navyblue",bg="gold").grid(row=0,column=3,padx=5,pady=5)
        back_button = Button(buttonframe,text="PREV",command=self.prevSong,width=4,height=1,font=("times new roman",14,"bold"),fg="navyblue",bg="gold").grid(row=0,column=4,padx=5,pady=5)
        shuffle_button = Button(buttonframe,text="SHUFFLE",command=self.shuffleSong,width=7,height=1,font=("times new roman",14,"bold"),fg="navyblue",bg="gold").grid(row=0,column=5,padx=5,pady=5)
        recent_played = Button(buttonframe,text="RECENT PLAYED",command=self.recentPlaylist,width=10,height=1,font=("times new roman",12,"bold"),fg="navyblue",bg="gold").grid(row=0,column=6,padx=5,pady=5)

    """
    Create the playlist frame containing all songs. 
    """
    def createPlaylistFrame(self):
        # Creating Playlist Frame
        songsframe = LabelFrame(self.root,text="Song Playlist",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
        songsframe.place(x=WINDOW_WIDTH * 0.6,y=0,width=WINDOW_WIDTH * 0.4,height=WINDOW_HEIGHT)
        # Inserting scrollbar + listbox
        scrol_y = Scrollbar(songsframe,orient=VERTICAL)
        self.playlist = Listbox(songsframe,yscrollcommand=scrol_y.set,selectbackground="gold",selectmode=SINGLE,font=("times new roman",12,"bold"),bg="silver",fg="navyblue",bd=5,relief=GROOVE, height=WINDOW_HEIGHT//20)
        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT,fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)


    """
    Add a song to the playlist. 
    """
    def addSong(self):
        song_dir = filedialog.askopenfilename(initialdir="songs", title="Choose a song", filetypes=[("mp3 files", "*.mp3")])
        if song_dir:
            #trimp the directory and file extension to get the song_title
            start = len(song_dir) - 1
            while song_dir[start-1] != '/':
                start -= 1
            song_title = song_dir[start:len(song_dir)-4]

            #load the audio's directory
            song = (song_title, song_dir)
            self.database.addSong(song)
            self.playlist.insert(END, song_title)

    """
    Remove a song from the playlist. 
    """
    def removeSong(self):
        song_title = self.playlist.get(ACTIVE)
        cur_song_idx = self.playlist.curselection()[0]
        if cur_song_idx >= 0:
            #stop the song before remove it from the database
            self.stopSong()
            self.database.removeSong(song_title)
            self.playlist.delete(cur_song_idx)

    """
    Play the selected song
    """
    def playSong(self):
        song_title = self.playlist.get(ACTIVE)
        self.track.set(song_title)
        self.status.set(" - Playing")
        # Load the audio 
        self.audio = self.database.getSong(song_title)[2]
        pygame.mixer.music.load(self.audio)
        # Playing Selected Song
        pygame.mixer.music.play()
        #Get playtime info
        self.songPlaytime()
      
    """
    Stop the current playing song. 
    """
    def stopSong(self):
        self.status.set(" - Stopped")
        pygame.mixer.music.stop()
        #clear the time bar and selection bar
        self.playlist.selection_clear(ACTIVE)
        self.time_bar.config(text="")
        self.time_slider.config(value=0)

    """
    Pause and unpause song
    """
    def pauseSong(self):
        if self.paused:
            self.status.set(" - Playing")
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            self.status.set("- Paused")
            pygame.mixer.music.pause()
            self.paused = True
       
    """
    Play the next song. Stop if the current song is the last one. 
    """
    def nextSong(self):
        cur_song_indices = self.playlist.curselection()
        cur_song_idx = cur_song_indices[0] + 1
        if cur_song_idx < self.playlist.size():
            self.playlist.selection_clear(cur_song_indices)
            self.playlist.select_set(cur_song_idx)
            self.playlist.activate(cur_song_idx)
            self.playSong()

    """
    Play the previous song. Stop if the current song is the first one. 
    """
    def prevSong(self):
        cur_song_indices = self.playlist.curselection()
        cur_song_idx = cur_song_indices[0] - 1
        if cur_song_idx >= 0:
            self.playlist.selection_clear(cur_song_indices)
            self.playlist.select_set(cur_song_idx)
            self.playlist.activate(cur_song_idx)
            self.playSong()

    """
    Shuffle playlist using Fisher_Yates algorithm. 
    """
    def shuffleSong(self):
        #Get an array of songs and shuffle
        songs = self.database.getSongCollection()
        song_titles = []
        for id, song_title, audio in songs:
            song_titles.append(song_title)
        song_titles = Fisher_Yates_randomize(song_titles)
        #update the playlist
        self.updatePlaylist(song_titles)
        

    """
        Keep track of the song playing time and duration. 
    """
    def songPlaytime(self):
        cur_time = pygame.mixer.music.get_pos() / 1000
        converted_time = time.strftime("%M:%S", time.gmtime(cur_time))
        cur_song_indices = self.playlist.curselection()
        if cur_song_indices:
            #load song's length with Mutagen
            mutagen_mp3 = MP3(self.audio)
            song_length = mutagen_mp3.info.length
            converted_song_length = time.strftime("%M:%S", time.gmtime(song_length))
            #output to time bar
            self.time_slider.config(value=cur_time, to=song_length)
            self.time_bar.config(text=f"Time elapsed: {converted_time} of {converted_song_length}")
            self.time_bar.after(1000, self.songPlaytime)

"""
    Execute the music player. 
"""
if __name__ == "__main__":
    # Creating TK Container
    root = Tk()
    # Passing Root to MusicPlayer Class
    MusicPlayer(root)
    # Root Window Looping
    root.mainloop()