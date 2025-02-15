from typing import Dict, Any
import asyncio
import httpx

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

from voice2txt.src.Controllers.SpeechController import SpeechController
from face_recognition2.src.controllers.recognition_controller import RecognitionController
from face_recognition2.src.controllers.output_controller import combine_results
from .pathEnums import PathEnums

# Initialize router
router = APIRouter()

# Initialize controllers
recognition_controller = RecognitionController()
speech_controller = SpeechController()

def get_response_headers() -> Dict[str, str]:
    """Get common response headers with CORS settings."""
    return {
        "Content-Type": "application/json; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

async def serve_html_page():
    """Helper function to serve the HTML page."""
    try:
        with open(PathEnums.voicefacestart.value, "r", encoding='utf-8') as file:
            html_content = file.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        print(f"Error reading template: {str(e)}")
        return JSONResponse(
            content={"error": "Failed to load template", "details": str(e)},
            headers=get_response_headers()
        )

@router.get("/")
@router.get("/process/")
async def main_page():
    """Serve the HTML page."""
    return await serve_html_page()

@router.get("/start")
async def start_processing():
    """Process face recognition and voice input."""
    try:
        # Start face recognition first
        face_result = await recognition_controller.start_recognition()
        if face_result is None:
            return JSONResponse(
                content={"error": "No face detected"},
                headers=get_response_headers()
            )

        # Get voice input (optional)
        try:
            voice_result = await speech_controller.process_speech()
        except Exception as e:
            print(f"Speech recognition error: {str(e)}")
            voice_result = {"text": None}

        # Format response
        response_data = {
            "recognition": {
                "name": face_result["name"],
                "class": face_result["class"],
                "message": voice_result.get("text")
            }
        }

        return JSONResponse(
            content=response_data,
            headers=get_response_headers()
        )

    except Exception as e:
        print(f"Processing error: {str(e)}")
        return JSONResponse(
            content={"error": "Processing failed", "details": str(e)},
            headers=get_response_headers()
        )
