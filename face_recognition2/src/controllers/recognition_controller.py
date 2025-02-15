import cv2
from ..models import FacialRecognitionModel
from ..helpers import get_settings
import json
import asyncio

class RecognitionController:
    def __init__(self):
        """Initialize the RecognitionController class."""
    
        self.result = None
        self.model = None
        self.camera = None

    async def initialize_camera(self):
        """Initialize the camera and model."""
        # Always close any existing camera first
        if self.camera is not None:
            self.camera.release()
            
        # Create new camera instance
        self.camera = cv2.VideoCapture(get_settings().CAMER_INPUT)
        if not self.camera.isOpened():
            print("Error: Could not access the camera.")
            return False
            
        # Let the camera warm up
        await asyncio.sleep(0.5)
        return True

    async def start_recognition(self):
        """Capture a single frame and perform recognition."""
        try:
            if self.model is None:
                self.model = await FacialRecognitionModel.Init_FacialRecognitionModel()

            # Initialize camera
            if not await self.initialize_camera():
                return None

            # Try to capture frame multiple times if needed
            ret = False
            frame = None
            for attempt in range(3):
                ret, frame = self.camera.read()
                if ret and frame is not None:
                    break
                await asyncio.sleep(0.2)
            
            if not ret or frame is None:
                print("Error: Failed to capture image after multiple attempts.")
                return None

            # Process the frame
            self.result = await self.model.predict(frame)
            return self.result

        finally:
            # Always release the camera
            if self.camera is not None:
                self.camera.release()
                self.camera = None


        # Predict using the model
        self.result = await self.model.predict(frame)
        
        # Release the camera
        self.camera.release()
        
        return self.result

    async def get_recognition_result(self):
        print("hello from get_recognition_result")
        recognition_result = {
            "class": self.result["class"],
            "name": self.result["name"],
            "confidence": self.result["confidence"]
        }
        print("recognition_result", recognition_result)
        return recognition_result