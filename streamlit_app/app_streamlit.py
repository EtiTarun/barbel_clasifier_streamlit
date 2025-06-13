# app_streamlit.py
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Barbell Classifier", layout="centered")



from streamlit_lottie import st_lottie
import requests
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Load model once
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("model/barbell_model.h5")

model = load_model()
import json
import os

# Load class names based on training order
def load_class_names(model_path):
    # Get class names from training
    class_indices = model.get_layer(index=0).input_shape
    return list(train_data.class_indices.keys())  # ❌ this won't work here since `train_data` isn't available

# ✅ Better solution:
# Save class_names list during training:
with open("model/class_names.json", "r") as f:
    class_names = json.load(f)


# Menu options

# Use sidebar with styled option menu
with st.sidebar:
    menu = option_menu(
        "Navigation",  # Title
        ["🏠 Home", "📂 Proceed", "📄 Abstract", "❓ Help"],  # Options
        icons=["house", "cloud-upload", "file-earmark-text", "question-circle"],  # Bootstrap icons
        menu_icon="cast",  
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#0f1117"},
            "icon": {"color": "white", "font-size": "20px"}, 
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "color": "white",
                "padding": "10px 15px",
            },
            "nav-link-selected": {
                "background-color":	"#FF4B4B",  # 🔴 Red highlight
                "color": "white",
                "font-weight": "bold",
                "box-shadow": "0 0 10px rgba(255,75,75,0.4)"
            },
        }
    )


# Home Page
if menu == "🏠 Home":
    st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
                    url("https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translateY(-20px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}
    .custom-title {{
        font-size: 3rem;
        font-weight: 900;
        color: #FFD700;
        text-align: center;
        text-shadow: 3px 3px 10px black;
        margin-top: 3rem;
        animation: fadeIn 1.5s ease-out;
    }}
    .custom-desc {{
        max-width: 800px;
        margin: 2rem auto;
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        color: #f0f0f0;
        font-size: 1.2rem;
        line-height: 1.7;
        text-align: center;
        backdrop-filter: blur(8px);
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
        animation: fadeIn 2s ease-in;
    }}
    </style>

    <div class="custom-title">
        🏋️ Barbell Exercise Classifier
    </div>
    <div class="custom-desc">
        Welcome to the Barbell Exercise Classifier!<br><br>
        Upload an image of a barbell workout, and let our AI predict the exercise type with precision.<br><br>
        📁 Use the sidebar to explore app features like Help, Abstract, and Image Upload.
    </div>
    """,
    unsafe_allow_html=True
)


    def load_lottie_url(url: str):
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        except Exception as e:
            st.error(f"Failed to load Lottie animation: {e}")
            return None

        # Load Lottie animation
    def load_lottie_url(url: str):
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        except Exception as e:
            st.error(f"Failed to load Lottie animation: {e}")
            return None

    # URL for your animation
    lottie_url = "https://lottie.host/ded5da16-8e1a-4bbd-af94-cf8b9bbcc136/rratSq8W25.json"
    lottie_json = load_lottie_url(lottie_url)

    # Inject CSS to remove grey background and center the animation
    st.markdown(
        """
        <style>
        .lottie-container {
            display: flex;
            justify-content: center;
            align-items: center;
            background: transparent !important;
            padding: 0;
            margin: 0;
        }
        iframe {
            background: transparent !important;
        }
        </style>
        <div class="lottie-container">
        """,
        unsafe_allow_html=True
    )

    # Display Lottie animation
    if lottie_json:
        st_lottie(
            lottie_json,
            speed=1,
            reverse=False,
            loop=True,
            quality="high",
            height=300,
            width=300,
        )
    else:
        st.warning("⚠️ Could not load animation. Try again later.")

    # Close the styled div
    st.markdown("</div>", unsafe_allow_html=True)


# Proceed: Upload & Predict
elif menu == "📂 Proceed":
    import hashlib

    # Load or create user database
    USER_DB = "users.json"
    if not os.path.exists(USER_DB):
        with open(USER_DB, "w") as f:
            json.dump({}, f)

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users():
        with open(USER_DB, "r") as f:
            return json.load(f)

    def save_users(users):
        with open(USER_DB, "w") as f:
            json.dump(users, f)

    def authenticate_user(username, password):
        users = load_users()
        hashed_pw = hash_password(password)
        return users.get(username) == hashed_pw

    def create_user(username, password):
        users = load_users()
        if username in users:
            return False
        users[username] = hash_password(password)
        save_users(users)
        return True

    # SESSION STATE
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = ""

    st.title("📤 Barbell Classifier - User Login")

    if not st.session_state.logged_in:
        # Track the last option
        if "last_auth_option" not in st.session_state:
            st.session_state.last_auth_option = "🔑 Login"

        # Radio to choose between login and create account
        option = st.radio("Choose an option:", ["🔑 Login", "🆕 Create Account"], key="auth_option")

        # Clear input fields when option changes
        if st.session_state.auth_option != st.session_state.last_auth_option:
            st.session_state.username = ""
            st.session_state.password = ""
            st.session_state.last_auth_option = st.session_state.auth_option

        # Username and password fields
        username = st.text_input("Username", key="username")
        password = st.text_input("Password", type="password", key="password")

        if option == "🔑 Login":
            if st.button("Login"):
                if authenticate_user(username, password):
                    st.success("✅ Login successful!")
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials.")

        elif option == "🆕 Create Account":
            if st.button("Create Account"):
                if create_user(username, password):
                    st.success("✅ Account created successfully. Please login.")
                else:
                    st.warning("⚠️ Username already exists.")

    else:
        st.subheader(f"👋 Welcome, {st.session_state.current_user}")
        uploaded_file = st.file_uploader("Upload a barbell exercise image", type=["jpg", "jpeg", "png"])
        
        if uploaded_file:
            img = Image.open(uploaded_file).convert("RGB")
            st.image(img, caption="🖼️ Uploaded Image", use_container_width=True)

            img_for_model = img.resize((128, 128), resample=Image.BICUBIC)
            img_array = image.img_to_array(img_for_model)
            img_array = np.expand_dims(img_array, axis=0) / 255.0

            predictions = model.predict(img_array)
            predicted_class = class_names[np.argmax(predictions)]
            confidence = np.max(predictions)

            st.success(f"✅ Prediction: **{predicted_class.replace('_', ' ').title()}**")
            st.info(f"🔍 Confidence: **{confidence * 100:.2f}%**")
            st.bar_chart({class_names[i]: float(predictions[0][i]) for i in range(len(class_names))})

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.rerun()
            
        st.markdown("---")
        st.subheader("🗑️ Delete Account")

        with st.expander("⚠️ Delete your account permanently"):
            st.warning("This will permanently delete your account. This action cannot be undone.")
            confirm_username = st.text_input("Confirm Username", key="confirm_user")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_pass")

            if st.button("Delete Account"):
                if confirm_username == st.session_state.current_user:
                    if authenticate_user(confirm_username, confirm_password):
                        users = load_users()
                        users.pop(confirm_username, None)
                        save_users(users)
                        st.success("✅ Your account has been deleted.")
                        st.session_state.logged_in = False
                        st.session_state.current_user = ""
                        st.rerun()
                    else:
                        st.error("❌ Incorrect password.")
                else:
                    st.error("❌ Username mismatch.")




# Abstract
elif menu == "📄 Abstract":
    st.title("📑 Project Abstract")
    st.markdown("""
    ### Barbell Exercise Image Classifier using CNN
    This project aims to classify barbell exercises such as:
    - Bench Press  
    - Squat  
    - Deadlift  
    - Barbell Biceps Curl  
    - Shoulder Press  

    #### 🛠️ Workflow:
    - Downloaded and labeled barbell images using GoogleImageCrawler.
    - Preprocessed and split dataset using `split_dataset.py`.
    - Built and trained a custom CNN model using TensorFlow/Keras.
    - Deployed an interactive UI with Streamlit for image-based classification.

    **Objective**: To automate the recognition of gym exercises from static images for fitness tracking or gym management systems.
    """)

# Help
elif menu == "❓ Help":
    st.title("🆘 Help & Instructions")
    st.markdown("""
    - Go to **Proceed** to upload a barbell exercise image.
    - Supported formats: `.jpg`, `.jpeg`, `.png`.
    - You’ll get the predicted class and a confidence score.
    
    **Need more help?**  
    Contact: [Tarun Eti](mailto:your.email@example.com)
    """)
