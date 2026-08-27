from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
import uuid
from datetime import datetime


app = Flask(__name__)

# =========================================================
# SECRET KEY
# =========================================================

app.secret_key = "diabetic_retinopathy_secret_key"


# =========================================================
# LOAD ML MODEL
# =========================================================

MODEL_PATH = os.path.join("model", "fmodel.keras")

model = load_model(MODEL_PATH)

print("Model loaded successfully!")


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================================================
# USER DATABASE MODEL
# =========================================================

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    full_name = db.Column(
        db.String(100),
        nullable=True
    )

    age = db.Column(
        db.Integer,
        nullable=True
    )

    gender = db.Column(
        db.String(20),
        nullable=True
    )

    mobile = db.Column(
        db.String(20),
        nullable=True
    )

    email = db.Column(
        db.String(100),
        nullable=True
    )

    diabetes = db.Column(
        db.String(10),
        nullable=True
    )

    diabetes_years = db.Column(
        db.Integer,
        nullable=True
    )


# =========================================================
# SYMPTOMS DATABASE MODEL
# =========================================================

class SymptomRecord(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        nullable=False
    )

    blurred_vision = db.Column(
        db.String(10),
        nullable=True
    )

    floaters = db.Column(
        db.String(10),
        nullable=True
    )

    night_vision = db.Column(
        db.String(10),
        nullable=True
    )

    eye_pain = db.Column(
        db.String(10),
        nullable=True
    )

    headache = db.Column(
        db.String(10),
        nullable=True
    )

    blood_sugar_controlled = db.Column(
        db.String(10),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =========================================================
# SCREENING RESULT DATABASE MODEL
# =========================================================

class ScreeningResult(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        nullable=False
    )

    image_path = db.Column(
        db.String(300),
        nullable=False
    )

    prediction = db.Column(
        db.String(200),
        nullable=False
    )

    confidence = db.Column(
        db.Float,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =========================================================
# UPLOAD FOLDER
# =========================================================

UPLOAD_FOLDER = os.path.join(
    "static",
    "uploads"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================================
# HOME / WELCOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session["user_id"] = user.id
            session["username"] = user.username

            print(
                "Login successful:",
                username
            )

            return redirect(
                url_for("patient")
            )

        return "Invalid username or password!"

    return render_template(
        "login.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if not username or not password:

            return (
                "Please enter username and password."
            )

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            return (
                "Username already exists! "
                "Please choose another username."
            )

        hashed_password = generate_password_hash(
            password
        )

        new_user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(
            new_user
        )

        db.session.commit()

        session["user_id"] = new_user.id
        session["username"] = new_user.username

        print(
            "Account created:",
            username
        )

        return redirect(
            url_for("patient")
        )

    return render_template(
        "register.html"
    )


# =========================================================
# PATIENT INFORMATION
# =========================================================

@app.route("/patient", methods=["GET", "POST"])
def patient():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    user = User.query.get(
        session["user_id"]
    )

    if request.method == "POST":

        user.full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        age = request.form.get(
            "age",
            ""
        ).strip()

        if age:
            user.age = int(age)
        else:
            user.age = None

        user.gender = request.form.get(
            "gender",
            ""
        )

        user.mobile = request.form.get(
            "mobile",
            ""
        ).strip()

        user.email = request.form.get(
            "email",
            ""
        ).strip()

        user.diabetes = request.form.get(
            "diabetes",
            ""
        )

        diabetes_years = request.form.get(
            "diabetes_years",
            ""
        ).strip()

        if diabetes_years:
            user.diabetes_years = int(
                diabetes_years
            )
        else:
            user.diabetes_years = None

        db.session.commit()

        print(
            "Patient information saved:",
            user.username
        )

        return redirect(
            url_for("symptoms")
        )

    return render_template(
        "patient.html",
        user=user
    )


# =========================================================
# SYMPTOMS
# =========================================================

@app.route("/symptoms", methods=["GET", "POST"])
def symptoms():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    username = session["username"]

    previous_symptoms = SymptomRecord.query.filter_by(
        username=username
    ).order_by(
        SymptomRecord.id.desc()
    ).first()

    if request.method == "POST":

        symptom = SymptomRecord(

            username=username,

            blurred_vision=request.form.get(
                "blurred_vision"
            ),

            floaters=request.form.get(
                "floaters"
            ),

            night_vision=request.form.get(
                "night_vision"
            ),

            eye_pain=request.form.get(
                "eye_pain"
            ),

            headache=request.form.get(
                "headache"
            ),

            blood_sugar_controlled=request.form.get(
                "blood_sugar_controlled"
            )
        )

        db.session.add(
            symptom
        )

        db.session.commit()

        print(
            "Symptoms saved:",
            username
        )

        return redirect(
            url_for("upload")
        )

    return render_template(
        "symptoms.html",
        symptoms=previous_symptoms
    )


# =========================================================
# UPLOAD PAGE
# =========================================================

@app.route("/upload", methods=["GET", "POST"])
def upload():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    username = session["username"]

    previous_result = ScreeningResult.query.filter_by(
        username=username
    ).order_by(
        ScreeningResult.id.desc()
    ).first()

    previous_image_url = None

    if previous_result:

        saved_path = previous_result.image_path

        saved_path = saved_path.replace(
            "\\",
            "/"
        )

        if saved_path.startswith("static/"):

            saved_path = saved_path[
                len("static/"):
            ]

        previous_image_url = url_for(
            "static",
            filename=saved_path
        )

    return render_template(
        "upload.html",
        previous_result=previous_result,
        previous_image_url=previous_image_url
    )


# =========================================================
# RESULT / IMAGE UPLOAD
# =========================================================

@app.route("/result", methods=["POST"])
def result():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    username = session["username"]

    print(
        "Processing screening for:",
        username
    )

    # -----------------------------------------------------
    # CHECK IMAGE
    # -----------------------------------------------------

    if "image" not in request.files:

        return "No image was selected."

    image = request.files["image"]

    if image.filename == "":

        return "Please select an image."

    # -----------------------------------------------------
    # CREATE FILE NAME
    # -----------------------------------------------------

    extension = os.path.splitext(
        image.filename
    )[1].lower()

    if not extension:
        extension = ".jpg"

    filename = (
        "image_"
        + uuid.uuid4().hex[:8]
        + extension
    )

    # -----------------------------------------------------
    # SAVE IMAGE
    # -----------------------------------------------------

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    image.save(
        filepath
    )

    print(
        "Uploaded image saved:",
        filepath
    )

    # -----------------------------------------------------
    # WEB IMAGE PATH
    # -----------------------------------------------------

    image_relative_path = (
        "uploads/"
        + filename
    )

    image_url = url_for(
        "static",
        filename=image_relative_path
    )

    print(
        "Image URL:",
        image_url
    )

    # =====================================================
    # IMAGE PREPROCESSING
    # =====================================================

    img = Image.open(
        filepath
    ).convert("RGB")

    img = img.resize(
        (224, 224)
    )

    img_array = np.array(
        img
    )

    img_array = img_array / 255.0

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    # =====================================================
    # MODEL PREDICTION
    # =====================================================

    predictions = model.predict(
        img_array,
        verbose=0
    )

    print(
        "Raw prediction:",
        predictions
    )

    predicted_class = np.argmax(
        predictions[0]
    )

    confidence = (
        float(
            np.max(
                predictions[0]
            )
        ) * 100
    )

    # =====================================================
    # CLASS NAMES
    # =====================================================

    class_names = [

        "No Diabetic Retinopathy",

        "Mild Diabetic Retinopathy",

        "Moderate Diabetic Retinopathy",

        "Severe Diabetic Retinopathy",

        "Proliferative Diabetic Retinopathy"

    ]

    prediction = class_names[
        predicted_class
    ]

    # =====================================================
    # SAVE SCREENING RESULT
    # =====================================================

    new_result = ScreeningResult(

        username=username,

        image_path=image_relative_path,

        prediction=prediction,

        confidence=round(
            confidence,
            2
        )
    )

    db.session.add(
        new_result
    )

    db.session.commit()

    print(
        "Screening result saved:",
        username
    )

    # =====================================================
    # RESULT PAGE
    # =====================================================

    return render_template(

        "result.html",

        image_path=image_relative_path,

        image_url=image_url,

        prediction=prediction,

        confidence=round(
            confidence,
            2
        ),

        username=username

    )


# =========================================================
# PREVIOUS RESULT
# =========================================================

@app.route("/previous-result")
def previous_result():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    username = session["username"]

    previous_result = ScreeningResult.query.filter_by(
        username=username
    ).order_by(
        ScreeningResult.id.desc()
    ).first()

    if not previous_result:

        return redirect(
            url_for("upload")
        )

    saved_path = previous_result.image_path

    saved_path = saved_path.replace(
        "\\",
        "/"
    )

    if saved_path.startswith("static/"):

        saved_path = saved_path[
            len("static/"):
        ]

    image_url = url_for(
        "static",
        filename=saved_path
    )

    return render_template(

        "result.html",

        image_path=saved_path,

        image_url=image_url,

        prediction=previous_result.prediction,

        confidence=previous_result.confidence,

        username=username

    )


# =========================================================
# SCREENING HISTORY
# =========================================================

@app.route("/history")
def history():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    username = session["username"]

    user = User.query.get(
        session["user_id"]
    )

    results = ScreeningResult.query.filter_by(
        username=username
    ).order_by(
        ScreeningResult.id.desc()
    ).all()

    symptoms = SymptomRecord.query.filter_by(
        username=username
    ).order_by(
        SymptomRecord.id.desc()
    ).first()

    return render_template(

        "history.html",

        results=results,

        user=user,

        symptoms=symptoms

    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    print(
        "Logout:",
        session.get("username")
    )

    session.clear()

    return redirect(
        url_for("home")
    )


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

with app.app_context():

    db.create_all()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )