# from face_recognition2 import RecognitionController

# from middle_ware import DataPipeline
from face_recognition2 import RecognitionController
import asyncio
rc = RecognitionController()
rc.start_recognition()

# asyncio.run(print( await rc.get_recognition_result()))
print(asyncio.run(rc.get_recognition_result()))
