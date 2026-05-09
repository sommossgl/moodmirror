# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] — 2026-04-23

### Added
- Initial MVP: Streamlit web app
- Face registration via webcam
- Real-time face recognition (DeepFace.find)
- Real-time emotion detection — 7 emotions
- Live dashboard: emotion distribution, per-person breakdown
- CSV export of emotion log
- Bilingual UI (Thai labels)

### Tech
- Streamlit 1.56
- DeepFace 0.0.99
- OpenCV 4.13
- TensorFlow 2.21

### Known Limitations
- Single camera only (Streamlit limitation)
- Emotion log stored in session state (lost on refresh)
- No authentication
- No persistent database

---

## [Unreleased]

### Planned
- [ ] Persistent SQLite log
- [ ] Multi-camera support
- [ ] Authentication
- [ ] Anti-spoofing
- [ ] Cloud deploy (Streamlit Community Cloud)
- [ ] Mobile-friendly UI
