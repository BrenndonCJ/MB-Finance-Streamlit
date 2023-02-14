import streamlit as st
from PIL import Image
import cv2
from pathlib import Path
import os
import numpy as np

from models import load_RNASR


def apply_super_resolution(img):
    img = np.array(img.convert('RGB'))

    # dir = Path(__file__).resolve().parent
    # dir = os.path.join(dir, 'ESPCN_X4.pb')

    # sr = cv2.dnn_superres.DnnSuperResImpl_create()
    # sr.readModel(dir)
    # sr.setModel("espcn",4)

    sr = load_RNASR()
    img = sr.upsample(img)


    cv2.imwrite("temp.png", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    img = Image.fromarray(img, "RGB")
    return img


st.set_page_config(
         page_icon="",
         page_title="Super Resolução",
         layout="wide",
         initial_sidebar_state="expanded"
)

st.title('Aplicar Super Resolução')

img = st.file_uploader(label="Selecione uma foto", type=['jpg', 'png', 'gif'])

j1, j2, j3 = st.columns([1,2,1])

with j2:
    if img:
        img = Image.open(img)
        if img.size[0] <= 1920 and img.size[1] <= 1080:
            st.image(img, caption=img.size)

            if st.button(label="Aplicar"):
                with st.spinner('Wait for it...'):
                    new_img = apply_super_resolution(img)

                imagem = open("temp.png", "rb")

                st.image('temp.png', caption=new_img.size)

                btn = st.download_button(
                label="Download image",
                data=imagem,
                mime="image/png"
                )
        else:
            st.error("Carregue uma imagem com domensões maximas de 1920x1080")