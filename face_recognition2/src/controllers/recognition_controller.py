import cv2
from ..models import FacialRecognitionModel

class RecognitionController:
    def __init__(self):
        """Initialize the RecognitionController class."""
        self.model = FacialRecognitionModel()

    def start_recognition(self):
        """Start the facial recognition process using the webcam."""
        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            print("Error: Could not access the camera.")
            return

        print("Press 'q' to quit.")

        while True:
            ret, frame = camera.read()
            if not ret:
                print("Error: Failed to capture image.")
                break

            # Predict using the model
            result = self.model.predict(frame)
            label = result["label"]
            confidence = result["confidence"]

            # Overlay the prediction on the frame
            text = f"{label} ({confidence * 100:.2f}%)"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Facial Recognition", frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources
        camera.release()
        cv2.destroyAllWindows()
