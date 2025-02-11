from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse, StreamingResponse
import uvicorn
import cv2

app = FastAPI()

# Base router to check server status
base_router = APIRouter()

@base_router.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>Server is up! Name: FastAPI Camera App | Version: 1.0</h1>"

# Camera router
camera_router = APIRouter()

@camera_router.get("/camera", response_class=HTMLResponse)
async def camera_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Camera Stream</title>
    </head>
    <body>
        <h1>Camera Stream</h1>
        <p>The live camera feed is shown below:</p>
        <img src="/camera/stream" width="640" height="480" alt="Camera Stream">
        <button id="actionButton">Press Me</button>
        <p id="responseText"></p>
        <script>
            document.getElementById('actionButton').addEventListener('click', function() {
                fetch('/camera/button-action')
                    .then(response => response.text())
                    .then(data => {
                        document.getElementById('responseText').innerText = data;
                    });
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

def generate_frames():
    cap = cv2.VideoCapture(0)  # Open the default camera (usually the webcam)
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

@camera_router.get("/camera/stream")
async def camera_stream():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@camera_router.get("/camera/button-action")
async def button_action():
    return "I'm on"

# Register routers
app.include_router(base_router, prefix="/base")
app.include_router(camera_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)