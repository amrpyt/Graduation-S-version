from typing import Dict, Any
import asyncio
import httpx
import json

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from voice2txt.src.Controllers.SpeechController import SpeechController
from face_recognition2.src.controllers.recognition_controller import RecognitionController
from face_recognition2.src.controllers import combine_results
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
        "Access-Control-Allow-Headers": "Content-Type"
    }

def format_json_to_markdown(data: dict) -> str:
    """Convert JSON data to a markdown formatted string."""
    def format_value(value):
        if isinstance(value, (dict, list)):
            return f"\n```json\n{json.dumps(value, indent=2)}\n```"
        return str(value)

    md_lines = []
    for key, value in data.items():
        if isinstance(value, dict):
            md_lines.append(f"## {key}")
            for sub_key, sub_value in value.items():
                md_lines.append(f"- **{sub_key}**: {format_value(sub_value)}")
        else:
            md_lines.append(f"## {key}")
            md_lines.append(format_value(value))
    
    return "\n".join(md_lines)

def create_error_response(message: str, details: Any = None) -> JSONResponse:
    """Create a standardized error response."""
    content = {
        "error": message,
        "markdown": f"## Error\n{message}\n\n{details if details else ''}"
    }
    if details:
        content["details"] = details
    return JSONResponse(content=content, headers=get_response_headers())

async def serve_html_page():
    """Helper function to serve the HTML page."""
    try:
        with open(PathEnums.voicefacestart.value, "r", encoding='utf-8') as file:
            html_content = file.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        print(f"Error reading template: {str(e)}")
        return create_error_response(
            message="Failed to load template",
            details=str(e)
        )

@router.get("/")
async def vf_starting_page():
    """Serve the HTML page at root."""
    return await serve_html_page()

@router.get("/start")
async def start_processing():
    """Run face recognition and voice processing concurrently."""
    try:
        # Start the face recognition and voice processing concurrently
        result_f, result_v = await asyncio.gather(
            recognition_controller.start_recognition(),   # Face recognition
            speech_controller.process_speech(),      # Speech recognition
            return_exceptions=True    # Don't let one failure stop the other
        )
        
        # Handle face recognition result
        if isinstance(result_f, Exception):
            print(f"Face recognition error: {str(result_f)}")
            return create_error_response(
                message="Face recognition failed",
                details=str(result_f)
            )
        elif result_f is None:
            return create_error_response(
                message="No face detected",
                details="Face detection failed to identify any faces in the image"
            )
            
        # Handle speech recognition result
        if isinstance(result_v, Exception):
            print(f"Speech recognition error: {str(result_v)}")
            return create_error_response(
                message="Speech recognition failed",
                details=str(result_v)
            )

        # Combine results in the desired format
        recognition_result = await combine_results(result_f, result_v)
        
        # Send to chat API
        chat_api_url = "https://primary-production-5212.up.railway.app/webhook/chat/message"
        headers = {"Content-Type": "application/json"}
        
        try:
            async with httpx.AsyncClient() as client:
                chat_response = await client.post(
                    chat_api_url,
                    json=recognition_result,
                    headers=headers,
                    timeout=10.0
                )
                chat_result = chat_response.json()
                
                # Format the final response
                final_result = {
                    "recognition": {
                        "name": result_f["name"],
                        "userType": result_f["class"],
                        "message": result_v.get("text", "No speech detected")
                    }
                }

                # Add chat response if available
                if chat_result:
                    final_result["chat_response"] = chat_result

                if "error" in result_v:
                    final_result["recognition"]["speech_error"] = result_v["error"]
                
                # Process chat result
                if "timestamp" in chat_result:
                    final_result["timestamp"] = chat_result["timestamp"]
                if "error" in chat_result:
                    final_result["chat_error"] = chat_result["error"]

                # Add markdown formatted version
                final_result["markdown"] = format_json_to_markdown(final_result)

                return JSONResponse(
                    content=final_result,
                    headers=get_response_headers()
                )
                
        except Exception as e:
            error_msg = str(e)
            print(f"Chat API error: {error_msg}")
            response_data = {
                "recognition": {
                    "name": result_f["name"],
                    "userType": result_f["class"],
                    "message": result_v.get("text", "No speech detected"),
                },
                "chat_error": error_msg
            }
            response_data["markdown"] = format_json_to_markdown(response_data)
            return JSONResponse(
                content=response_data,
                headers=get_response_headers()
            )

    except Exception as e:
        print(f"Error during processing: {str(e)}")
        return create_error_response(
            message="Processing failed",
            details=str(e)
        )

@router.get("/result")
async def get_recognition_result():
    """Fetch the recognition result without starting the process."""
    result = await recognition_controller.get_recognition_result()
    response = {"status": "fetched", "result": result}
    response["markdown"] = format_json_to_markdown(response)
    return response
