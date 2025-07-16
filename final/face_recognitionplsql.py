# # import cv2
# # import numpy as np
# # import streamlit as st
# # from insightface.app import FaceAnalysis
# # from datetime import date, datetime
# # import json
# # import os
# # import time
# # from databasePLSQL import fetch_all_employees, fetch_image_blob_by_name, init_db
# # from generate_templateplsql import fill_template, render_to_image
# # from tts import speak_text

# # LOG_PATH = "greet_log.json"
# # OUTPUT_DIR = "output_cards"

# # os.makedirs(OUTPUT_DIR, exist_ok=True)

# # def load_log():
# #     if not os.path.exists(LOG_PATH):
# #         with open(LOG_PATH, "w") as f:
# #             json.dump({}, f)
# #     with open(LOG_PATH, "r") as f:
# #         return json.load(f)

# # def update_log(name):
# #     log = load_log()
# #     today = str(date.today())
# #     log[name] = today
# #     with open(LOG_PATH, "w") as f:
# #         json.dump(log, f)

# # def already_greeted(name):
# #     log = load_log()
# #     return log.get(name) == str(date.today())

# # @st.cache_resource(show_spinner=False)
# # def load_face_app():
# #     app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
# #     app.prepare(ctx_id=-1)
# #     return app

# # def cosine_similarity(a, b):
# #     norm_a = np.linalg.norm(a)
# #     norm_b = np.linalg.norm(b)
# #     if norm_a == 0 or norm_b == 0:
# #         return 0.0
# #     return np.dot(a, b) / (norm_a * norm_b)

# # def identify_person(embedding, known_employees, threshold=0.4):
# #     best_score = -1.0
# #     best_match = None
# #     for emp in known_employees:
# #         known_emb_blob = emp.get('embedding')
# #         if known_emb_blob is None:
# #             continue
# #         try:
# #             known_emb = np.frombuffer(known_emb_blob, dtype=np.float32)
# #         except Exception as e:
# #             print(f"Error decoding embedding for {emp.get('name')}: {e}")
# #             continue
# #         if known_emb.shape[0] != embedding.shape[0]:
# #             print(f"Skipping {emp.get('name')} due to shape mismatch.")
# #             continue
# #         sim = cosine_similarity(known_emb, embedding)
# #         print(f"[DEBUG] Best match: {emp.get('name')} with similarity {sim:.3f}")
# #         if sim > best_score and sim >= threshold:
# #             best_score = sim
# #             best_match = emp
# #     if best_match:
# #         return best_match['name'], best_match['dob']
# #     return None, None

# # def generate_and_display_card(name, image_blob, card_placeholder):
# #     html_path = fill_template(name, image_blob)
# #     render_to_image(html_path, name)
# #     card_path = os.path.join(OUTPUT_DIR, f"birthday_{name.replace(' ', '_')}.png")
# #     time.sleep(0.2)
# #     if os.path.exists(card_path):
# #         card_placeholder.image(card_path, caption=f"🎂 Birthday Card for {name}", use_container_width=True)
# #     else:
# #         st.warning(f"❌ Could not generate birthday card for {name}.")

# # def run_recognition():
# #     st.title("🎥 Face Recognition Panel")

# #     if "camera_running" not in st.session_state:
# #         st.session_state.camera_running = False

# #     col1, col2 = st.columns(2)
# #     with col1:
# #         if not st.session_state.camera_running:
# #             if st.button("▶️ Start Camera", key="start_camera_btn_rec"):
# #                 st.session_state.camera_running = True
# #                 st.rerun()
# #         else:
# #             if st.button("⏹️ Stop Camera", key="stop_camera_btn_rec"):
# #                 st.session_state.camera_running = False
# #                 st.success("✅ Camera stopped.")
# #                 st.rerun()

# #     if not st.session_state.camera_running:
# #         st.info("Click 'Start Camera' to begin face recognition.")
# #         return

# #     app = load_face_app()
# #     known_employees = fetch_all_employees()
# #     known_employees_with_embeddings = [emp for emp in known_employees if emp.get('embedding') is not None]

# #     if not known_employees_with_embeddings:
# #         st.warning("⚠️ No employees with face embeddings found in the database.")
# #         st.session_state.camera_running = False
# #         return

# #     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# #     if not cap.isOpened():
# #         st.error("❌ Failed to open webcam.")
# #         return

# #     frame_placeholder = st.empty()
# #     card_placeholder = st.empty()
# #     greeted_names = set()
# #     active_birthday_names = set()
# #     refresh_time = time.time()
# #     frame_count = 0

# #     while st.session_state.camera_running:
# #         ret, frame = cap.read()
# #         if not ret:
# #             st.warning("⚠️ Failed to read frame from camera.")
# #             break

# #         if time.time() - refresh_time > 10:
# #             known_employees = fetch_all_employees()
# #             known_employees_with_embeddings = [emp for emp in known_employees if emp.get('embedding') is not None]
# #             refresh_time = time.time()

# #         faces = app.get(frame)
# #         current_names_in_frame = set()

# #         for face in faces:
# #             embedding = face.normed_embedding
# #             bbox = face.bbox.astype(int)
# #             name, dob = identify_person(embedding, known_employees_with_embeddings, threshold=0.4)
# #             x1, y1, x2, y2 = bbox
# #             color = (0, 255, 0) if name else (0, 0, 255)
# #             label = name if name else "Unknown"

# #             cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
# #             cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

# #             if name:
# #                 current_names_in_frame.add(name)
# #                 if dob:
# #                     try:
# #                         dob_obj = datetime.strptime(dob, "%Y-%m-%d").date()
# #                         today = date.today()
# #                         if (dob_obj.month, dob_obj.day) == (today.month, today.day):
# #                             if name not in greeted_names and not already_greeted(name):
# #                                 speak_text(f"🎉 Happy Birthday, {name}!")
# #                                 update_log(name)
# #                                 greeted_names.add(name)
# #                                 image_blob = fetch_image_blob_by_name(name)
# #                                 if image_blob:
# #                                     generate_and_display_card(name, image_blob, card_placeholder)
# #                                     active_birthday_names.add(name)
# #                     except Exception as e:
# #                         print(f"[ERROR] Birthday check failed for {name}: {e}")

# #         for name_on_card in list(active_birthday_names):
# #             if name_on_card not in current_names_in_frame:
# #                 card_placeholder.empty()
# #                 active_birthday_names.remove(name_on_card)

# #         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #         frame_count += 1
# #         if frame_count % 3 == 0:
# #             frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

# #         time.sleep(0.001)

# #     cap.release()

# # if __name__ == "__main__":
# #     st.set_page_config(page_title="Face Recognition", layout="centered")
# #     st.title("Welcome to the Face Recognition System")
# #     init_db()
# #     run_recognition()
# import cv2
# import numpy as np
# import streamlit as st
# from insightface.app import FaceAnalysis
# from datetime import date, datetime
# import json
# import os
# import time
# from databasePLSQL import fetch_all_employees, fetch_image_blob_by_name, init_db
# from generate_templateplsql import fill_template, render_to_image,image_blob_to_base64
# from tts import speak_text

# LOG_PATH = "greet_log.json"
# OUTPUT_DIR = "output_cards"

# os.makedirs(OUTPUT_DIR, exist_ok=True)

# def load_log():
#     if not os.path.exists(LOG_PATH):
#         with open(LOG_PATH, "w") as f:
#             json.dump({}, f)
#     with open(LOG_PATH, "r") as f:
#         return json.load(f)

# def update_log(name):
#     log = load_log()
#     today = str(date.today())
#     if name not in log:
#         log[name] = []
#     if today not in log[name]:
#         log[name].append(today)
#     with open(LOG_PATH, "w") as f:
#         json.dump(log, f)

# def already_greeted(name):
#     log = load_log()
#     return str(date.today()) in log.get(name, [])

# @st.cache_resource(show_spinner=False)
# def load_face_app():
#     app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
#     app.prepare(ctx_id=-1)
#     return app

# def cosine_similarity(a, b):
#     norm_a = np.linalg.norm(a)
#     norm_b = np.linalg.norm(b)
#     if norm_a == 0 or norm_b == 0:
#         return 0.0
#     return np.dot(a, b) / (norm_a * norm_b)

# def identify_person(embedding, known_employees, threshold=0.4):
#     best_score = -1.0
#     best_match = None
#     for emp in known_employees:
#         known_emb_blob = emp.get('embedding')
#         if known_emb_blob is None:
#             continue
#         try:
#             known_emb = np.frombuffer(known_emb_blob, dtype=np.float32)
#         except Exception as e:
#             print(f"Error decoding embedding for {emp.get('name')}: {e}")
#             continue
#         if known_emb.shape[0] != embedding.shape[0]:
#             print(f"Skipping {emp.get('name')} due to shape mismatch.")
#             continue
#         sim = cosine_similarity(known_emb, embedding)
#         print(f"[DEBUG] Best match: {emp.get('name')} with similarity {sim:.3f}")
#         if sim > best_score and sim >= threshold:
#             best_score = sim
#             best_match = emp
#     if best_match:
#         return best_match
#     return None

# def generate_and_display_card(emp, card_placeholder):
#     name = emp['name']
#     image_blob = emp.get('full_image')
#     dob = emp.get('dob')
#     doj = emp.get('doj')
#     is_guest = emp.get('is_special_guest', False)
#     designation = emp.get('designation')

#     today = date.today()

#     if not image_blob:
#         return

#     if is_guest and not already_greeted(f"{name}_guest"):
#         html_path = fill_template("templates/special_guest_template.html", name, image_blob, is_birthday=False, is_guest=True)
#         render_to_image(html_path, name, event_type="guest")
#         speak_text(f"🎖️ Welcome special guest {name} to TechProjects!")
#         card_path = os.path.join(OUTPUT_DIR, f"guest_{name.replace(' ', '_')}.png")
#         card_placeholder.image(card_path, caption=f"🎖️ Special Guest: {name}", use_container_width=True)
#         update_log(f"{name}_guest")

#     if doj:
#         doj_obj = datetime.strptime(doj, "%Y-%m-%d").date() if isinstance(doj, str) else doj
#         if doj_obj.strftime("%m-%d") == today.strftime("%m-%d") and not already_greeted(f"{name}_doj"):
#             html_path = fill_template("templates/welcome_template.html", name, image_blob, is_birthday=False, is_guest=False, designation=designation)
#             render_to_image(html_path, name, event_type="welcome")
#             speak_text(f"👋 Welcome to the team, {name}, our new {designation}!")
#             card_path = os.path.join(OUTPUT_DIR, f"welcome_{name.replace(' ', '_')}.png")
#             card_placeholder.image(card_path, caption=f"👋 Welcome: {name}", use_container_width=True)
#             update_log(f"{name}_doj")

#     if dob:
#         dob_obj = datetime.strptime(dob, "%Y-%m-%d").date() if isinstance(dob, str) else dob
#         if dob_obj.strftime("%m-%d") == today.strftime("%m-%d") and not already_greeted(f"{name}_dob"):
#             html_path = fill_template("templates/birthday_template.html", name, image_blob)
#             render_to_image(html_path, name)
#             speak_text(f"🎉 Happy Birthday, {name}!")
#             card_path = os.path.join(OUTPUT_DIR, f"birthday_{name.replace(' ', '_')}.png")
#             card_placeholder.image(card_path, caption=f"🎂 Birthday Card for {name}", use_container_width=True)
#             update_log(f"{name}_dob")

# def run_recognition():
#     st.title("🎥 Face Recognition Panel")

#     if "camera_running" not in st.session_state:
#         st.session_state.camera_running = False

#     col1, col2 = st.columns(2)
#     with col1:
#         if not st.session_state.camera_running:
#             if st.button("▶️ Start Camera", key="start_camera_btn_rec"):
#                 st.session_state.camera_running = True
#                 st.rerun()
#         else:
#             if st.button("⏹️ Stop Camera", key="stop_camera_btn_rec"):
#                 st.session_state.camera_running = False
#                 st.success("✅ Camera stopped.")
#                 st.rerun()

#     if not st.session_state.camera_running:
#         st.info("Click 'Start Camera' to begin face recognition.")
#         return

#     app = load_face_app()
#     known_employees = fetch_all_employees()
#     known_employees_with_embeddings = [emp for emp in known_employees if emp.get('embedding') is not None]

#     if not known_employees_with_embeddings:
#         st.warning("⚠️ No employees with face embeddings found in the database.")
#         st.session_state.camera_running = False
#         return

#     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#     if not cap.isOpened():
#         st.error("❌ Failed to open webcam.")
#         return

#     frame_placeholder = st.empty()
#     card_placeholder = st.empty()
#     refresh_time = time.time()
#     frame_count = 0
    
#     while st.session_state.camera_running:
#         ret, frame = cap.read()
#         if not ret:
#             st.warning("⚠️ Failed to read frame from camera.")
#             break

#         if time.time() - refresh_time > 10:
#             known_employees = fetch_all_employees()
#             known_employees_with_embeddings = [emp for emp in known_employees if emp.get('embedding') is not None]
#             refresh_time = time.time()

#         faces = app.get(frame)

#         for face in faces:
#             embedding = face.normed_embedding
#             bbox = face.bbox.astype(int)
#             emp = identify_person(embedding, known_employees_with_embeddings, threshold=0.4)
#             x1, y1, x2, y2 = bbox
#             color = (0, 255, 0) if emp else (0, 0, 255)
#             label = emp['name'] if emp else "Unknown"

#             cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
#             cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

#             if emp:
#                 generate_and_display_card(emp, card_placeholder)

#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         frame_count += 1
#         if frame_count % 3 == 0:
#             frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

#         time.sleep(0.001)

#     cap.release()

# if __name__ == "__main__":
#     st.set_page_config(page_title="Face Recognition", layout="centered")
#     st.title("Welcome to the Face Recognition System")
#     init_db()
#     run_recognition()
import cv2
import numpy as np
import streamlit as st
from insightface.app import FaceAnalysis
from datetime import date, datetime
import json
import os
import time

from databasePLSQL import fetch_all_employees, fetch_image_blob_by_name, init_db
from generate_templateplsql import (
    fill_template,
    render_to_image,
    image_blob_to_base64
)

from tts import speak_text

LOG_PATH = "greet_log.json"
OUTPUT_DIR = "output_cards"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_log():
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            json.dump({}, f)
    with open(LOG_PATH, "r") as f:
        return json.load(f)

def update_log(name_key):
    log = load_log()
    today = str(date.today())
    log[name_key] = today
    with open(LOG_PATH, "w") as f:
        json.dump(log, f)

def already_greeted(name_key):
    log = load_log()
    return log.get(name_key) == str(date.today())

@st.cache_resource(show_spinner=False)
def load_face_app():
    app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=-1)
    return app

def cosine_similarity(a, b):
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return np.dot(a, b) / (norm_a * norm_b)

def identify_person(embedding, known_employees, threshold=0.4):
    best_score = -1.0
    best_match = None
    for emp in known_employees:
        known_emb_blob = emp.get('embedding')
        if known_emb_blob is None:
            continue
        try:
            known_emb = np.frombuffer(known_emb_blob, dtype=np.float32)
        except Exception as e:
            print(f"Error decoding embedding for {emp.get('name')}: {e}")
            continue
        if known_emb.shape[0] != embedding.shape[0]:
            print(f"Skipping {emp.get('name')} due to shape mismatch.")
            continue
        sim = cosine_similarity(known_emb, embedding)
        print(f"[DEBUG] Best match: {emp.get('name')} with similarity {sim:.3f}")
        if sim > best_score and sim >= threshold:
            best_score = sim
            best_match = emp
    return best_match

def generate_and_display_card(emp, card_placeholder):
    name = emp.get("name")
    dob = emp.get("dob")
    doj = emp.get("doj")
    designation = emp.get("designation")
    is_guest = emp.get("is_special_guest", False)
    image_blob = fetch_image_blob_by_name(name)

    if not image_blob:
        return

    image_b64 = image_blob_to_base64(image_blob)
    today = date.today()

    if is_guest and not already_greeted(f"{name}_guest"):
        html_path = fill_template("templates/special_guest_template.html", name, image_b64, is_birthday=False)
        render_to_image(html_path, name, event_type="guest")
        speak_text(f"🎖️ Welcome special guest {name} to TechProjects!")
        card_path = os.path.join(OUTPUT_DIR, f"guest_{name.replace(' ', '_')}.png")
        if os.path.exists(card_path):
            card_placeholder.image(card_path, caption=f"🌟 Special Guest: {name}", use_container_width=True)
        update_log(f"{name}_guest")

    if doj:
        try:
            doj_obj = datetime.strptime(doj, "%Y-%m-%d").date()
            if (doj_obj.month, doj_obj.day) == (today.month, today.day) and not already_greeted(f"{name}_join"):
                html_path = fill_template("templates/welcome_template.html", name, image_b64, is_birthday=False, designation=designation)
                render_to_image(html_path, name, event_type="welcome")
                speak_text(f"👋 Welcome to TechProjects, {name}, our new {designation}!")
                card_path = os.path.join(OUTPUT_DIR, f"welcome_{name.replace(' ', '_')}.png")
                if os.path.exists(card_path):
                    card_placeholder.image(card_path, caption=f"👋 Welcome: {name}", use_container_width=True)
                update_log(f"{name}_join")
        except Exception as e:
            print(f"[ERROR] Joining day check failed for {name}: {e}")

    if dob:
        try:
            dob_obj = datetime.strptime(dob, "%Y-%m-%d").date()
            if (dob_obj.month, dob_obj.day) == (today.month, today.day) and not already_greeted(f"{name}_bday"):
                html_path = fill_template("templates/birthday_template.html", name, image_b64, is_birthday=True)
                render_to_image(html_path, name, event_type="birthday")
                speak_text(f"🎉 Happy Birthday, {name}!")
                card_path = os.path.join(OUTPUT_DIR, f"birthday_{name.replace(' ', '_')}.png")
                if os.path.exists(card_path):
                    card_placeholder.image(card_path, caption=f"🎂 Birthday Card for {name}", use_container_width=True)
                update_log(f"{name}_bday")
        except Exception as e:
            print(f"[ERROR] Birthday check failed for {name}: {e}")

def run_recognition():
    st.title("🎥 Face Recognition Panel")

    if "camera_running" not in st.session_state:
        st.session_state.camera_running = False

    col1, col2 = st.columns(2)
    with col1:
        if not st.session_state.camera_running:
            if st.button("▶️ Start Camera", key="start_camera_btn_rec"):
                st.session_state.camera_running = True
                st.rerun()
        else:
            if st.button("⏹️ Stop Camera", key="stop_camera_btn_rec"):
                st.session_state.camera_running = False
                st.success("✅ Camera stopped.")
                st.rerun()

    if not st.session_state.camera_running:
        st.info("Click 'Start Camera' to begin face recognition.")
        return

    app = load_face_app()
    known_employees = fetch_all_employees()
    known_employees_with_embeddings = [emp for emp in known_employees if emp.get('embedding') is not None]

    if not known_employees_with_embeddings:
        st.warning("⚠️ No employees with face embeddings found in the database.")
        st.session_state.camera_running = False
        return

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        st.error("❌ Failed to open webcam.")
        return

    frame_placeholder = st.empty()
    card_placeholder = st.empty()
    shown_names = set()
    refresh_time = time.time()
    frame_count = 0

    while st.session_state.camera_running:
        ret, frame = cap.read()
        if not ret:
            st.warning("⚠️ Failed to read frame from camera.")
            break

        if time.time() - refresh_time > 10:
            known_employees = fetch_all_employees()
            known_employees_with_embeddings = [emp for emp in known_employees if emp.get('embedding') is not None]
            refresh_time = time.time()

        faces = app.get(frame)
        current_names_in_frame = set()

        for face in faces:
            embedding = face.normed_embedding
            bbox = face.bbox.astype(int)
            emp = identify_person(embedding, known_employees_with_embeddings, threshold=0.4)

            name = emp.get("name") if emp else None
            x1, y1, x2, y2 = bbox
            color = (0, 255, 0) if name else (0, 0, 255)
            label = name if name else "Unknown"

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            if name:
                current_names_in_frame.add(name)
                if name not in shown_names:
                    generate_and_display_card(emp, card_placeholder)
                    shown_names.add(name)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_count += 1
        if frame_count % 3 == 0:
            frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

        time.sleep(0.001)

    cap.release()
# def generate_card_for_employee(emp):
#     """
#     Generates greeting card and speaks based on employee's special event today (DOB/DOJ/Guest).
#     Used in FastAPI-based face recognition workflow.
#     """
#     from generate_templateplsql import fill_template, render_to_image, image_blob_to_base64
#     name = emp.get("name")
#     dob = emp.get("dob")
#     doj = emp.get("doj")
#     designation = emp.get("designation")
#     is_guest = emp.get("is_special_guest", False)
#     image_blob = fetch_image_blob_by_name(name)

#     if not image_blob:
#         print(f"⚠️ No image blob found for {name}")
#         return

#     image_b64 = image_blob_to_base64(image_blob)
#     today = date.today()

#     # 🌟 Special Guest
#     if is_guest and not already_greeted(f"{name}_guest"):
#         html_path = fill_template("templates/special_guest_template.html", name, image_b64, is_birthday=False)
#         render_to_image(html_path, name, event_type="guest")
#         speak_text(f"🎖️ Welcome special guest {name} to TechProjects!")
#         update_log(f"{name}_guest")

#     # 👋 Joining Anniversary
#     if doj:
#         try:
#             doj_obj = datetime.strptime(doj, "%Y-%m-%d").date()
#             if (doj_obj.month, doj_obj.day) == (today.month, today.day) and not already_greeted(f"{name}_join"):
#                 html_path = fill_template("templates/welcome_template.html", name, image_b64, is_birthday=False, designation=designation)
#                 render_to_image(html_path, name, event_type="welcome")
#                 speak_text(f"👋 Welcome to TechProjects, {name}, our new {designation}!")
#                 update_log(f"{name}_join")
#         except Exception as e:
#             print(f"[ERROR] Joining day check failed for {name}: {e}")

#     # 🎉 Birthday
#     if dob:
#         try:
#             dob_obj = datetime.strptime(dob, "%Y-%m-%d").date()
#             if (dob_obj.month, dob_obj.day) == (today.month, today.day) and not already_greeted(f"{name}_bday"):
#                 html_path = fill_template("templates/birthday_template.html", name, image_b64, is_birthday=True)
#                 render_to_image(html_path, name, event_type="birthday")
#                 speak_text(f"🎉 Happy Birthday, {name}!")
#                 update_log(f"{name}_bday")
#         except Exception as e:
#             print(f"[ERROR] Birthday check failed for {name}: {e}")
# ✅ Step 1: Modify `generate_card_for_employee` to return rendered image path, title, and message

def generate_card_for_employee(emp):
    from generate_templateplsql import fill_template, render_to_image, image_blob_to_base64
    from datetime import datetime, date
    import os

    name = emp.get("name")
    dob = emp.get("dob")
    doj = emp.get("doj")
    designation = emp.get("designation")
    is_guest = emp.get("is_special_guest", False)
    image_blob = fetch_image_blob_by_name(name)

    if not image_blob:
        return None

    image_b64 = image_blob_to_base64(image_blob)
    today = date.today()

    if is_guest and not already_greeted(f"{name}_guest"):
        html_path = fill_template("templates/guest_template.html", name, image_b64)
        png_path = render_to_image(html_path, name, event_type="guest")
        update_log(f"{name}_guest")
        return {
            "event": "Special Guest",
            "message": f"Welcome special guest {name} to TechProjects!",
            "image_url": f"/{png_path}"
        }

    if doj:
        try:
            doj_obj = datetime.strptime(doj, "%Y-%m-%d").date()
            if (doj_obj.month, doj_obj.day) == (today.month, today.day) and not already_greeted(f"{name}_join"):
                html_path = fill_template("templates/joining_template.html", name, image_b64, designation=designation)
                png_path = render_to_image(html_path, name, event_type="welcome")
                update_log(f"{name}_join")
                return {
                    "event": "Welcome Onboard",
                    "message": f"Welcome {name}, our new {designation}!",
                    "image_url": f"/{png_path}"
                }
        except Exception as e:
            print("[ERROR] DOJ check failed:", e)

    if dob:
        try:
            dob_obj = datetime.strptime(dob, "%Y-%m-%d").date()
            if (dob_obj.month, dob_obj.day) == (today.month, today.day) and not already_greeted(f"{name}_bday"):
                html_path = fill_template("templates/birthday_template.html", name, image_b64)
                png_path = render_to_image(html_path, name, event_type="birthday")
                update_log(f"{name}_bday")
                return {
                    "event": "Happy Birthday",
                    "message": f"Wishing you a joyful day, {name}!",
                    "image_url": f"/{png_path}"
                }
        except Exception as e:
            print("[ERROR] DOB check failed:", e)

    return None


if __name__ == "__main__":
    st.set_page_config(page_title="Face Recognition", layout="centered")
    st.title("Welcome to the Face Recognition System")
    init_db()
    run_recognition()
