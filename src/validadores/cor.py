from PIL import Image

TOLERANCIA_COR = 10

def validar_imagem_colorida(imagem: Image.Image) -> tuple[bool, str]:
    modo_original = imagem.mode

    if modo_original == "L":
        return False, f"Imagem em escala de cinza (modo {modo_original})"

    imagem_rgb = imagem.convert("RGB")
    pixels = imagem_rgb.getdata()

    for r, g, b in pixels:
        diferenca_rg = abs(r - g)
        diferenca_rb = abs(r - b)
        diferenca_gb = abs(g - b)

        if (
            diferenca_rg > TOLERANCIA_COR
            or diferenca_rb > TOLERANCIA_COR
            or diferenca_gb > TOLERANCIA_COR
        ):
            return True, (
                f"Imagem colorida "
                f"(modo original: {modo_original}, tolerância: {TOLERANCIA_COR})"
            )

    return False, (
        f"Imagem sem cores detectáveis "
        f"(modo original: {modo_original}, tolerância: {TOLERANCIA_COR})"
    )