import asyncio
from Controllers.SpeechController import SpeechController

async def main():
    try:
        speech_controller = SpeechController()
        result = await speech_controller.process_speech()
        
        # Print the result
        print("Result:", result)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
   asyncio.run(main())