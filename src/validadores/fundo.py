from PIL import Image

TAMANHO_BORDA_PERCENTUAL = 0.18

def validar_fundo(imagem: Image.Image) -> tuple[bool, str, float]:
    imagem_rgb = imagem.convert("RGB")

    largura, altura = imagem_rgb.size

    borda_x = int(largura * TAMANHO_BORDA_PERCENTUAL)
    borda_y = int(altura * TAMANHO_BORDA_PERCENTUAL)

    