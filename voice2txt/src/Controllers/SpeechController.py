from ..Services.SpeechService import SpeechService
import json

class SpeechController:
    def __init__(self):
        try:
            self.service = SpeechService()
        except Exception as e:
            print(f"Error initializing SpeechService: {str(e)}")
            self.service = None

    async def process_speech(self):
        try:
            if self.service is None:
                # Return dummy response if service isn't available
                return {
                    "text": "Speech recognition is not available",
                    "error": "Speech service initialization failed"
                }
            
            result = await self.service.voice_to_text()
            return result

        except Exception as e:
            print(f"Speech recognition error: {str(e)}")
            return {
                "text": "Speech recognition encountered an error",
                "error": str(e)
            }