import speech_recognition as sr
from googletrans import Translator
from models.SpeechModel import SpeechModel

class SpeechService:
    def __init__(self, languages=("en-US", "ar-EG")):
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        self.languages = languages

    def voice_to_text(self):
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.25)
            print(f"Speak now (Supported languages: {', '.join(self.languages)})...")

            try:
                audio = self.recognizer.listen(source)
                print("Processing your input...")
                for language in self.languages:
                    try:
                        recognized_text = self.recognizer.recognize_google(audio, language=language)
                        print(f"You said ({language}): {recognized_text}")

                        translation = None
                        if language == "ar-EG":
                            translation = self.translator.translate(recognized_text, src="ar", dest="en").text
                            print(f"Translation to English: {translation}")
                        elif language == "en-US":
                            translation = self.translator.translate(recognized_text, src="en", dest="ar").text
                            print(f"Translation to Arabic: {translation}")

                        return SpeechModel(recognized_text, language, translation)
                    except sr.UnknownValueError:
                        continue
                print("Sorry, I could not understand the audio in the supported languages.")
                return SpeechModel()
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return SpeechModel()