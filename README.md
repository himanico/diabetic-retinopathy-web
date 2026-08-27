# 🩺 RetinaCare - Diabetic Retinopathy Detection System

RetinaCare is a web-based Diabetic Retinopathy Detection System developed using Python, Flask, TensorFlow, HTML, CSS and JavaScript.

The system allows users to register, enter patient information, complete a health assessment, upload a retinal image and receive an AI-based diabetic retinopathy prediction.

## 🌐 Live Demo

https://diabetic-retinopathy-web.onrender.com

## ✨ Features

- 🏠 Welcome/Home Page
- 👤 User Registration
- 🔐 User Login
- 🧑‍⚕️ Patient Profile
- 📋 Health/Symptom Assessment
- 🖼️ Retina Image Upload
- 🤖 AI-based Diabetic Retinopathy Prediction
- 📊 Prediction Result and Confidence
- 📜 Screening History
- 📱 Responsive Medical UI

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- SQLite

### Machine Learning
- TensorFlow
- Keras
- CNN / Deep Learning
- Retinal Image Classification

### Deployment
- GitHub
- Render

## 📂 Project Structure

```text
diabetic-retinopathy-web/
│
├── app.py
├── requirements.txt
├── README.md
├── .python-version
│
├── model/
│   └── fmodel.keras
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── patient.html
│   ├── symptoms.html
│   ├── upload.html
│   ├── result.html
│   └── history.html
│
└── static/
    ├── style.css
    ├── images/
    └── uploads/