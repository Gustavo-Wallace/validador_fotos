from PIL import Image

LARGURA_MINIMA = 300
ALTURA_MINIMA = 400

def validar_resolucao(imagem: Image.Image):
    largura, altura = imagem.size

    valido = largura >= LARGURA_MINIMA and altura >= ALTURA_MINIMA

    mensagem = f"Resolução {'OK' if valido else 'insuficiente'}: {largura}x{altura}"
    
    return valido, mensagem, largura, altura