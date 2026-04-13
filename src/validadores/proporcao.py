from PIL import Image

PROPORCAO_ESPERADA = 0.750
TOLERANCIA_PROPORCAO = 0.20


def validar_proporcao(imagem: Image.Image) -> tuple[bool, str, float]:
    largura, altura = imagem.size

    proporcao_calculada = largura / altura

    valido = abs(proporcao_calculada - PROPORCAO_ESPERADA) <= TOLERANCIA_PROPORCAO

    if valido:
        return (
            True,
            f"Proporção OK: {largura}x{altura} ({proporcao_calculada:.3f})",
            proporcao_calculada
        )

    return (
        False,
        f"Proporção inválida: {largura}x{altura} ({proporcao_calculada:.3f})",
        proporcao_calculada
    )