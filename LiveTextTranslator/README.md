# 🌐 LiveTextTranslator – Real-Time Multilingual Communication

**Course:** Deep Learning and Its Applications  
**Grade:** 99/100  
**Type:** Deep Learning & Web Application  
**Technologies:** Python, FastAPI, WebSocket, Streamlit, Hugging Face Transformers, NLLB-200, Firebase

---

## Overview
LiveTextTranslator (named **LinguaLink**) is a real-time multilingual translator for text and planned speech conversations.  
It allows users speaking different languages to communicate instantly and seamlessly, leveraging the **NLLB-200 transformer model** for high-accuracy translation.  
An **interactive demo page** is available to showcase the tool to non-coders and allow them to try live translations.  
The project also lays the groundwork for future speech-to-speech, speech-to-text, and text-to-speech integration.

---

## Problem & Motivation
Language barriers hinder global collaboration, communication, and learning. Many existing translation tools are slow or limited in language support. LiveTextTranslator addresses this problem by providing instant translation in multiple languages with high accuracy.

---

## Goals
- Build a fast, real-time text translation application 
- Support multiple languages for global communication  
- Provide an interactive demo for users to test translations  
- Facilitate easy integration into messaging platforms or customer support systems 

---

## Role
This project was completed as part of a group. My specific contributions included:
- Developed the backend using FastAPI and WebSocket for real-time communication
- Integrated transformer-based multilingual model (NLLB-200) for translation
- Created the interactive demo page using Streamlit
- Tested multiple languages and large input texts to ensure performance and accuracy
  
---

## System Architecture / How it Works
- Users input text via a web interface connected to a FastAPI backend using WebSocket 
- The backend sends text to the transformer model for translation 
- Translated text is returned instantly to the user interface
- Multiple users can use the system simultaneously with low latency

---

## Features
- Translates text in real-time across multiple languages  
- Provides WebSocket-based backend for instant response  
- Offers interactive demo page for testing translations  
- Supports multiple simultaneous users 

---


## Prototype
- The prototype demonstrates the real-time translation workflow 
- Users can input text, select source and target languages, and receive translations instantly
- The system handles multiple inputs and simulates live conversation flows

---

## Demo / Instructions
- Access the interactive demo page via the provided [link](https://appapppy-livetexttranslator.streamlit.app/).  
- **Instructions to use the demo:**
  **1.** Open the demo page in your web browser
  **2.** Select the source language of your text 
  **3.** Select the target language for translation
  **4.** Type or paste your text into the input box
  **5.** Press “Enter” or submit to receive the translation
  **6.** Test multiple languages and longer text inputs to observe real-time translation  
  **7.** Input consecutive messages to simulate a conversation flow; the system handles multiple users and continuous text 

---

## Business Impact
- Facilitates global communication and collaboration 
- Can be integrated into messaging platforms, educational tools, or online customer support
- Demonstrates practical application of transformer-based NLP models

---

## Tools & Technologies
- Python, FastAPI, WebSocket  
- Streamlit for interactive demo  
- Hugging Face Transformers, NLLB-200  
- Firebase for storage and logging
> **Note:** NLLB-200 (No Language Left Behind) is a transformer-based model developed by Meta/Facebook, capable of translating between 200 languages with high accuracy, even for low-resource languages   

---

## Project Files

- **Presentation:** [Link](https://github.com/Tams03/CS-Projects/blob/main/LiveTextTranslator/Deep_Learning.pdf)  
- **Google Survey & Results:** [Link](https://docs.google.com/forms/d/15E-CbHtdQRPs7BiZ-v9oNSgnP_QKuv6a1FX3L-Kx6GI/edit#responses)  
- **Github Repository:** [Link](https://github.com/Tams03/DL-Translator-Project.git)  

---

## Results
- Provided accurate and fast translations in real-time  
- Supported multiple languages and users simultaneously  
- Demonstrated feasibility of deploying transformer models for live translation

---

## Reflections
- Learned to implement real-time WebSocket communication with deep learning models 
- Gained experience integrating NLP models into interactive applications  
- Understood challenges of handling multi-language inputs and performance optimization
- Learned to work effectively in a team
