# #####working#####
# # from fastapi import FastAPI, Request, UploadFile, File, HTTPException
# # from fastapi.responses import HTMLResponse, JSONResponse
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.staticfiles import StaticFiles
# # from fastapi.templating import Jinja2Templates
# # from pydantic import BaseModel

# # import numpy as np
# # import uuid
# # import cv2
# # import base64
# # import os
# # import tempfile
# # from gtts import gTTS

# # # Custom imports
# # from agent.bp2 import chat_with_agent
# # from face_recognitionplsql import (
# #     load_face_app,
# #     cosine_similarity,
# #     identify_person,
# #     generate_card_for_employee
# # )
# # from databasePLSQL import fetch_all_employees

# # app = FastAPI()

# # # ✅ CORS setup
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_methods=["*"],
# #     allow_headers=["*"]
# # )

# # # ✅ Static & Template Mount
# # app.mount("/static", StaticFiles(directory="static"), name="static")
# # templates = Jinja2Templates(directory="templates")

# # # ✅ Page Routes
# # @app.get("/", response_class=HTMLResponse)
# # def home(request: Request):
# #     return templates.TemplateResponse("index.html", {"request": request})

# # @app.get("/chat", response_class=HTMLResponse)
# # def chat(request: Request):
# #     name = request.query_params.get("name", "Guest")
# #     return templates.TemplateResponse("chat.html", {"request": request, "name": name})

# # # ✅ Voice Bot Q&A
# # class Question(BaseModel):
# #     question: str

# # @app.post("/ask")
# # async def ask(q: Question):
# #     try:
# #         result = chat_with_agent(q.question)
# #         return {"answer": result}
# #     except Exception as e:
# #         print("❌ Error in /ask:", str(e))
# #         raise HTTPException(status_code=500, detail="Internal Server Error")

# # # ✅ Face Recognition Endpoint
# # @app.post("/recognize-face")
# # async def recognize_face(file: UploadFile = File(...)):
# #     try:
# #         contents = await file.read()
# #         img_arr = np.frombuffer(contents, np.uint8)
# #         frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

# #         app_model = load_face_app()
# #         faces = app_model.get(frame)

# #         if not faces:
# #             return JSONResponse({"success": False, "message": "No face detected"})

# #         emb = faces[0].embedding
# #         employees = fetch_all_employees()
# #         match = identify_person(emb, employees)

# #         if match:
# #             name = match.get("name")
# #             generate_card_for_employee(match)

# #             greeting = f"Hey {name}, how can I assist you today?"
# #             audio_b64 = text_to_base64(greeting)

# #             return {
# #                 "success": True,
# #                 "name": name,
# #                 "greeting": greeting,
# #                 "audio_base64": audio_b64
# #             }
# #         else:
# #             return JSONResponse({"success": False, "message": "Face not recognized"})

# #     except Exception as e:
# #         print("❌ Face recognition error:", str(e))
# #         raise HTTPException(status_code=500, detail="Error processing face image")

# # # ✅ Utility: Convert text to base64 audio
# # def text_to_base64(text):
# #     tts = gTTS(text=text[:300], lang="en")
# #     temp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.mp3")
# #     tts.save(temp_path)

# #     with open(temp_path, "rb") as f:
# #         audio_data = f.read()
# #     os.remove(temp_path)

# #     return base64.b64encode(audio_data).decode()
# #####working#######
# from fastapi import FastAPI, Request, UploadFile, File, HTTPException
# from fastapi.responses import HTMLResponse, JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel

# import numpy as np
# import uuid
# import cv2
# import base64
# import os
# import tempfile
# from gtts import gTTS
# from urllib.parse import quote_plus

# # Custom imports
# from agent.bp2 import chat_with_agent
# from face_recognitionplsql import (
#     load_face_app,
#     cosine_similarity,
#     identify_person,
#     generate_card_for_employee
# )
# from databasePLSQL import fetch_all_employees

# app = FastAPI()

# # ✅ CORS setup
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# # ✅ Static & Template Mount
# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/output_cards", StaticFiles(directory="output_cards"), name="output_cards")
# templates = Jinja2Templates(directory="templates")

# # ✅ Home Page
# @app.get("/", response_class=HTMLResponse)
# def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# # ✅ Chat Page
# @app.get("/chat", response_class=HTMLResponse)
# def chat(request: Request):
#     name = request.query_params.get("name", "Guest")
#     return templates.TemplateResponse("chat.html", {"request": request, "name": name})

# # ✅ Dynamic Greeting Template Page
# @app.get("/template", response_class=HTMLResponse)
# def show_template(request: Request, title: str = "", message: str = "", image: str = ""):
#     return templates.TemplateResponse("template.html", {
#         "request": request,
#         "title": title,
#         "message": message,
#         "image": image
#     })

# # ✅ Voice Bot API
# class Question(BaseModel):
#     question: str

# @app.post("/ask")
# async def ask(q: Question):
#     try:
#         result = chat_with_agent(q.question)
#         return {"answer": result}
#     except Exception as e:
#         print("❌ Error in /ask:", str(e))
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# # ✅ Recognize Face API
# @app.post("/recognize-face")
# async def recognize_face(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         img_arr = np.frombuffer(contents, np.uint8)
#         frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

#         app_model = load_face_app()
#         faces = app_model.get(frame)

#         if not faces:
#             return JSONResponse({"success": False, "message": "No face detected"})

#         emb = faces[0].embedding
#         employees = fetch_all_employees()
#         match = identify_person(emb, employees)

#         if match:
#             name = match.get("name")
#             greeting_data = generate_card_for_employee(match)

#             if greeting_data:
#                 redirect_url = (
#                     f"/template?"
#                     f"title={quote_plus(greeting_data['event'])}"
#                     f"&message={quote_plus(greeting_data['message'])}"
#                     f"&image={quote_plus(greeting_data['image_url'])}"
#                 )

#                 greeting = greeting_data["message"]
#                 audio_b64 = text_to_base64(greeting)

#                 return {
#                     "success": True,
#                     "name": name,
#                     "greeting": greeting,
#                     "audio_base64": audio_b64,
#                     "redirect_url": redirect_url
#                 }

#             else:
#                 fallback_greeting = f"Hello {name}, good to see you!"
#                 return {
#                     "success": True,
#                     "name": name,
#                     "greeting": fallback_greeting,
#                     "audio_base64": text_to_base64(fallback_greeting),
#                     "redirect_url": None
#                 }

#         else:
#             return JSONResponse({"success": False, "message": "Face not recognized"})

#     except Exception as e:
#         print("❌ Face recognition error:", str(e))
#         raise HTTPException(status_code=500, detail="Error processing face image")

# # ✅ Text to Base64 Audio
# def text_to_base64(text):
#     tts = gTTS(text=text[:300], lang="en")
#     temp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.mp3")
#     tts.save(temp_path)

#     with open(temp_path, "rb") as f:
#         audio_data = f.read()
#     os.remove(temp_path)

#     return base64.b64encode(audio_data).decode()
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import numpy as np
import uuid
import cv2
import base64
import os
import tempfile
from gtts import gTTS
from urllib.parse import quote_plus

# -----------------------
# Custom Module Imports
# -----------------------
from agent.bp2 import chat_with_agent
from face_recognitionplsql import (
    load_face_app,
    cosine_similarity,
    identify_person,
    generate_card_for_employee
)
from databasePLSQL import fetch_all_employees

# -----------------------
# App Initialization
# -----------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# -----------------------
# Static & Template Mounts
# -----------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/output_cards", StaticFiles(directory="output_cards"), name="output_cards")
templates = Jinja2Templates(directory="templates")

# -----------------------
# Routes
# -----------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/chat", response_class=HTMLResponse)
def chat(request: Request):
    name = request.query_params.get("name", "Guest")
    return templates.TemplateResponse("chat.html", {"request": request, "name": name})


@app.get("/template", response_class=HTMLResponse)
def show_template(request: Request, title: str = "", message: str = "", image: str = ""):
    return templates.TemplateResponse("template.html", {
        "request": request,
        "title": title,
        "message": message,
        "image": image
    })


# -----------------------
# Voice Q&A API
# -----------------------
class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask(q: Question):
    try:
        result = chat_with_agent(q.question)
        return {"answer": result}
    except Exception as e:
        print("❌ Error in /ask:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


# -----------------------
# Face Recognition API
# -----------------------
@app.post("/recognize-face")
async def recognize_face(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img_arr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

        app_model = load_face_app()
        faces = app_model.get(frame)

        if not faces:
            return JSONResponse({"success": False, "message": "No face detected"})

        emb = faces[0].embedding
        employees = fetch_all_employees()
        match = identify_person(emb, employees)

        if match:
            name = match.get("name")
            greeting_data = generate_card_for_employee(match)

            greeting = ""
            redirect_url = None

            if greeting_data:
                # Create redirect URL for /template
                redirect_url = (
                    f"/template?"
                    f"title={quote_plus(greeting_data['event'])}"
                    f"&message={quote_plus(greeting_data['message'])}"
                    f"&image={quote_plus(greeting_data['image_url'])}"
                )
                greeting = greeting_data["message"]
            else:
                greeting = f"Hello {name}, good to see you!"

            audio_b64 = text_to_base64(greeting)

            return {
                "success": True,
                "name": name,
                "greeting": greeting,
                "audio_base64": audio_b64,
                "redirect_url": redirect_url
            }

        else:
            return JSONResponse({"success": False, "message": "Face not recognized"})

    except Exception as e:
        print("❌ Face recognition error:", str(e))
        raise HTTPException(status_code=500, detail="Error processing face image")


# -----------------------
# Utility: Text to Base64 Audio
# -----------------------
def text_to_base64(text):
    tts = gTTS(text=text[:300], lang="en")
    temp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.mp3")
    tts.save(temp_path)

    with open(temp_path, "rb") as f:
        audio_data = f.read()
    os.remove(temp_path)

    return base64.b64encode(audio_data).decode()
