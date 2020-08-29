# Importing Required Modules & libraries
from tkinter import *
import pygame
import os
from constants import *


# Defining MusicPlayer Class
class MusicPlayer:

  # Defining Constructor
    def __init__(self,root):
        self.root = root
        # Title of the window
        self.root.title("SoundEDM")
        # Window Geometry
        self.root.geometry("1000x400")
        # Initiating Pygame
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        # Declaring track Variable
        self.track = StringVar()
        # Declaring Status Variable
        self.status = StringVar()
        #draw track frame
        self.createTrackFrame()

        #draw a button frame
        self.createButtonFrame()

        #create playlist frame
        self.createPlaylistFrame()
       
        # Changing Directory for fetching Songs
        os.chdir("/home/baonguyen/Projects/python/pygame/MusicPlayer/songs")

        # Fetching Songs
        songtracks = os.listdir()
        # Inserting Songs into Playlist
        for track in songtracks:
            self.playlist.insert(END,track)


    def createTrackFrame(self):
        # Creating Track Frame for Song label & status label
        trackframe = LabelFrame(self.root,text="Song Track",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
        trackframe.place(x=0,y=0,width=WINDOW_WIDTH * 0.6,height=WINDOW_HEIGHT * 0.5)
        # Inserting Song Track and Track Status label. 
        songtrack = Label(trackframe,textvariable=self.track,width=20,font=("times new roman",24,"bold"),bg="grey",fg="gold").grid(row=0,column=0,padx=10,pady=5)
        trackstatus = Label(trackframe,textvariable=self.status,font=("times new roman",24,"bold"),bg="grey",fg="gold").grid(row=0,column=1,padx=10,pady=5)

    def createButtonFrame(self):
        # Creating Button Frame
        buttonframe = LabelFrame(self.root,text="Control Panel",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
        buttonframe.place(x=0,y=WINDOW_HEIGHT * 0.5,width=WINDOW_WIDTH * 0.6,height=WINDOW_HEIGHT * 0.5)
        #Insert Play, Pause, Unpause, Stop buttons
        playbtn = Button(buttonframe,text="PLAY",command=self.playSong,width=6,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=0,column=0,padx=10,pady=5)
        playbtn = Button(buttonframe,text="PAUSE",command=self.pauseSong,width=8,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=0,column=1,padx=10,pady=5)
        playbtn = Button(buttonframe,text="UNPAUSE",command=self.unpauseSong,width=10,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=0,column=2,padx=10,pady=5)
        playbtn = Button(buttonframe,text="STOP",command=self.stopSong,width=6,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=0,column=3,padx=10,pady=5)
        playbtn = Button(buttonframe,text="NEXT",command=self.nextSong,width=6,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=1,column=0,padx=10,pady=5)
        playbtn = Button(buttonframe,text="PREV",command=self.prevSong,width=6,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=1,column=1,padx=10,pady=5)

    def createPlaylistFrame(self):
        # Creating Playlist Frame
        songsframe = LabelFrame(self.root,text="Song Playlist",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
        songsframe.place(x=WINDOW_WIDTH * 0.6,y=0,width=WINDOW_WIDTH * 0.4,height=WINDOW_HEIGHT)
        # Inserting scrollbar + listbox
        scrol_y = Scrollbar(songsframe,orient=VERTICAL)
        self.playlist = Listbox(songsframe,yscrollcommand=scrol_y.set,selectbackground="gold",selectmode=SINGLE,font=("times new roman",12,"bold"),bg="silver",fg="navyblue",bd=5,relief=GROOVE, height=WINDOW_HEIGHT // 20)
        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT,fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)


    # Defining Play Song Function
    def playSong(self):
        # Displaying Selected Song title
        self.track.set(self.playlist.get(ACTIVE))
        # Displaying Status
        self.status.set("-Playing")
        # Loading Selected Song
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        # Playing Selected Song
        pygame.mixer.music.play()

    def stopSong(self):
        # Displaying Status
        self.status.set("-Stopped")
        # Stopped Song
        pygame.mixer.music.stop()

    def pauseSong(self):
        # Displaying Status
        self.status.set("-Paused")
        # Paused Song
        pygame.mixer.music.pause()

    def unpauseSong(self):
        # Displaying Status
        self.status.set("-Playing")
        # Playing back Song
        pygame.mixer.music.unpause()

    def nextSong(self):
        cur_song_indices = self.playlist.curselection()
        cur_song_idx = cur_song_indices[0] + 1
        if cur_song_idx < self.playlist.size():
            self.playlist.selection_clear(cur_song_indices)
            self.playlist.select_set(cur_song_idx)
            self.playlist.activate(cur_song_idx)
            self.playSong()

    def prevSong(self):
        cur_song_indices = self.playlist.curselection()
        cur_song_idx = cur_song_indices[0] - 1
        if cur_song_idx >= 0:
            self.playlist.selection_clear(cur_song_indices)
            self.playlist.select_set(cur_song_idx)
            self.playlist.activate(cur_song_idx)
            self.playSong()

if __name__ == "__main__":
    # Creating TK Container
    root = Tk()
    # Passing Root to MusicPlayer Class
    MusicPlayer(root)
    # Root Window Looping
    root.mainloop()