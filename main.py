
from face_recognition2 import RecognitionController
import asyncio
# rc = RecognitionController()
# asyncio.run(rc.start_recognition())
# print(asyncio.run(rc.get_recognition_result()))

async def main():
    rc = RecognitionController()
    await rc.start_recognition()
    print(await rc.get_recognition_result())

asyncio.run(main())