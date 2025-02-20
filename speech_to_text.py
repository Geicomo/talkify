from tkinter import *
import pyttsx3
import speech_recognition as sr
import os
import socket
from fuzzywuzzy import fuzz
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import threading
import pygame  # Import the pygame library

# Spotify API setup with cached token
SPOTIPY_CLIENT_ID = '141ac1cdc293449f93c854636e1619e1'
SPOTIPY_CLIENT_SECRET = 'dccd1190076045918165792c6f82efef'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-modify-playback-state user-read-playback-state',
                                               cache_path='token_cache'))

microphone_active = False
listening_thread = None

def listen_continuously():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while microphone_active:
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
                text = recognizer.recognize_google(audio)
                update_text(f"Recognized: {text}")

                # Check if the text starts with a phrase close to "Hey Spotify"
                trigger_phrase = "Yo Spotify"
                similarity_threshold = 70  # You can adjust this threshold
                if fuzz.ratio(text.lower().strip(), trigger_phrase.lower()) > similarity_threshold:
                    update_text(f"Command received: {text}")
                    listen_for_command(recognizer, source)
            except sr.UnknownValueError:
                update_text("Could not understand audio.")
            except sr.RequestError as e_request:
                update_text(f"Could not request results; {e_request}")
            except Exception as ex:
                print(f"An error occurred: {ex}")

def listen_for_command(recognizer, source):
    pygame.mixer.init()  # Initialize Pygame Mixer
    pygame.mixer.music.load('Audio/listening.wav')  # Load the sound
    pygame.mixer.music.play()  # Play the sound
    try:
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        command = recognizer.recognize_google(audio).lower()
        update_text(f"Command: {command}")

        if 'play' in command:
            if 'playlist' in command:
                playlist_name = command.split('playlist', 1)[1].strip()
                update_text(f"Playing playlist: {playlist_name}")
                play_playlist(playlist_name)
            else:
                update_text("Playing music on Spotify...")
                play_music()
        elif 'pause' in command or 'stop' in command:
            update_text("Pausing music on Spotify...")
            pause_music()
        elif 'skip' in command:
            update_text("Skipping to next track...")
            skip_track()
        elif 'back' in command or 'previous' in command:
            update_text("Going back to the previous track...")
            previous_track()
        else:
            update_text("Unknown command.")
    except sr.WaitTimeoutError:
        update_text("Listening timed out, no command detected.")
    except sr.UnknownValueError:
        update_text("Could not understand command.")
    except sr.RequestError as e_request:
        update_text(f"Could not request results; {e_request}")
    except Exception as ex:
        update_text(f"An error occurred while processing the command: {ex}")

def play_music():
    pygame.mixer.init()  # Initialize Pygame Mixer
    pygame.mixer.music.load('Audio/heard.wav')  # Load the sound
    pygame.mixer.music.play()  # Play the sound
    try:
        devices = sp.devices()
        if devices['devices']:
            device_id = devices['devices'][0]['id']
            sp.transfer_playback(device_id, force_play=True)
        else:
            update_text("No active Spotify device found.")
    except spotipy.exceptions.SpotifyException as e:
        update_text(f"Error: {e}")

def pause_music():
    pygame.mixer.init()  # Initialize Pygame Mixer
    pygame.mixer.music.load('Audio/heard.wav')  # Load the sound
    pygame.mixer.music.play()  # Play the sound
    try:
        sp.pause_playback()
    except spotipy.exceptions.SpotifyException as e:
        update_text(f"Error: {e}")

def skip_track():
    pygame.mixer.init()  # Initialize Pygame Mixer
    pygame.mixer.music.load('Audio/heard.wav')  # Load the sound
    pygame.mixer.music.play()  # Play the sound
    try:
        sp.next_track()
    except spotipy.exceptions.SpotifyException as e:
        update_text(f"Error: {e}")

def previous_track():
    pygame.mixer.init()  # Initialize Pygame Mixer
    pygame.mixer.music.load('Audio/heard.wav')  # Load the sound
    pygame.mixer.music.play()  # Play the sound
    try:
        sp.previous_track()
    except spotipy.exceptions.SpotifyException as e:
        update_text(f"Error: {e}")

def play_playlist(playlist_name):
    pygame.mixer.init()  # Initialize Pygame Mixer
    pygame.mixer.music.load('Audio/heard.wav')  # Load the sound
    pygame.mixer.music.play()  # Play the sound
    try:
        # First, search through the user's playlists
        user_playlists = sp.current_user_playlists(limit=50)
        user_playlist_uri = None
        for playlist in user_playlists['items']:
            if fuzz.ratio(playlist_name.lower(), playlist['name'].lower()) > 50:
                user_playlist_uri = playlist['uri']
                update_text(f"Found in your playlists: {playlist['name']}")
                break

        # If not found in user's playlists, search public playlists
        if user_playlist_uri:
            sp.start_playback(context_uri=user_playlist_uri)
        else:
            results = sp.search(q=f'playlist:{playlist_name}', type='playlist', limit=1)
            playlists = results.get('playlists', {}).get('items', [])
            if playlists:
                playlist_uri = playlists[0]['uri']
                sp.start_playback(context_uri=playlist_uri)
                update_text(f"Started playing public playlist: {playlists[0]['name']}")
            else:
                update_text(f"No playlist found with name: {playlist_name}")
    except spotipy.exceptions.SpotifyException as e:
        update_text(f"Error: {e}")

def update_text(message):
    t.after(0, e.insert, END, message + "\n")
    t.after(0, e.see, END)  # Scroll to the end

def start_listening():
    global microphone_active, listening_thread
    microphone_active = True
    activate_button.config(state=DISABLED)
    deactivate_button.config(state=NORMAL)
    listening_thread = threading.Thread(target=listen_continuously)
    listening_thread.daemon = True
    listening_thread.start()

def stop_listening():
    global microphone_active
    microphone_active = False
    activate_button.config(state=NORMAL)
    deactivate_button.config(state=DISABLED)

def write_text():
    if socket.gethostbyname(socket.gethostname()) == "127.0.0.1":
        msg.showerror("App", "Your device is not connected to the internet")
    else:
        e.delete(1.0, END)  # Clear the text box before starting
        start_listening()

t = Tk()
t.geometry("400x300")
t.title("Talkify")

activate_button = Button(text="Activate Microphone", command=write_text)
activate_button.place(x=50, y=170)
deactivate_button = Button(text="Deactivate Microphone", command=stop_listening, state=DISABLED)
deactivate_button.place(x=200, y=170)

e = Text(bd=4, height=8, width=42)
e.place(x=20, y=10)

t.mainloop()
