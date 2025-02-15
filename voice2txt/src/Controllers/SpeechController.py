from ..Services.SpeechService import SpeechService
import json


class SpeechController:
    def __init__(self):
        self.service = SpeechService()

    async def process_speech(self):
        result = await self.service.voice_to_text()
        return result # TODO: Return the result in the desired JSON format