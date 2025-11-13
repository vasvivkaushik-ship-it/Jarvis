import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import openai
import os
from gtts import gTTS
import pygame
import time

# ---------------- CONFIGURATION ----------------
#openai.api_key = "your_openai_api_key_here"   # replace with your OpenAI key
NEWS_API_KEY = "your_newsapi_key_here"        # replace with your NewsAPI key
WAKE_WORD = "jarvis"

# ---------------- TEXT TO SPEECH ----------------
engine = pyttsx3.init()

def speak(text):
    print(f"[Jarvis speaking -> pyttsx3]: {text}")
    engine.say(text)
    engine.runAndWait()

def speak_gtts(text):
    print(f"[Jarvis speaking -> gTTS]: {text}")
    try:
        tts = gTTS(text=text, lang="en")
        filename = "temp.mp3"
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.3)
        pygame.mixer.quit()
        os.remove(filename)
    except Exception as e:
        print("[Background recognizer request error]:", e)

# ---------------- FEATURES ----------------
def open_website(site):
    urls = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "linkedin": "https://www.linkedin.com"
    }
    if site in urls:
        speak(f"Opening {site}")
        webbrowser.open(urls[site])
    else:
        speak("Website not found.")

def play_music():
    speak("Playing music from your library.")
    webbrowser.open("https://open.spotify.com")  # change to your favorite link

def fetch_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    try:
        news = requests.get(url).json()
        articles = news.get("articles", [])[:5]
        speak("Here are the top news headlines.")
        for i, article in enumerate(articles, start=1):
            speak(f"Headline {i}: {article.get('title')}")
    except Exception as e:
        speak("Sorry, I was unable to fetch the news.")
        print("[NewsAPI error]:", e)

def chat_with_openai(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}]
        )
        answer = response.choices[0].message["content"]
        speak(answer)
    except Exception as e:
        speak("Sorry, I couldn't process that request.")
        print("[OpenAI error]:", e)

# ---------------- COMMAND HANDLING ----------------
def process_command(command):
    command = command.lower()

    if "open" in command:
        if "google" in command:
            open_website("google")
        elif "youtube" in command:
            open_website("youtube")
        elif "facebook" in command:
            open_website("facebook")
        elif "linkedin" in command:
            open_website("linkedin")
        else:
            speak("I don't know that website.")
    
    elif "music" in command:
        play_music()

    elif "news" in command:
        fetch_news()

    elif "exit" in command or "quit" in command:
        speak("Goodbye.")
        os._exit(0)
    
    else:
        chat_with_openai(command)

# ---------------- LISTENING FUNCTIONS ----------------
recognizer = sr.Recognizer()

def listen_for_command():
    with sr.Microphone() as source:
        print("[Jarvis]: Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"[Command recognized]: {command}")
        process_command(command)
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Network error while processing your request.")

# ---------------- BACKGROUND ACTIVATION ----------------
def activated_callback(recognizer, audio):
    """Detects wake word 'Jarvis' and triggers active listening."""
    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"[Background recognition]: {text}")

        if WAKE_WORD in text.split():
            speak("Ya.")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.4)
                speak("I'm listening.")
                audio2 = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            try:
                command = recognizer.recognize_google(audio2)
                print(f"[Command recognized]: {command}")
                process_command(command)
            except sr.WaitTimeoutError:
                speak("I didn't hear anything.")
            except sr.UnknownValueError:
                speak("Sorry, I couldn't understand that.")
            except sr.RequestError as e:
                print("[Background recognizer request error]:", e)

    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print("[Main recognizer request error]:", e)

# ---------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    print("[System]: Starting Jarvis...")
    speak("Initializing Jarvis....")
    speak("Jarvis is ready. Say 'Jarvis' to wake me up.")
    
    mic = sr.Microphone()
    stop_listening = recognizer.listen_in_background(mic, activated_callback)
    print("[System]: Listening in background. Say 'Jarvis' to activate.")

    # Keep running forever
    while True:
        time.sleep(0.5)


