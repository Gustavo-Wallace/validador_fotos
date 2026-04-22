import cv2
import numpy as np
from PIL import Image
import os

CAMINHO_CLASSIFICADOR = os.path.join(
    cv2.data.haarcascades,
    "haarcascade_frontalface_default.xml"
)

AREA_MINIMA_ROSTO = 0.12
TOLERANCIA_CENTRO_X = 0.20
TOLERANCIA_CENTRO_Y = 0.20

def validar_enquadramento_rosto(imagem: Image.Image) -> tuple[bool, str, dict]:
    imagem_cinza = imagem.convert("L")
    matriz_imagem = np.array(imagem_cinza)

    classificador = cv2.CascadeClassifier(CAMINHO_CLASSIFICADOR)

    if classificador.empty():
        return False, "Erro ao carregar classificador facial.", {}

    rostos = classificador.detectMultiScale(
        matriz_imagem,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    quantidade_rostos = len(rostos)

    if quantidade_rostos == 0:
        return False, "Nenhum rosto detectado para análise de enquadramento.", {}
    
    if quantidade_rostos > 1:
        return False, "Mais de um rosto detectado para análise de enquadramento.", {}
    
    x, y, w, h = rostos[0]

    largura_imagem, altura_imagem = imagem.size
    area_imagem = largura_imagem * altura_imagem
    area_rosto = w * h
    proporcao_area_rosto = area_rosto / area_imagem

    centro_rosto_x = x + (w / 2)
    centro_rosto_y = y + (h / 2)

    centro_imagem_x = largura_imagem / 2
    centro_imagem_y = altura_imagem / 2

    desvio_x = abs(centro_rosto_x - centro_imagem_x) / largura_imagem
    desvio_y = abs(centro_rosto_y - centro_imagem_y) / altura_imagem

    area_valida = proporcao_area_rosto >= AREA_MINIMA_ROSTO
    centro_x_valido = desvio_x <= TOLERANCIA_CENTRO_X
    centro_y_valido = desvio_y <= TOLERANCIA_CENTRO_Y

    enquadramento_valido = area_valida and centro_x_valido and centro_y_valido

    detalhes = {
        "quantidade_rostos": quantidade_rostos,
        "area_rosto": area_rosto,
        "proporcao_area_rosto": round(proporcao_area_rosto, 3),
        "desvio_x": round(desvio_x, 3),
        "desvio_y": round(desvio_y, 3),
        "retangulo_rosto": {
            "x": int(x),
            "y": int(y),
            "w": int(w),
            "h": int(h)
        }
    }

    if enquadramento_valido:
        return True, "Enquadramento do rosto OK.", detalhes

    motivos = []

    if not area_valida:
        motivos.append("rosto muito pequeno na imagem")

    if not centro_x_valido:
        motivos.append("rosto muito deslocado horizontalmente")

    if not centro_y_valido:
        motivos.append("rosto muito deslocado verticalmente")

    return False, f"Enquadramento inválido: {', '.join(motivos)}.", detalhes