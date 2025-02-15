try:
    import speech_recognition as sr
except ImportError as e:
    print(f"Speech recognition import error: {str(e)}")
    sr = None

class SpeechService:
    def __init__(self, languages=("en-US", "ar-EG")):
        if sr is None:
            raise ImportError("Speech recognition module not available")
        
        self.recognizer = sr.Recognizer()
        # Adjust recognition parameters
        self.recognizer.energy_threshold = 300  # Minimum audio energy to consider for recording
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_ratio = 1.5
        self.recognizer.pause_threshold = 0.8  # Seconds of non-speaking audio before a phrase is considered complete
        self.languages = languages
        self.test_microphone()

    def test_microphone(self):
        """Test if microphone is available and working."""
        try:
            print("Testing microphone...")
            with sr.Microphone() as source:
                # Short adjustment for testing
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Microphone is working")
        except Exception as e:
            print(f"Microphone error: {str(e)}")
            raise Exception("Microphone not available or not working properly")

    async def voice_to_text(self):
        """Convert voice to text using speech recognition."""
        try:
            print("Starting voice recognition...")
            with sr.Microphone() as source:
                print("Adjusting for ambient noise...")
                # Longer adjustment for actual use
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                print("Listening... (Speak now)")
                try:
                    # Increased timeout and added phrase_time_limit
                    audio = self.recognizer.listen(source, 
                                                 timeout=10,  # Increased timeout
                                                 phrase_time_limit=10)  # Max seconds for a phrase
                    print("Audio captured successfully")
                except sr.WaitTimeoutError:
                    print("No speech detected within timeout period")
                    return {"error": "No speech detected. Please try speaking louder or check your microphone."}

                print("Processing audio...")
                # Try each language for recognition
                for language in self.languages:
                    try:
                        print(f"Attempting recognition in {language}...")
                        recognized_text = self.recognizer.recognize_google(audio, language=language)
                        print(f"Successfully recognized in {language}: {recognized_text}")
                        return {"text": recognized_text}
                            
                    except sr.UnknownValueError:
                        print(f"Could not understand audio in {language}")
                        continue
                    except sr.RequestError as e:
                        print(f"Could not request results for {language}; {e}")
                        return {"error": f"Speech recognition service error: {str(e)}"}
                    
                print("Could not understand the audio in any supported language")
                return {"error": "Could not understand the audio. Please try speaking more clearly."}
                
        except Exception as e:
            print(f"Speech recognition error: {str(e)}")
            return {"error": f"Speech recognition error: {str(e)}. Please try again."}