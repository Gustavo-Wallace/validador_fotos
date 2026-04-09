from pathlib import Path

TAMANHO_MAXIMO_KB = 500

def validar_tamanho_arquivo(caminho_imagem: Path):
    tamanho_bytes = caminho_imagem.stat().st_size
    tamanho_kb = tamanho_bytes / 1024

    valido = tamanho_kb <= TAMANHO_MAXIMO_KB
    
    mensagem = f"Tamanho {'OK' if valido else 'excedido'}: {tamanho_kb:.2f} KB"

    return valido, mensagem, tamanho_kb