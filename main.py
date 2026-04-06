import uuid
import json
from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent

load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

session_service = InMemorySessionService()
APP_NAME = "DischargeSummary"
USER_ID  = "clinician"

runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)


@app.on_event("startup")
async def startup():
    global SESSION_ID
    SESSION_ID = str(uuid.uuid4())
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    print(f"[DischargeSummary] Session: {SESSION_ID}")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    notes: str = data.get("notes", "").strip()

    if not notes:
        raise HTTPException(status_code=400, detail="No clinical notes provided.")
    if len(notes) < 30:
        raise HTTPException(status_code=400, detail="Please provide more detail about the patient's admission.")

    print(f"[DischargeSummary] Generating for: {notes[:80]}...")

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=(
            f"Generate a complete discharge summary from the following clinical notes:\n\n{notes}"
        ))],
    )

    final_response_text = ""
    try:
        for event in runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=user_message):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

    try:
        session = await session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
        result = session.state.get("discharge_summary")
        if result is None:
            result = json.loads(final_response_text)
    except (json.JSONDecodeError, AttributeError) as e:
        raise HTTPException(status_code=500, detail=f"Could not parse output: {str(e)}")

    payload = result.model_dump() if hasattr(result, "model_dump") else result
    return JSONResponse(content=payload)
