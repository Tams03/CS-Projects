# 🧊 SmartFridge – IoT Food Management System

**Course:** IOT  
**Grade:** 92/100  
**Type:** IoT & Mobile Application  
**Technologies:** Python, OpenCV, Pyzbar, Firebase, Pyrebase, Flutter, Gemini AI, Raspberry Pi, OpenFoodFacts API  

---

## Overview

SmartFridge is an IoT-based system designed to manage home food inventory intelligently: barcode-based scanning with a Raspberry Pi camera, a Flutter mobile app, and Firebase for real-time sync. It sends expiration and low-stock alerts and provides AI-powered recipe suggestions.

---

## Problem & Motivation

- Households often waste food because they forget what’s in the fridge or when items expire.  
- Manual inventory checks and planning shopping lists take time and effort.  
- SmartFridge solves this by automatically detecting items, tracking inventory, and notifying users before food expires.

---

## 🎯 Goals

- Reduce food waste through real-time expiration alerts  
- Save time with automatic shopping lists and remote access  
- Provide a modern, intuitive, AI-assisted user experience  

---

## 👩‍💻 My Role

- Implemented barcode recognition using OpenCV + Pyzbar  
- Integrated Firebase real-time database for inventory tracking  
- Created the user manual and final documentation  

---

## 🧩 System Architecture

- **Application Layer:** Flutter mobile app (Android 8.0+), displays inventory, shows alerts, interacts with AI Gemini assistant  
- **Service Layer:** Handles barcode recognition and product identification using OpenCV + Pyzbar and OpenFoodFacts APIs  
- **Business Layer:** Manages logic for expiration tracking, alert scheduling, and shopping list generation  
- **Data Layer:** Stores inventory, dates, and user data in Firebase, synchronized in real time  

---

## ⚙️ Hardware Components

- Raspberry Pi with built-in camera for barcode scanning  
- Wi-Fi module for real-time synchronization with Firebase  
- *(Future feature): Pressure sensors for detecting item removal and quantity*  

---

## 🚀 Core Features

- Real-time tracking of fridge inventory  
- Expiration and low-stock alerts  
- Smart suggestions using Gemini AI (e.g., “What can I cook with milk and eggs?”)  
- Barcode scanning with Raspberry Pi camera  
- Mobile app for inventory management and shopping lists  
- Remote access and real-time updates  

---

## 🧪 Prototype

- Working fridge prototype with a single barcode camera  
- Fully functional Android Flutter app with Firebase backend  
- Integrated Gemini AI for recipe suggestions and item queries  
- API connection to OpenFoodFacts for nutritional and product data  

---

## 🎬 Demo Video

Watch the SmartFridge prototype in action: [Demo Video](https://github.com/Tams03/CS-Projects/blob/main/SmartFridge/smartfridge-demo.mp4)

---

## 💼 Business & Impact

- **Innovation:** Combines IoT, AI, and mobile computing for a real-life problem  
- **Social Impact:** Reduces food waste, saves money, and simplifies daily routines  
- **Commercial Potential:** Licensing opportunities for appliance manufacturers and grocery partners  

---

## 🧰 Tools & Technologies

Python, OpenCV, Pyzbar, Pyrebase, Firebase, Requests, Flutter, Gemini AI, Raspberry Pi, Figma, Postman, Git, Canva  

---

## 📂 Project Files

- **Final Report (Hebrew):** [Link](https://github.com/Tams03/CS-Projects/blob/main/SmartFridge/Reports/SmartFridge%20%E2%80%93%20%D7%9E%D7%A1%D7%9E%D7%9A%20%D7%90%D7%A4%D7%99%D7%95%D7%9F%20%D7%A1%D7%95%D7%A4%D7%99.pdf)  
- **Presentation Slides (Hebrew):**[Link](https://github.com/Tams03/CS-Projects/blob/main/SmartFridge/Reports/IOT_FINAL_PRECENTATION.pdf) 
- **User Guide (Hebrew):** [Link](https://github.com/Tams03/CS-Projects/blob/main/SmartFridge/Reports/SmartFridge%20-%20%D7%9E%D7%93%D7%A8%D7%99%D7%9A%20%D7%9C%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9.pdf)
- **Github Repository:**[Link]()

---

## 📈 Results & Reflection

The prototype successfully demonstrated seamless IoT integration and real-time inventory tracking.  
Gained hands-on experience with computer vision, cloud synchronization, and AI-based user assistance.  
Strengthened understanding of full-stack IoT development.
