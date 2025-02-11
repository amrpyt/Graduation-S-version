from fastapi import FastAPI
from routers.face_routers import router as face_router
import uvicorn

app = FastAPI()

# Include the face_router
app.include_router(face_router, prefix="/face")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

