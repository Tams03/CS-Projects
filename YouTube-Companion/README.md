# 📺 YouTube Companion – Channel Insights & Recommendations

**Course:** Advanced Development  
**Grade:** 98/100  
**Type:** Python Application & Data Analysis Tool  
**Technologies:** Python, YouTube API  

---

## Overview

YouTube Companion is a Python tool that retrieves, compares, and analyzes YouTube channel data.  
It helps users quickly gain insights into channel performance, compare multiple channels, and receive personalized channel recommendations — all **without needing to know how to code**.

---

## Problem & Motivation

- Millions of YouTube channels make it difficult to track performance or find relevant content manually.  
- Content creators, marketers, and enthusiasts need data-driven insights to make informed decisions.  
- Manual tracking is time-consuming and inefficient.  
- This project provides fast, automated analysis and personalized recommendations for YouTube channels.

---

## 🎯 Goals

- Retrieve detailed channel information including subscribers, views, video count, engagement rate, content frequency, most popular video, and overall category  
- Compare multiple channels based on key metrics to identify top performers  
- Suggest new channels based on input channels or topics 

---

## 👩‍💻 My Role

- Full YouTube API integration for real-time data retrieval  
- Data processing entirely in Python  
- Designed outputs for comparison and recommendations  
- Developed a professional interactive page for non-coders

---

## 🧩 System Architecture

- **backend.py** – Python scripts for data retrieval, processing, and analysis  
- **app.py** – Interactive app interface for users  
- Modular design allows easy extension for additional features  

---

## 🚀 Core Features

- Channel data retrieval  
- Channel comparison by Subscribers, Views, and Engagement Rate  
- Personalized channel recommendations  
- User-friendly interactive page for anyone to access and explore insights  

---

## 🧪 Prototype

- Colab Notebook: YouTube Companion Notebook  
- Tested example outputs of channel data and recommendations  

---

## 💼 Business & Impact

- Enables automatic comparisons and personalized recommendations, saving time and effort  
- Demonstrates Python programming, API integration, and data analysis skills  

---

## 🧰 Tools & Technologies

Python, YouTube API, Streamlit  

---

## 🖥️ Interactive Page Instructions (For Users – No Coding Required)

### How to Access

The app is hosted online and can be accessed through your browser:  
[Streamlit App Link](#) *(replace with your actual deployed URL)*

### How to Use

1. Choose one of the three actions:

   - **Compare Channels** – Enter two or more channel names to compare subscribers, views, and engagement  
   - **Get Channel Data** – Enter one or more channels to see detailed statistics and metrics  
   - **Suggest Me a Channel** – Either:  
     - Enter channels you like to get a similar channel recommendation, or  
     - Enter a topic you like to get a recommended channel based on that topic  

2. Input your channel names or topic in the provided text box  

3. Click the corresponding action button  

4. View results instantly:

   - Comparison results show as tables and key metrics  
   - Channel suggestions display with clickable YouTube links  

Enjoy the insights and explore recommended channels **without needing to know Python**  

---

## 💻 Developer Instructions (Optional – For Running or Editing the App)

### Requirements

Make sure you have Python installed. Required packages:

```bash
pip install streamlit google-api-python-client pandas matplotlib
````

### Running Locally

Ensure `backend.py` and `app.py` are in the same directory

Run the app:

```bash
streamlit run app.py
```

Your default browser will open with the interactive YouTube Companion page

### Optional Deployment

To make the app accessible online:

**Streamlit Cloud (free for small projects)**

1. Push `app.py`, `backend.py`, and `requirements.txt` to GitHub
2. Go to Streamlit Cloud and connect your repository
3. Your app will be hosted online with a shareable URL

Other hosting options:

* Heroku
* AWS Elastic Beanstalk
* Google Cloud Run

---

## 📂 Project Files

* Backend Code: `backend.py`
* Interactive App: `app.py`
* Github Repository: [Link]()
* Colab Notebook: [Link](https://github.com/Tams03/CS-Projects/blob/main/YouTube-Companion/YouTube-Companion-code)
* Example outputs of channel data and recommendations

---

## 📈 Results & Reflection

* Successfully created a YouTube channel analysis tool that retrieves, compares, and recommends channels
* Enables automatic comparisons and personalized recommendations, saving time and effort
* Demonstrates Python programming, API integration, and data analysis skills
