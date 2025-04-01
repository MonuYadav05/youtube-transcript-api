from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi, YouTubeTranscriptApiException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def home_root():
    return {"message":"success"}

@app.get("/transcript/{video_id}")
def get_transcript(video_id: str):  # Specify the type of video_id
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([d['text'] for d in transcript_list])
        transcript_with_timestamps = [
            {"text": entry["text"], "start": entry["start"], "duration": entry["duration"]}
            for entry in transcript_list
        ]
        return {"transcript": transcript , "transcriptWithTimestamps": transcript_with_timestamps}
    except YouTubeTranscriptApiException as e:
        # If an exception occurs (e.g., no transcript available)
        raise HTTPException(status_code=200, detail=f"Error fetching transcript")
    except Exception as e:
        # Catch any other unforeseen exceptions
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
