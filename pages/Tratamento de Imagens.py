import streamlit as st
from PIL import Image
import cv2
from pathlib import Path
import os
import numpy as np
from rembg import remove

from models import load_RNASR


def apply_super_resolution(img):
    img = np.array(img.convert('RGBA'))

    # dir = Path(__file__).resolve().parent
    # dir = os.path.join(dir, 'ESPCN_X4.pb')

    # sr = cv2.dnn_superres.DnnSuperResImpl_create()
    # sr.readModel(dir)
    # sr.setModel("espcn",4)

    sr = load_RNASR()
    img = sr.upsample(img)
    cv2.imwrite("temp.png", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    img = Image.fromarray(img, "RGBA")
    return img


def bg_mask(img, mask=False):
    # img = np.array(img)
    output_img = remove(
        img,
        alpha_matting = False,
        alpha_matting_foreground_threshold = 240,
        alpha_matting_background_threshold = 10,
        alpha_matting_erode_size = 10,
        only_mask=mask,
        post_process_mask=False,
    )
    # output_img = Image.fromarray(img)
    return output_img


st.set_page_config(
         page_icon="",
         page_title="Tratamento de Imagens",
         layout="wide",
         initial_sidebar_state="expanded"
)

st.title('Aplicar Tratamentos de Imagem')

paginas = st.tabs(["Super Resolução","Remover Fundo/BG"])

with paginas[0]:
    st.title('Aplicar Super Resolução')

    img = st.file_uploader(label="Selecione uma foto", type=['jpg', 'png', 'gif', 'jpeg'], key='super_resolucao')

    j1, j2, j3 = st.columns([1,2,1])

    with j2:
        if img:
            img = Image.open(img)
            if img.size[0] <= 1920 and img.size[1] <= 1920:
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

with paginas[1]:
    st.title('Remover Fundo / Background')

    img = st.file_uploader(label="Selecione uma foto", type=['jpg', 'png', 'gif', 'jpeg'], key='remover_fundo')

    if img:
        img = Image.open(img).convert("RGBA")

        st.image(img, caption=img.size)

        bgmask = st.radio("Selecione uma opção", options=['Remover Fundo','Criar mascara'])
        
        if st.button(label="Aplicar", key="bt_remove"):
            
            if bgmask == 'Remover Fundo':
                with st.spinner('Wait for it...'):
                    img = bg_mask(img)
            else:
                with st.spinner('Wait for it...'):
                    img = bg_mask(img, True)
                
            st.image(img, caption=img.size)

            # st.download_button(
            #         label="Download image",
            #         data=img,
            #         mime="image/png"
            #         )
