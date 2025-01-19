import cv2
from ..models import FacialRecognitionModel
from ..helpers import get_settings
import json
import asyncio


class RecognitionController:
    def __init__(self):
        """Initialize the RecognitionController class."""
        self.model = FacialRecognitionModel()  # Already supports asynchronous operations
        self.result = None
        self.camera = cv2.VideoCapture(get_settings().CAMER_INPUT)

    async def start_recognition(self):
        """Start the facial recognition process using the webcam."""
        if not self.camera.isOpened():
            print("Error: Could not access the camera.")
            return

        print("Press 'q' to quit.")

        loop = asyncio.get_event_loop()

        while True:
            ret, frame = self.camera.read()
            if not ret:
                print("Error: Failed to capture image.")
                break

            # Predict using the model asynchronously
            self.result = await self.model.predict(frame)

            label = self.result["name"]
            person_class = self.result["class"]
            confidence = self.result["confidence"]

            # Overlay the prediction on the frame
            text = f"{label} ({person_class}, {confidence * 100:.2f}%)"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Facial Recognition", frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources
        self.camera.release()
        cv2.destroyAllWindows()

    async def get_recognition_result(self):
        """Get the most recent recognition result."""
        if self.result:
            recognition_result = {
                "class": self.result["class"],
                "name": self.result["name"],
                "confidence": self.result["confidence"]
            }
            return json.dumps(recognition_result)
        return json.dumps({"error": "No result available yet"})
