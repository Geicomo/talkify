import os
import sys
import logging
from tkinter import *
import pyttsx3
import speech_recognition as sr
import socket
from fuzzywuzzy import fuzz
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import threading
import pygame
import configparser

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Read configuration settings
config = configparser.ConfigParser()
config_path = resource_path('config.ini')
config.read(config_path)
ACTIVATE_PHRASE = config.get('Settings', 'ActivatePhrase', fallback='Yo Spotify')

def listen_continuously():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        logging.debug("Microphone adjusted for ambient noise")
        while microphone_active:
            try:
                logging.debug("Listening for audio...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                text = recognizer.recognize_google(audio)
                logging.debug(f"Recognized: {text}")
                update_text(f"Recognized: {text}")

                # Check if the text starts with the activate phrase
                similarity_threshold = 70  # You can adjust this threshold
                if fuzz.ratio(text.lower().strip(), ACTIVATE_PHRASE.lower()) > similarity_threshold:
                    update_text(f"Command received: {text}")
                    listen_for_command(recognizer, source)
            except sr.WaitTimeoutError:
                update_text("Listening timed out, no phrase detected.")
                logging.warning("Listening timed out, no phrase detected.")
            except sr.UnknownValueError:
                update_text("Could not understand audio.")
                logging.warning("Could not understand audio.")
            except sr.RequestError as e_request:
                update_text(f"Could not request results; {e_request}")
                logging.error(f"Could not request results; {e_request}")
            except Exception as ex:
                update_text(f"An error occurred: {ex}")
                logging.error(f"An error occurred: {ex}")

def listen_for_command(recognizer, source):
    logging.debug("Listening for command...")
    pygame.mixer.init()
    pygame.mixer.music.load(resource_path('Audio/listening.wav'))
    pygame.mixer.music.play()
    try:
        audio = recognizer.listen(source, timeout=15, phrase_time_limit=15)
        command = recognizer.recognize_google(audio).lower()
        logging.debug(f"Command: {command}")
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
        elif 'skip' in command or 'next' in command:
            update_text("Skipping to next track...")
            skip_track()
        elif 'back' in command or 'previous' in command:
            update_text("Going back to the previous track...")
            previous_track()
        else:
            update_text("Unknown command.")
            logging.warning(f"Unknown command: {command}")
    except sr.WaitTimeoutError:
        update_text("Listening timed out, no command detected.")
        logging.warning("Listening timed out, no command detected.")
    except sr.UnknownValueError:
        update_text("Could not understand command.")
        logging.warning("Could not understand command.")
    except sr.RequestError as e_request:
        update_text(f"Could not request results; {e_request}")
        logging.error(f"Could not request results; {e_request}")
    except Exception as ex:
        update_text(f"An error occurred while processing the command: {ex}")
        logging.error(f"An error occurred while processing the command: {ex}")

def play_music():
    logging.debug("Attempting to play music...")
    pygame.mixer.init()
    pygame.mixer.music.load(resource_path('Audio/heard.wav'))
    pygame.mixer.music.play()
    try:
        devices = sp.devices()
        if devices['devices']:
            device_id = devices['devices'][0]['id']
            sp.transfer_playback(device_id, force_play=True)
        else:
            update_text("No active Spotify device found.")
            logging.warning("No active Spotify device found.")
    except spotipy.exceptions.SpotifyException as e:
        update_text(f"Error: {e}")
        logging.error(f"SpotifyException: {e}")

def pause_music():
    logging.debug("Attempting to pause music...")
    pygame.mixer.init()
    pygame.mixer.music.load(resource_path('Audio/heard.wav'))
    pygame.mixer.music.play()
    try:
        sp.pause_playback()
    except spotipy.exceptions.SpotifyException as e:
        update_text(f"Error: {e}")
        logging.error(f"SpotifyException: {e}")

def skip_track():
    logging.debug("Attempting to skip track...")
    pygame.mixer.init()
    pygame.mixer.music.load(resource_path('Audio/heard.wav'))
    pygame.mixer.music.play()
    try:
        sp.next_track()
    except spotipy.exceptions.SpotifyException as e:
        update_text(f"Error: {e}")
        logging.error(f"SpotifyException: {e}")

def previous_track():
    logging.debug("Attempting to go to previous track...")
    pygame.mixer.init()
    pygame.mixer.music.load(resource_path('Audio/heard.wav'))
    pygame.mixer.music.play()
    try:
        sp.previous_track()
    except spotipy.exceptions.SpotifyException as e:
        update_text(f"Error: {e}")
        logging.error(f"SpotifyException: {e}")

def play_playlist(playlist_name):
    logging.debug(f"Attempting to play playlist: {playlist_name}")
    pygame.mixer.init()
    pygame.mixer.music.load(resource_path('Audio/heard.wav'))
    pygame.mixer.music.play()
    try:
        user_playlists = sp.current_user_playlists(limit=50)
        user_playlist_uri = None
        for playlist in user_playlists['items']:
            if fuzz.ratio(playlist_name.lower(), playlist['name'].lower()) > 50:
                user_playlist_uri = playlist['uri']
                update_text(f"Found in your playlists: {playlist['name']}")
                break

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
                logging.warning(f"No playlist found with name: {playlist_name}")
    except spotipy.exceptions.SpotifyException as e:
        update_text(f"Error: {e}")
        logging.error(f"SpotifyException: {e}")

def update_text(message):
    logging.info(message)
    t.after(0, e.insert, END, message + "\n")
    t.after(0, e.see, END)  # Scroll to the end

def start_listening():
    global microphone_active, listening_thread
    microphone_active = True
    activate_button.config(state=DISABLED)
    deactivate_button.config(state=NORMAL)
    logging.debug("Starting listening thread...")
    listening_thread = threading.Thread(target=listen_continuously)
    listening_thread.daemon = True
    listening_thread.start()

def stop_listening():
    global microphone_active
    microphone_active = False
    activate_button.config(state=NORMAL)
    deactivate_button.config(state=DISABLED)
    logging.debug("Stopped listening.")

def write_text():
    if socket.gethostbyname(socket.gethostname()) == "127.0.0.1":
        update_text("Your device is not connected to the internet")
    else:
        e.delete(1.0, END)  # Clear the text box before starting
        start_listening()

# Colors and styling
BACKGROUND_COLOR = "#5c5c5c"
TEXT_COLOR = "#FFFFFF"
FONT = ("Helvetica", 12)
BUTTON_COLOR = "#1DB954"
BUTTON_HOVER_COLOR = "#14833b"
BUTTON_ACTIVE_COLOR = "#1ED760"

t = Tk()
t.geometry("400x300")
t.title("Talkify")

# Apply styles
t.configure(bg=BUTTON_COLOR)
activate_button = Button(text="Activate Microphone", command=write_text,
                         bg=BUTTON_COLOR, font=FONT, relief=FLAT, activebackground=BUTTON_ACTIVE_COLOR)
activate_button.place(x=45, y=200, width=145, height=40)
deactivate_button = Button(text="Deactivate Microphone", command=stop_listening, state=DISABLED,
                           bg=BUTTON_COLOR, font=FONT, relief=FLAT, activebackground=BUTTON_ACTIVE_COLOR)
deactivate_button.place(x=210, y=200, width=160, height=40)

e = Text(bd=0, height=10, width=40, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=10, relief=FLAT)
e.place(x=20, y=20)

t.mainloop()
