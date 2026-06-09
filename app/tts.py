import pyttsx3
import threading

def speak(text):

    def run_tts():

        engine = pyttsx3.init()

        engine.setProperty(
            "rate",
            170
        )

        engine.setProperty(
            "volume",
            1.0
        )

        engine.say(text)

        engine.runAndWait()

    threading.Thread(
        target=run_tts,
        daemon=True
    ).start()