import cv2
import numpy as np
from PIL import Image

CAMINHO_CLASSIFICADOR = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

def validar_rosto(imagem: Image.Image) -> tuple[bool, str, int]:
    imagem_cinza = imagem.convert("L")
    matriz_imagem = np.array(imagem_cinza)

    classificador = cv2.CascadeClassifier(CAMINHO_CLASSIFICADOR)

    rostos = classificador.detectMultiScale(
        matriz_imagem,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    quantidade_rostos = len(rostos)

    if quantidade_rostos == 1:
        return True, "Um rosto detectado.", quantidade_rostos

    if quantidade_rostos == 0:
        return False, "Nenhum rosto detectado.", quantidade_rostos

    return False, f"Multiplos rostos detectados: {quantidade_rostos}.", quantidade_rostos