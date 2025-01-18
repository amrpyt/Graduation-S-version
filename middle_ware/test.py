import sys
import os

# Dynamically add the project root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the RecognitionController class
from face_recognition2 import RecognitionController

# Use the class
controller = RecognitionController()
print(controller.greet())

# print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))