from fastapi import FastAPI
from routers.face_routers import router as face_router
from routers.voice_routes import router as voice_router
from routers.start_router import router as start_router
import uvicorn

app = FastAPI()

# Include the face_router
app.include_router(face_router, prefix="/face")
app.include_router(voice_router, prefix="/voice")
app.include_router(start_router, prefix="/process")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

