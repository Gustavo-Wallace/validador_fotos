from PIL import Image

def validar_imagem_colorida(imagem: Image.Image) -> tuple[bool, str]:

    modo_original = imagem.mode

    if modo_original == "L":
        return False, f"Imagem em escala cinza (modo {modo_original})"
    
    imagem_rgb = imagem.convert("RGB")

    pixels = imagem_rgb.getdata()

    for r, g, b in pixels:
        if r != g or g != b:
            return True, f"Imagem colorida (modo original: {modo_original})"
    
    return False, f"Imagem sem cores detectáveis (modo original: {modo_original})"