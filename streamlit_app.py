import os
import streamlit as st
from PIL import Image
from app_funcs import *

st.set_page_config(
    page_title="ISR using ESRGAN",
    page_icon="",
    layout="centered",
    initial_sidebar_state="auto",
)

upload_path = "uploads/"
download_path = "downloads/"

main_image = Image.open('static/main_banner.png')

st.image(main_image, use_column_width='auto')
st.title("✨ ISR using ESRGAN ")

model_name = st.radio("Choose Model for Image Super Resolution", ('ESRGAN model ✅', 'PSNR-oriented model ✅'))
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.info('✨ Supports all popular image formats  - PNG, JPG, BMP ')

# Specify paths to the four images
image_paths = [
    "/home/lenovo/Streamlit-based-Image-Super-Resolution-using-ESRGAN/uploads/baboon.png",
    "/home/lenovo/Streamlit-based-Image-Super-Resolution-using-ESRGAN/uploads/2.jpeg",
    "/home/lenovo/Streamlit-based-Image-Super-Resolution-using-ESRGAN/uploads/1.bmp",
    "/home/lenovo/Streamlit-based-Image-Super-Resolution-using-ESRGAN/uploads/comic.png"
]

# Display the images side by side
col1, col2, col3, col4 = st.columns(4)
with col1:
    image1 = Image.open(image_paths[0])
    st.image(image1, caption='Image 1', use_column_width=True)

with col2:
    image2 = Image.open(image_paths[1])
    st.image(image2, caption='Image 2', use_column_width=True)

with col3:
    image3 = Image.open(image_paths[2])
    st.image(image3, caption='Image 3', use_column_width=True)

with col4:
    image4 = Image.open(image_paths[3])
    st.image(image4, caption='Image 4', use_column_width=True)

# Capture selected image for super-resolution
selected_image_index = st.selectbox("Select Image for Super-Resolution", range(len(image_paths)))
selected_image_path = image_paths[selected_image_index]

# Proceed with super-resolution
if st.button("Run Super-Resolution"):
    with st.spinner(f"Working... "):
        uploaded_image = selected_image_path
        downloaded_image = os.path.abspath(os.path.join(download_path, f"output_image_{selected_image_index}.png"))

        # Open the uploaded image for display
        uploaded_image_obj = Image.open(uploaded_image)
        st.subheader("**Uploaded Image**")
        st.image(uploaded_image_obj, caption='This is your uploaded image.')

        model = instantiate_model(model_name)
        image_super_resolution(uploaded_image, downloaded_image, model)

        # Display the super-resolved image
        final_image = Image.open(downloaded_image)
        st.markdown("---")
        st.subheader("**Super-Resolved Image**")
        st.image(final_image, caption='This is how your final image looks like ')

        # Download the super-resolved image
        with open(downloaded_image, "rb") as file:
            if downloaded_image.endswith('.jpg'):
                if st.download_button(
                        label="Download Output Image ",
                        data=file,
                        file_name=f"output_image_{selected_image_index}.jpg",
                        mime='image/jpg'
                ):
                    download_success()

            elif downloaded_image.endswith('.jpeg'):
                if st.download_button(
                        label="Download Output Image ",
                        data=file,
                        file_name=f"output_image_{selected_image_index}.jpeg",
                        mime='image/jpeg'
                ):
                    download_success()

            elif downloaded_image.endswith('.png'):
                if st.download_button(
                        label="Download Output Image ",
                        data=file,
                        file_name=f"output_image_{selected_image_index}.png",
                        mime='image/png'
                ):
                    download_success()

            elif downloaded_image.endswith('.bmp'):
                if st.download_button(
                        label="Download Output Image ",
                        data=file,
                        file_name=f"output_image_{selected_image_index}.bmp",
                        mime='image/bmp'
                ):
                    download_success()

