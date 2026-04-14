import cv2
import numpy as np
from PIL import Image

LIMIAR_NITIDEZ = 350.0

def validar_nitidez(imagem: Image.Image) -> tuple[bool, str, float]:
    imagem_cinza = imagem.convert("L")

    matriz_imagem = np.array(imagem_cinza)

    variancia_laplaciano = cv2.Laplacian(matriz_imagem, cv2.CV_64F).var()

    valido = variancia_laplaciano >= LIMIAR_NITIDEZ

    if valido:
        return (
            True,
            f"Nitidez OK: {variancia_laplaciano:.2f}",
            variancia_laplaciano
        )
    
    return (
        False,
        f"Nitidez insuficiente: {variancia_laplaciano:.2f}",
        variancia_laplaciano
    )