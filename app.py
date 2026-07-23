

import streamlit as st
import easyocr
from PIL import Image
import cv2
import numpy as np

# Blur Detection Function
def detect_blur(image):
    img = np.array(image)

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2GRAY
    )

    score = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    return score


st.title("AI Document Verification System")

uploaded_file = st.file_uploader(
    "Upload Aadhaar, PAN or Passport"
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image)

    # Image Quality Check
    blur_score = detect_blur(image)

    st.subheader("Image Quality")

    st.write("Blur Score:", round(blur_score, 2))

    if blur_score < 100:
        st.error("Blurry Document")
    else:
        st.success("Clear Document")

    try:

        st.subheader("OCR Status")

        st.write("Loading OCR model...")

        reader = easyocr.Reader(['en'])

        st.write("OCR model loaded")

        st.write("Extracting text...")

        result = reader.readtext(
            np.array(image),
            detail=0
        )

        st.write("Text extraction complete")

        extracted_text = " ".join(result)

        st.subheader("Extracted Text")

        if extracted_text.strip() == "":
            st.warning("No text detected in the image.")
        else:
            st.write(extracted_text)

        # Document Statistics
        word_count = len(extracted_text.split())

        st.subheader("Document Statistics")
        st.write("Total Words:", word_count)

        # Document Classification
        text = extracted_text.lower()

        document_type = "Unknown Document"

        if "aadhaar" in text:
            document_type = "Aadhaar Card"

        elif "income tax department" in text:
            document_type = "PAN Card"

        elif "passport" in text:
            document_type = "Passport"

        st.subheader("Document Type")
        st.success(document_type)

    except Exception as e:
        st.error(f"OCR Error: {e}")