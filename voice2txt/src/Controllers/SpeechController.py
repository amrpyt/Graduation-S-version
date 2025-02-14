from ..Services.SpeechService import SpeechService


class SpeechController:
    def __init__(self):
        self.service = SpeechService()

    async def process_speech(self):
        result = await self.service.voice_to_text()
        return await result.to_dict()