import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import pandas as pd
from datetime import datetime
import os

FACES_DIR = "registered_faces"
os.makedirs(FACES_DIR, exist_ok=True)

def load_registered_faces():
    faces = {}
    for name in os.listdir(FACES_DIR):
        person_dir = os.path.join(FACES_DIR, name)
        if os.path.isdir(person_dir):
            faces[name] = person_dir
    return faces

def recognize_face(frame, registered_faces):
    if not registered_faces:
        return "Unknown"
    try:
        for name, face_dir in registered_faces.items():
            result = DeepFace.find(
                img_path=frame,
                db_path=face_dir,
                enforce_detection=False,
                silent=True
            )
            if len(result) > 0 and not result[0].empty:
                return name
    except:
        pass
    return "Unknown"

if "emotion_log" not in st.session_state:
    st.session_state.emotion_log = []
if "running" not in st.session_state:
    st.session_state.running = False
if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False

st.sidebar.title("⚙️ เมนู")
page = st.sidebar.radio("เลือกหน้า", ["📷 กล้อง", "📊 Dashboard"])

if page == "📷 กล้อง":
    st.title("😊 Face & Emotion Detection")
    st.markdown("---")

    with st.expander("👤 ลงทะเบียนใบหน้าใหม่"):
        reg_name = st.text_input("ชื่อ:")
        capture_btn = st.button("📸 ถ่ายรูปและลงทะเบียน")

        if capture_btn and reg_name:
            cap = cv2.VideoCapture(0)
            for i in range(10):
                cap.read()
            ret, frame = cap.read()
            cap.release()

            if ret:
                person_dir = os.path.join(FACES_DIR, reg_name)
                os.makedirs(person_dir, exist_ok=True)
                img_path = os.path.join(person_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                cv2.imwrite(img_path, frame)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                st.image(frame_rgb, caption=f"ลงทะเบียน: {reg_name}", width=300)
                st.success(f"✅ ลงทะเบียน '{reg_name}' สำเร็จ!")
            else:
                st.error("ไม่สามารถเปิดกล้องได้")

    registered_faces = load_registered_faces()
    if registered_faces:
        st.info(f"👥 ลงทะเบียนแล้ว: {', '.join(registered_faces.keys())}")
    else:
        st.warning("⚠️ ยังไม่มีใบหน้าที่ลงทะเบียน")

    col1, col2 = st.columns(2)
    with col1:
        start_btn = st.button("▶️ เริ่ม", use_container_width=True)
    with col2:
        stop_btn = st.button("⏹ หยุด", use_container_width=True)

    if start_btn:
        st.session_state.running = True
        st.session_state.show_dashboard = False
        st.session_state.emotion_log = []

    if stop_btn:
        st.session_state.running = False
        st.session_state.show_dashboard = True

    FRAME_WINDOW = st.image([])
    log_placeholder = st.empty()

    if st.session_state.running:
        camera = cv2.VideoCapture(0)
        for i in range(10):
            camera.read()

        while st.session_state.running:
            ret, frame = camera.read()
            if not ret:
                break

            name = recognize_face(frame, registered_faces)

            try:
                result = DeepFace.analyze(
                    frame,
                    actions=["emotion"],
                    enforce_detection=False,
                    silent=True
                )

                for face in result:
                    x = face["region"]["x"]
                    y = face["region"]["y"]
                    w = face["region"]["w"]
                    h = face["region"]["h"]
                    emotion = face["dominant_emotion"]
                    confidence = round(face["emotion"][emotion], 1)

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        f"{name} | {emotion} ({confidence}%)",
                        (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

                    st.session_state.emotion_log.append({
                        "เวลา": datetime.now().strftime("%H:%M:%S"),
                        "ชื่อ": name,
                        "อารมณ์": emotion,
                        "ความมั่นใจ (%)": confidence
                    })

            except:
                pass

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame_rgb)

            if st.session_state.emotion_log:
                df = pd.DataFrame(st.session_state.emotion_log[-10:])
                log_placeholder.dataframe(df, use_container_width=True)

        camera.release()

    if st.session_state.show_dashboard:
        st.success("✅ หยุดการทำงานแล้ว — ไปดู Dashboard ได้เลยครับ!")
        st.sidebar.info("👉 กดที่ Dashboard เพื่อดูผลลัพธ์")

elif page == "📊 Dashboard":
    st.title("📊 Dashboard")
    st.markdown("---")

    if not st.session_state.emotion_log:
        st.info("ยังไม่มีข้อมูล กรุณาเปิดกล้องและเริ่มการตรวจจับก่อนครับ")
    else:
        df = pd.DataFrame(st.session_state.emotion_log)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("จำนวนครั้งที่ detect", len(df))
        with col2:
            top_emotion = df["อารมณ์"].mode()[0]
            st.metric("อารมณ์หลัก", top_emotion)
        with col3:
            unique_people = df["ชื่อ"].nunique()
            st.metric("จำนวนคนที่พบ", unique_people)

        st.markdown("### 📈 สถิติอารมณ์")
        emotion_count = df["อารมณ์"].value_counts().reset_index()
        emotion_count.columns = ["อารมณ์", "จำนวน"]
        st.bar_chart(emotion_count.set_index("อารมณ์"))

        if df["ชื่อ"].nunique() > 1:
            st.markdown("### 👥 อารมณ์แยกตามคน")
            person_emotion = df.groupby(["ชื่อ", "อารมณ์"]).size().reset_index(name="จำนวน")
            st.bar_chart(person_emotion.pivot(index="อารมณ์", columns="ชื่อ", values="จำนวน").fillna(0))

        st.markdown("### 📋 Log ทั้งหมด")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ ดาวน์โหลด Log (CSV)",
            data=csv,
            file_name=f"emotion_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )