import json

async def combine_results(recognition_result, voice_result):
    """
    Combines the recognition result and voice result into the desired JSON format.
    """
    output = {
        "name": recognition_result.get("name", "Unknown User"),
        "userType": recognition_result.get("class", "unknown"),
        "message": voice_result.get("text", "No message detected")
    }

    print("Combined Output:", output)
    return output