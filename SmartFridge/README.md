# 🧊 SmartFridge – IoT Food Management System
**Grade:** 92/100  
**Type:** IoT & Mobile Application  
**Technologies:** Python, OpenCV, Pyzbar, Firebase, Pyrebase, Flutter, Gemini AI, Raspberry Pi, OpenFoodFacts API

---

## Overview
SmartFridge is an IoT system for home food inventory: barcode-based scanning with a Raspberry Pi camera, a Flutter mobile app, and Firebase for real-time sync. It sends expiration and low-stock alerts and provides AI-powered recipe suggestions.

## Problem & Motivation
Households waste food due to forgotten items and manual inventory. SmartFridge automates tracking and alerts to reduce waste and save time.

## Key Features
- Real-time inventory tracking  
- Expiration & low-stock alerts  
- Automatic shopping lists  
- Gemini AI suggestions (e.g., "What can I cook with milk and eggs?")  
- Barcode scanning (Raspberry Pi camera)

## Architecture & Tools
- Application: Flutter (Android 8.0+)  
- Vision: OpenCV + pyzbar for barcode detection  
- Backend: Firebase (real-time DB) via Pyrebase  
- Hardware: Raspberry Pi + camera, Wi-Fi module  
- APIs: OpenFoodFacts for product info

## Prototype & Results
- Prototype with single camera + Flutter app working with Firebase.  
- Outcome: Working demo, real-time sync, successful user flows.
