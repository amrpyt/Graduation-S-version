# from face_recognition2 import RecognitionController

# from middle_ware import DataPipeline
from face_recognition2 import RecognitionController

rc = RecognitionController()
rc.start_recognition()
print(rc.get_recognition_result())
