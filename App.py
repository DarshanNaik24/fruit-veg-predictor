import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image


# Set background image with blur and transparency using CSS
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://static.vecteezy.com/system/resources/thumbnails/034/084/993/small_2x/artistic-frame-of-fruits-and-vegetables-on-a-radiant-white-background-ai-generated-photo.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            backdrop-filter: blur(8px);
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.6); /* Adjust transparency */
            z-index: -1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_url()

# Tensorflow Model Prediction
def model_prediction(test_image):
    model = tf.keras.models.load_model("trained_model.h5")
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(64, 64))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions)  # return index of max element

# Sidebar
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About Project", "Prediction"])

# Main Page
if app_mode == "Home":
    st.header("FRUITS & VEGETABLES RECOGNITION SYSTEM")
    image_path = "full-frame-shot-multi-colored-fruits_1048944-957246.jpg"
    st.image(image_path)

# About Project
elif app_mode == "About Project":
    st.header("About Project")
    st.subheader("About Dataset")
    st.text("This dataset contains images of the following food items:")
    st.code("fruits - banana, apple, pear, grapes, orange, kiwi, watermelon, pomegranate, pineapple, mango.")
    st.code("vegetables - cucumber, carrot, capsicum, onion, potato, lemon, tomato, raddish, beetroot, cabbage, lettuce, spinach, soy bean, cauliflower, bell pepper, chilli pepper, turnip, corn, sweetcorn, sweet potato, paprika, jalepeño, ginger, garlic, peas, eggplant.")
    st.subheader("Content")
    st.text("This dataset contains three folders:")
    st.text("1. train (100 images each)")
    st.text("2. test (10 images each)")
    st.text("3. validation (10 images each)")

# Prediction Page
elif app_mode == "Prediction":
    st.header("Model Prediction")
    test_image = st.file_uploader("Choose an Image:")

    if test_image is not None:
        # Display image when either button is clicked
        if st.button("Show Image") or st.button("Predict"):
            # Convert to PIL Image
            try:
                image = Image.open(test_image)
                st.image(image, use_column_width=True)

                # If Predict button was clicked
                if st.button._last_clicked == "Predict":
                    st.snow()
                    st.write("Our Prediction")
                    result_index = model_prediction(test_image)

                    # Reading Labels
                    with open("labels.txt") as f:
                        content = f.readlines()
                    label = [i.strip() for i in content]
                    st.success('Model is Predicting it\'s a "{}"'.format(label[result_index]))

            except Exception as e:
                st.error(f"Error processing image: {str(e)}")

