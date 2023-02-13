import streamlit as st
from PIL import Image
import cv2
from pathlib import Path
import os
import numpy as np


def apply_super_resolution(img):
    img = Image.open(img)
    img = np.array(img.convert('RGB'))

    dir = Path(__file__).resolve().parent
    dir = os.path.join(dir, 'ESPCN_X4.pb')

    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(dir)
    sr.setModel("espcn",4)

    img = sr.upsample(img)

    cv2.imwrite("temp.png", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    img = Image.fromarray(img, "RGB")
    return img


st.title('Aplicar Super Reolução')

img = st.file_uploader(label="Selecione uma foto")

j1, j2, j3 = st.columns([1,2,1])

with j2:
    if img:
        st.image(img)

        if st.button(label="Aplicar"):
            with st.spinner('Wait for it...'):
                new_img = apply_super_resolution(img)

            imagem = open("temp.png", "rb")

            st.image('temp.png')

            btn = st.download_button(
            label="Download image",
            data=imagem,
            mime="image/png"
            )