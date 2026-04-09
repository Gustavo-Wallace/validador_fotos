from PIL import Image

FORMATOS_PERMITIDOS = {"JPEG", "JPG", "PNG"}

def validar_formato(imagem: Image.Image):
    formato = imagem.format.upper() if imagem.format else "DESCONHECIDO"

    valido = formato in FORMATOS_PERMITIDOS

    mensagem = f"Formato {'OK' if valido else 'inválido'}: {formato}"

    return valido, mensagem, formato