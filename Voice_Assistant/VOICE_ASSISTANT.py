import tkinter as tk
from tkinter import messagebox, scrolledtext
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import os

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen_command():
    """Listen for a voice command and return it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        output_text.insert(tk.END, "Listening...\n")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            output_text.insert(tk.END, f"Command: {command}\n")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
            output_text.insert(tk.END, "Sorry, I didn't catch that. Could you repeat?\n")
            return ""
        except sr.RequestError:
            speak("Sorry, there was an issue with the speech recognition service.")
            output_text.insert(tk.END, "Speech recognition service error.\n")
            return ""

def text_to_speech():
    """Convert user-provided text to speech."""
    text = input_text.get().strip()
    if text:
        speak(text)
        output_text.insert(tk.END, f"Speaking: {text}\n")
    else:
        messagebox.showerror("Error", "Please enter some text to convert to speech.")

def speech_to_text():
    """Convert speech to text and display it."""
    speak("Please speak something, and I will convert it to text.")
    text = listen_command()
    if text:
        output_text.insert(tk.END, f"Recognized Text: {text}\n")
        speak(f"You said: {text}")
    else:
        output_text.insert(tk.END, "No speech recognized.\n")

def execute_task(task):
    """Execute specific tasks like Search, YouTube, or Wikipedia."""
    if task == "search":
        query = input_text.get().strip()
        if not query:
            messagebox.showerror("Error", "Please enter a search query.")
            return
        speak(f"Searching for {query}")
        output_text.insert(tk.END, f"Searching Google for: {query}\n")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif task == "youtube":
        query = input_text.get().strip()
        if not query:
            messagebox.showerror("Error", "Please enter a YouTube search query.")
            return
        speak(f"Searching YouTube for {query}")
        output_text.insert(tk.END, f"Searching YouTube for: {query}\n")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    elif task == "wikipedia":
        query = input_text.get().strip()
        if not query:
            messagebox.showerror("Error", "Please enter a Wikipedia search query.")
            return
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            output_text.insert(tk.END, f"Wikipedia Summary: {results}\n")
            speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results for this. Please be more specific.")
            output_text.insert(tk.END, "DisambiguationError: Multiple results found. Be more specific.\n")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find anything on Wikipedia.")
            output_text.insert(tk.END, "PageError: No results found on Wikipedia.\n")
        except wikipedia.exceptions.WikipediaException as e:
            speak("An error occurred while searching Wikipedia.")
            output_text.insert(tk.END, f"WikipediaException: {e}\n")
        except Exception as e:
            speak("Something went wrong.")
            output_text.insert(tk.END, f"General Error: {e}\n")

def exit_program():
    """Exit the program."""
    speak("Goodbye!")
    root.destroy()

# # Create the GUI
# root = tk.Tk()
# root.title("Voice Assistant")

# Create the GUI
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("700x700")
root.configure(bg="#f0f0f0")

# Header Section
header_frame = tk.Frame(root, bg="#4CAF50", pady=10)
header_frame.pack(fill="x")
header_label = tk.Label(header_frame, text="Voice Assistant", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white")
header_label.pack()

# Menu Label
menu_label = tk.Label(root, text="Voice Assistant Menu", font=("cooper", 12, "bold"))
menu_label.pack(pady=10)

# Input Field
input_label = tk.Label(root, text="Enter your query or text:")
input_label.pack()
input_text = tk.Entry(root, width=50)
input_text.pack(pady=5)

# Buttons for Main Menu Options
text_to_speech_button = tk.Button(root, text="1. Convert Text to Speech", command=text_to_speech, width=30)
text_to_speech_button.pack(pady=5)

speech_to_text_button = tk.Button(root, text="2. Convert Speech to Text", command=speech_to_text, width=30)
speech_to_text_button.pack(pady=5)

# Submenu for Execute Tasks
execute_label = tk.Label(root, text="3. Execute Tasks", font=("Arial", 12, "bold"))
execute_label.pack(pady=10)

search_button = tk.Button(root, text="3.1 Search", command=lambda: execute_task("search"), width=30)
search_button.pack(pady=5)

youtube_button = tk.Button(root, text="3.2 YouTube", command=lambda: execute_task("youtube"), width=30)
youtube_button.pack(pady=5)

wikipedia_button = tk.Button(root, text="3.3 Wikipedia", command=lambda: execute_task("wikipedia"), width=30)
wikipedia_button.pack(pady=5)

# Exit Button
exit_button = tk.Button(root, text="4. Exit", command=exit_program, width=30, bg="red", fg="white")
exit_button.pack(pady=10)

# Output Area
output_label = tk.Label(root, text="Assistant Output:")
output_label.pack()
output_text = scrolledtext.ScrolledText(root, width=60, height=15)
output_text.pack(pady=5)

# Run the GUI
root.mainloop()
