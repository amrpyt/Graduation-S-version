import pickle
import numpy as np
import cv2
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

current_directory = os.getcwd()
model_path = os.path.join(current_directory, "face_recognition2/src/assets", "face_recognition_model.pkl")
label_map_path = os.path.join(current_directory, "face_recognition2/src/assets", "label_map.pkl")

class FacialRecognitionModel:
    def __init__(self, model_path=model_path, label_map_path=label_map_path):
        """Initialize the FacialRecognitionModel class.
        
        Args:
            model_path (str): Path to the trained model file.
            label_map_path (str): Path to the label map file.
        """
        self.model_path = model_path
        self.label_map_path = label_map_path
        self.model = None
        self.label_map = None
        self.reverse_label_map = None

        # self._load_model_and_labels()

    @classmethod
    async def Init_FacialRecognitionModel(self):
        object = FacialRecognitionModel()
        await object._load_model_and_labels()
        return object


    async def _load_model_and_labels(self):
        """Private method to load the trained model and label map."""
        loop = asyncio.get_event_loop()
        
        try:
            with ThreadPoolExecutor() as executor:
                self.model = await loop.run_in_executor(executor, self._load_pickle_file, self.model_path)
                self.label_map = await loop.run_in_executor(executor, self._load_pickle_file, self.label_map_path)

            # Create a reverse label map for easy decoding
            self.reverse_label_map = {v: k for k, v in self.label_map.items()}
        
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error loading files: {e}")

    def _load_pickle_file(self, path):
        """Helper method to load a pickle file."""
        with open(path, "rb") as file:
            return pickle.load(file)

    async def preprocess_image(self, image):
        """Preprocess the image for model prediction.
        
        Args:
            image (numpy.ndarray): The input image.
        
        Returns:
            numpy.ndarray: Preprocessed image ready for prediction.
        """
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            gray_image = await loop.run_in_executor(executor, cv2.cvtColor, image, cv2.COLOR_BGR2GRAY)
            resized_image = await loop.run_in_executor(executor, cv2.resize, gray_image, (100, 100))
            return resized_image.flatten().reshape(1, -1)

    async def predict(self, image):
        """Predict the class, name, and confidence for a given image.
        
        Args:
            image (numpy.ndarray): The input image.
        
        Returns:
            dict: Prediction result containing class, name, and confidence.
        """
        preprocessed_image = await self.preprocess_image(image)
        loop = asyncio.get_event_loop()
        
        with ThreadPoolExecutor() as executor:
            probabilities = await loop.run_in_executor(executor, self.model.predict_proba, preprocessed_image)
        probabilities = probabilities[0]

        predicted_label = np.argmax(probabilities)
        confidence = probabilities[predicted_label]
        label_name = self.reverse_label_map[predicted_label]

        # Split label_name into class and name
        person_class, person_name = label_name.split('/')

        return {
            "class": person_class,
            "name": person_name,
            "confidence": confidence
        }
