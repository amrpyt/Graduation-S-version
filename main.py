from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.face_routers import router as face_router
from routers.voice_routes import router as voice_router
from routers.start_router import router as start_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Root route for testing
@app.get("/")
async def root():
    return {"message": "Server is running"}

# Include routers
app.include_router(face_router, prefix="/face")
app.include_router(voice_router, prefix="/voice")
app.include_router(start_router, prefix="/process")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
