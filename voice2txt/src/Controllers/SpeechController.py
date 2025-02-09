from Services.SpeechService import SpeechService

class SpeechController:
    def __init__(self):
        self.service = SpeechService()

    def process_speech(self):
        result = self.service.voice_to_text()
        return result.to_dict()