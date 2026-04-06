from pathlib import Path
from PIL import Image

TAMANHO_MAXIMO_KB = 500
FORMATOS_PERMITIDOS = {"JPEG", "JPG", "PNG"}
LARGURA_MINIMA = 300
ALTURA_MINIMA = 400


def validar_tamanho_arquivo(caminho_imagem: Path) -> tuple[bool, str]:
    tamanho_bytes = caminho_imagem.stat().st_size
    tamanho_kb = tamanho_bytes / 1024

    if tamanho_kb <= TAMANHO_MAXIMO_KB:
        return True, f"Tamanho OK: {tamanho_kb:.2f} KB"
    return False, f"Tamanho excedido: {tamanho_kb:.2f} KB"


def validar_formato(imagem: Image.Image) -> tuple[bool, str]:
    formato = imagem.format.upper() if imagem.format else "DESCONHECIDO"

    if formato in FORMATOS_PERMITIDOS:
        return True, f"Formato OK: {formato}"
    return False, f"Formato inválido: {formato}"


def validar_resolucao(imagem: Image.Image) -> tuple[bool, str]:
    largura, altura = imagem.size

    if largura >= LARGURA_MINIMA and altura >= ALTURA_MINIMA:
        return True, f"Resolução OK: {largura}x{altura}"
    return False, f"Resolução insuficiente: {largura}x{altura}"


def validar_imagem(caminho_arquivo: str) -> None:
    caminho_imagem = Path(caminho_arquivo)

    if not caminho_imagem.exists():
        print("Arquivo não encontrado.")
        return

    try:
        with Image.open(caminho_imagem) as imagem:
            print(f"Analisando arquivo: {caminho_imagem.name}")
            print("-" * 40)

            resultado_tamanho, msg_tamanho = validar_tamanho_arquivo(caminho_imagem)
            resultado_formato, msg_formato = validar_formato(imagem)
            resultado_resolucao, msg_resolucao = validar_resolucao(imagem)

            print(msg_tamanho)
            print(msg_formato)
            print(msg_resolucao)

            if resultado_tamanho and resultado_formato and resultado_resolucao:
                print("\nStatus final: APROVADA nas validações iniciais")
            else:
                print("\nStatus final: REPROVADA nas validações iniciais")

    except Exception as erro:
        print(f"Erro ao abrir/processar a imagem: {erro}")


if __name__ == "__main__":
    validar_imagem("imagens_teste/foto1.png")