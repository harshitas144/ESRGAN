import cv2
import torch
import numpy as np
import streamlit as st
from PIL import Image
import RRDBNet_arch as arch  # Assuming RRDBNet_arch.py defines the model architecture

# Function to load the model
@st.cache_data(persist=False)
def instantiate_model(model_name):
    if model_name:
        if model_name == "ESRGAN model ✅":
            model_path = 'models/RRDB_ESRGAN_x4.pth'
        else:
            model_path = 'models/RRDB_PSNR_x4.pth'

        device = torch.device('cpu')
        model = arch.RRDBNet(3, 3, 64, 23, gc=32)
        model.load_state_dict(torch.load(model_path, map_location=device), strict=True)
        model.eval()
        model = model.to(device)
        print('Model path {:s}. \nModel Loaded successfully...'.format(model_path))
        return model
    else:
        st.warning('⚠ Please choose a model !! ')
        return None

def image_super_resolution(uploaded_image, downloaded_image, model):
    if not model:
        st.error("Please select a model before running super-resolution.")
        return

    device = torch.device('cpu')
    img = cv2.imread(uploaded_image, cv2.IMREAD_COLOR)
    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)
    with torch.no_grad():
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round()
    cv2.imwrite(downloaded_image, output)  # Save the super-resolution image

    # Generate unique filename
    import time
    downloaded_image = f"downloads/super_resolution_{uploaded_image}_{int(time.time())}.png"

def download_success():
    st.balloons()
    st.success('✅ Download Successful !!')

def main():
    """Streamlit app for image super-resolution"""

    model_name = st.selectbox("Select Model:", ("", "ESRGAN model ✅", "RRDB_PSNR_x4.pth"))
    model = instantiate_model(model_name)

    uploaded_file = st.file_uploader("Choose an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        uploaded_image = f"uploads/{uploaded_file.name}"
        with open(uploaded_image, "wb") as f:
            f.write(uploaded_file.getbuffer())

        downloaded_image = f"downloads/super_resolution_{uploaded_file.name}.png"

        if model:
            image_super_resolution(uploaded_image, downloaded_image, model)

            st.download_button(
                label="Download Super-Resolution Image",
                data=open(downloaded_image, 'rb').read(),
                file_name=downloaded_image,
                mime="image/jpeg",
            )
            download_success()

if __name__ == "__main__":
    main()
