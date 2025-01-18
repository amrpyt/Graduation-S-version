import pickle
import os
print(os.path)

current_directory = os.getcwd()
model_path = os.path.join(current_directory, "face_recognition2/src/assets", "face_recognition_model.pkl")



# Print the current working directory
print("Current Working Directory:", current_directory)
print("Model Path:", model_path)
with open(model_path, "rb") as model_file:
                model = pickle.load(model_file)


# /home/xxx/progects/project_struct/face_recognition2/src/assets/face_recognition_model.pkl