# 😊 Face & Emotion Detection

> Real-time face recognition + emotion analytics — built with Streamlit + DeepFace
>
> A hobby/learning project by **sommossgl** (Sommoss G.)

---

## ✨ Features

- 📷 **Face Registration** — capture face from webcam and register a person
- 🧠 **Real-time Recognition** — match live faces against registered users
- 😀 **Emotion Detection** — detect 7 emotions in real-time (happy, sad, angry, surprise, fear, disgust, neutral)
- 📊 **Live Dashboard** — analytics: emotion distribution, per-person breakdown, downloadable CSV log
- 🎥 **Webcam Integration** — works with built-in or USB cameras

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit 1.56 |
| Face Recognition + Emotion | DeepFace 0.0.99 |
| Computer Vision | OpenCV 4.13 |
| ML Backend | TensorFlow 2.21 |
| Data | Pandas |

---

## 🚀 Setup

### 1. Clone

```bash
git clone https://github.com/sommossgl/face-detection.git
cd face-detection
```

### 2. Create virtual env + install deps

```bash
python3 -m venv venv
source venv/bin/activate

pip install streamlit deepface opencv-python pandas tensorflow
```

> **Note:** TensorFlow + DeepFace install takes ~5-10 min the first time.

### 3. Run

```bash
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## 📖 Usage

### Register a face
1. Open the app
2. Expand **"👤 ลงทะเบียนใบหน้าใหม่"**
3. Type your name → click **📸 ถ่ายรูปและลงทะเบียน**
4. ✅ Face saved to `registered_faces/<name>/`

### Detect faces & emotions
1. Click **▶️ เริ่ม**
2. Camera turns on — face box + emotion appear in real-time
3. Click **⏹ หยุด** to stop and view dashboard

### View dashboard
- Total detections
- Top emotion
- Emotion bar chart
- Per-person emotion breakdown
- Download CSV log

---

## 📁 Project Structure

```
face-detection/
├── app.py                    # Main Streamlit app
├── registered_faces/         # User face images (gitignored — PII)
│   └── <name>/
│       ├── *.jpg            # Captured face
│       └── *.pkl            # DeepFace embedding cache
├── requirements.txt          # Python deps
├── .gitignore
└── README.md
```

---

## ⚠️ Privacy Notes

- **Face images are PII** — `registered_faces/` is `.gitignored` and never pushed
- Only register your own face or with explicit consent
- For production use, comply with **PDPA (Thailand)** / **GDPR (EU)** / local privacy laws

---

## 🗺 Roadmap (if I keep tinkering)

- [ ] Persistent SQLite log (currently session-only)
- [ ] Multi-camera support
- [ ] Authentication (currently open)
- [ ] Anti-spoofing (detect photo-of-photo attacks)
- [ ] Deploy to cloud (Streamlit Community Cloud / Render)
- [ ] Mobile-friendly UI
- [ ] Anti-bias evaluation (Asian face accuracy)

---

## 📜 License

MIT — feel free to fork and learn from it.

---

## 🤝 Contributing

This is a personal hobby project, but PRs welcome if you find bugs or add fun features.

---

Made with ☕ by [sommossgl](https://github.com/sommossgl)
