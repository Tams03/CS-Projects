# 🌐 Live Text Translator – Real-Time Multilingual Communication

**Course:** Deep Learning and Its Applications  
**Grade:** 99/100  
**Type:** Deep Learning & Web Application  
**Technologies:** Python, NLLB-200 (transformer-based translation model), FastAPI, WebSocket, GitHub Codespaces, Firebase, Streamlit  

---

## Overview

Live Text Translator (**LinguaLink**) is a real-time multilingual translator for text and planned speech conversations.  
It allows users speaking different languages to communicate instantly and seamlessly using the **NLLB-200 transformer model** for high-accuracy translation.  

> **Note:** NLLB-200 (No Language Left Behind) is a transformer-based model developed by Meta/Facebook, capable of translating between 200 languages with high accuracy, even for low-resource languages.  

The project includes a **core real-time translation system** and a lightweight **interactive demo page** for non-coders to explore translations.  

---

## Problem & Motivation

- Around 7,159 languages exist worldwide, but most people speak only 1–2.  
- Language barriers affect communication in business, healthcare, education, and personal interactions.  
- Existing translation tools are often too slow or impractical for real-time conversations.  
- LinguaLink addresses this by providing instant, bidirectional translations between multiple languages.

---

## 🎯 Goals

- Enable real-time translation between multiple languages  
- Support cross-language communication in group chats  
- Achieve low-latency, high-accuracy translation using NLLB-200  
- Prepare for future speech-to-speech, speech-to-text, and text-to-speech integration  

---

## 👩‍💻 My Role

- Implemented server-side translation using NLLB-200 in FastAPI  
- Built real-time WebSocket chat system for multilingual messaging  
- Conducted stress tests with multiple concurrent clients  
- Prepared documentation and README  
- Assisted with project planning and technical decisions  
- Developed a professional **interactive demo page** for non-coders  

---

## 🧩 System Architecture

- **Application Layer:** Telegram bot interface and WebSocket chat for real-time user interaction  
- **Service Layer:** FastAPI server handles translation requests using the NLLB-200-distilled-600M model  
- **Business Layer:** Manages pairing of users, session handling, and fallback strategies for large models  
- **Data Layer:** Stores user preferences and group metadata in Firestore  

---

## 🚀 Core Features

- Real-time text translation in group chats and direct messages  
- Automatic user pairing and reassignment if a participant disconnects  
- WebSocket communication for low-latency, dynamic message delivery  
- Future enhancements: speech-to-speech / speech-to-text / text-to-speech, additional language support  
- Development Environment: GitHub Codespaces with Python 3.12  
- Model: NLLB-200-distilled-600M (transformer-based, pre-trained by Meta/Facebook)  

---

## 🖥️ Interactive Demo Page

A lightweight **demo page** is available online for users who want to explore translations without installing or running the full project.  

- The demo allows typing messages in two languages with real-time translation between them.  
- For stability, the demo may use a lighter-weight model or a translation API (e.g., Google Translate).  
- The **core project still uses the full NLLB-200 model** for production-level accuracy.  
- Access the demo here: [Live Demo Page](https://appapppy-livetexttranslator.streamlit.app/)

---

## 🧪 Prototype

- WebSocket chat system running on FastAPI server  
- Telegram bot integrated for group translation  
- NLLB-200 transformer for high-accuracy translation  
- Tested in GitHub Codespaces using Python 3.12 environment  

---

## 💼 Business & Impact

- **Innovation:** Leverages cutting-edge NLLB-200 deep learning models for seamless multilingual communication  
- **Social Impact:** Bridges language gaps in real-time, helping businesses, healthcare, education, and global collaboration  
- **Future Potential:** Expand to 200+ languages, integrate speech recognition and synthesis, deploy as a public service  

---

## 🧰 Tools & Technologies

Python, FastAPI, Streamlit, WebSocket, Transformers (NLLB-200), PyTorch  

---

## 📂 Project Files

- **Presentation (Hebrew):** [Link](https://github.com/Tams03/CS-Projects/blob/main/LiveTextTranslator/Deep_Learning.pdf)  
- **Google Survey & Results:** [Link](https://docs.google.com/forms/d/15E-CbHtdQRPs7BiZ-v9oNSgnP_QKuv6a1FX3L-Kx6GI/edit#responses)  
- **Github Repository:** [Link](https://github.com/Tams03/DL-Translator-Project.git)  

---

## 📈 Results & Reflection

- Achieved a functional MVP for real-time multilingual text translation  
- Preliminary translation accuracy: BLEU score >0.35 (EN ↔ HE) and latency under 1 second  
- System successfully handled multiple concurrent users (10 clients across 6 languages) without latency issues  
- Gained hands-on experience with deep learning, real-time communication, and multilingual application design  
- Demonstrates innovation, scalability, and practical application, making it portfolio-ready
