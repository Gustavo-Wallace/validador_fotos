from pathlib import Path
from PIL import Image
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
import json


TAMANHO_MAXIMO_KB = 500
FORMATOS_PERMITIDOS = {"JPEG", "JPG", "PNG"}
LARGURA_MINIMA = 300
ALTURA_MINIMA = 400

@dataclass
class ResultadoValidacao:
    arquivo: str
    status: str
    validacoes: Dict[str, bool]
    detalhes: Dict[str, Optional[float]]
    mensagens: List[str] = field(default_factory=list)


def validar_tamanho_arquivo(caminho_imagem: Path):
    tamanho_bytes = caminho_imagem.stat().st_size
    tamanho_kb = tamanho_bytes / 1024

    valido = tamanho_kb <= TAMANHO_MAXIMO_KB

    mensagem = f"Tamanho {'OK' if valido else 'excedido'}: {tamanho_kb:.2f} KB"
    return valido, mensagem, tamanho_kb



def validar_formato(imagem: Image.Image):
    formato = imagem.format.upper() if imagem.format else "DESCONHECIDO"

    valido = formato in FORMATOS_PERMITIDOS

    mensagem = f"Formato {'OK' if valido else 'inválido'}: {formato}"
    return valido, mensagem, formato


def validar_resolucao(imagem: Image.Image):
    largura, altura = imagem.size

    valido = largura >= LARGURA_MINIMA and altura >= ALTURA_MINIMA

    mensagem = f"Resolução {'OK' if valido else 'insuficiente'}: {largura}x{altura}"
    return valido, mensagem, largura, altura


def validar_imagem(caminho_arquivo: str) -> ResultadoValidacao:
    caminho_imagem = Path(caminho_arquivo)

    if not caminho_imagem.exists():
        return ResultadoValidacao(
            arquivo=caminho_imagem.name,
            status="ERRO",
            validacoes={},
            detalhes={},
            mensagens=["Arquivo não encontrado."]
        )

    with Image.open(caminho_imagem) as imagem:
        tamanho_valido, msg_tamanho, tamanho_kb = validar_tamanho_arquivo(caminho_imagem)
        formato_valido, msg_formato, formato = validar_formato(imagem)
        resolucao_valida, msg_resolucao, largura, altura = validar_resolucao(imagem)

        validacoes = {
            "tamanho": tamanho_valido,
            "formato": formato_valido,
            "resolucao": resolucao_valida
        }

        mensagens = [msg_tamanho, msg_formato, msg_resolucao]

        status = "APROVADO" if all(validacoes.values()) else "REPROVADO"

        detalhes = {
            "tamanho_kb": round(tamanho_kb, 2),
            "formato": formato,
            "largura": largura,
            "altura": altura
        }

        return ResultadoValidacao(
            arquivo=caminho_imagem.name,
            status=status,
            validacoes=validacoes,
            detalhes=detalhes,
            mensagens=mensagens
        )


if __name__ == "__main__":
    resultado = validar_imagem("../imagens_teste/foto1.png")
    print(json.dumps(asdict(resultado), indent=4, ensure_ascii=False))