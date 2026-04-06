from pathlib import Path
from PIL import Image

imagem = Path("imagens_teste/foto1.png")

if imagem.exists():
    with Image.open(imagem) as img:

        print("arquivo encontrado")

        formato = img.format.upper()

        tamanho_bytes = imagem.stat().st_size
        tamanho_kb = tamanho_bytes / 1024
        largura, altura = img.size

        print(f"formato: {formato}")
        print(f"tamanho: {tamanho_kb:.2f} KB")
        print(f"resolução: {largura} x {altura}")

else:
    print("arquivo não encontrado")


if tamanho_kb <= 500 or largura >= 300 or altura >= 400 or formato == "PNG":
    print("APROVADO")
else:
    print("REPROVADO")

