import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import wikipedia

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
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            print(f"Command: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
            return ""
        except sr.RequestError:
            speak("Sorry, there was an issue with the speech recognition service.")
            return ""

def execute_command(query):
    """Execute tasks based on the voice command."""
    if 'search' in query:
        query = query.replace("search", "").strip()
        if not query:
            speak("Do you want to type or speak your query? Press 1 to type, 2 to speak.")
            choice = input("Enter your choice (1 or 2): ")
            if choice == '1':
                query = input("Enter your search query: ").strip()
            elif choice == '2':
                speak("Please specify what you want to search for.")
                query = listen_command()
            if not query:
                speak("Still didn't get it. Try again later.")
                return
        speak(f"Searching for {query}")
        print(f"Opening Google search for: {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif 'youtube' in query:
        query = query.replace("youtube", "").strip()
        if not query:
            speak("Do you want to type or speak your query? Press 1 to type, 2 to speak.")
            choice = input("Enter your choice (1 or 2): ")
            if choice == '1':
                query = input("Enter your YouTube search query: ").strip()
            elif choice == '2':
                speak("Please specify what you want to search on YouTube.")
                query = listen_command()
            if not query:
                speak("Still didn't get it. Try again later.")
                return
        speak(f"Searching YouTube for {query}")
        print(f"Opening YouTube search for: {query}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    elif 'wikipedia' in query:
        query = query.replace("wikipedia", "").strip()
        if not query:
            speak("Do you want to type or speak your query? Press 1 to type, 2 to speak.")
            choice = input("Enter your choice (1 or 2): ")
            if choice == '1':
                query = input("Enter your Wikipedia search query: ").strip()
            elif choice == '2':
                speak("Please specify what you want to search on Wikipedia.")
                query = listen_command()
            if not query:
                speak("Still didn’t catch that. Try again later.")
                return
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(f"Wikipedia Summary: {results}")
            speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results for this. Please be more specific.")
            print(f"DisambiguationError: {e}")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find anything on Wikipedia.")
        except wikipedia.exceptions.WikipediaException as e:
            speak("An error occurred while searching Wikipedia.")
            print(f"WikipediaException: {e}")
        except Exception as e:
            speak("Something went wrong.")
            print(f"General Error: {e}")

    elif 'open code' in query:
        speak("Opening Visual Studio Code.")
        os.system("code")  # Make sure VS Code is added to system PATH

    elif 'exit' in query or 'quit' in query:
        speak("Goodbye!")
        exit()

    else:
        speak("Sorry, I don't understand that command.")

def text_to_speech():
    """Convert user-provided text to speech."""
    speak("Do you want to type or speak the text? Press 1 to type, 2 to speak.")
    choice = input("Enter your choice (1 or 2): ")
    if choice == '1':
        text = input("Enter the text you want me to speak: ").strip()
    elif choice == '2':
        speak("Please speak the text you want me to convert to speech.")
        text = listen_command()
    else:
        speak("Invalid choice. Returning to the main menu.")
        return
    if text:
        speak(text)
    else:
        speak("No text provided.")

def speech_to_text():
    """Convert speech to text and display it."""
    speak("Do you want to type or speak the input? Press 1 to type, 2 to speak.")
    choice = input("Enter your choice (1 or 2): ")
    if choice == '1':
        text = input("Enter the text you want me to process: ").strip()
        if text:
            print(f"Recognized Text: {text}")
            speak(f"You entered: {text}")
    elif choice == '2':
        speak("Please speak something, and I will convert it to text.")
        text = listen_command()
        if text:
            print(f"Recognized Text: {text}")
            speak(f"You said: {text}")
        else:
            speak("Sorry, I couldn't recognize anything.")
    else:
        speak("Invalid choice. Returning to the main menu.")

def text_to_speech():
    """Convert user-provided text to speech."""
    speak("Please enter the text you want me to speak.")
    text = input("Enter text: ")
    speak(text)

def speech_to_text():
    """Convert speech to text and display it."""
    speak("Please speak something, and I will convert it to text.")
    text = listen_command()
    if text:
        print(f"Recognized Text: {text}")
        speak(f"You said: {text}")

# Main Program
if __name__ == "__main__":
    while True:
        print("\n--- Voice Assistant Menu ---")
        print("1. Convert Text to Speech")
        print("2. Convert Speech to Text")
        print("3. Execute Commands Based on Voice Input")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            text_to_speech()
        elif choice == '2':
            speech_to_text()
        elif choice == '3':
            speak("Hello, your assistant is ready. What would you like me to do?")
            while True:
                query = listen_command()
                if query:
                    execute_command(query)
        elif choice == '4':
            speak("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
