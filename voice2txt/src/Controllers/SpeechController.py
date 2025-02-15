from ..Services.SpeechService import SpeechService
import json

class SpeechController:
    def __init__(self):
        """Initialize the SpeechController."""
        try:
            self.service = SpeechService()
        except Exception as e:
            print(f"Error initializing SpeechService: {str(e)}")
            self.service = None

    async def process_speech(self):
        """Process speech input with error handling."""
        try:
            if self.service is None:
                return {
                    "text": None,
                    "error": "Speech service not available"
                }
            
            result = await self.service.voice_to_text()
            if "error" in result:
                print(f"Speech recognition error: {result['error']}")
                return {
                    "text": None,
                    "error": result["error"]
                }

            return result

        except Exception as e:
            print(f"Speech processing error: {str(e)}")
            return {
                "text": None,
                "error": str(e)
            }