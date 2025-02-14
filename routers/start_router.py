from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from voice2txt.src.Controllers import SpeechController
from face_recognition2.src.controllers import RecognitionController
from face_recognition2.src.controllers.recognition_pipeline import run_recognition_pipeline
from .pathEnums import PathEnums
import asyncio


router = APIRouter()
@router.get("/", response_class=HTMLResponse)
async def vf_starting_page():
    #Serve the HTML page for face recognition and voice2txt.
    with open(PathEnums.voicefacestart.value, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)



@router.get("/start")
async def start_processing():
    """Run face recognition and voice processing concurrently."""
    rc= RecognitionController()
    sc = SpeechController()
    result_f, result_v = await asyncio.gather(
        run_recognition_pipeline(rc),   # Face recognition
        sc.process_speech()       # Speech recognition
    )
    return {
        "result_face": result_f,
        "result_voice": result_v
        }





