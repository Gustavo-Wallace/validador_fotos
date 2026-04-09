from pathlib import Path
from PIL import Image
from dataclasses import asdict
import json

from src.models.resultado_validacao import ResultadoValidacao
from src.validadores.tamanho import validar_tamanho_arquivo
from src.validadores.formato import validar_formato
from src.validadores.resolucao import validar_resolucao
from src.validadores.cor import validar_imagem_colorida


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
        cor_valida, msg_cor = validar_imagem_colorida(imagem)

        validacoes = {
            "tamanho": tamanho_valido,
            "formato": formato_valido,
            "resolucao": resolucao_valida,
            "colorida": cor_valida
        }

        mensagens = [msg_tamanho, msg_formato, msg_resolucao, msg_cor]

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
    caminho_imagem = Path(__file__).parent.parent / "imagens_teste" / "foto1_pb.png"

    resultado = validar_imagem(str(caminho_imagem))

    print(json.dumps(asdict(resultado), indent=4, ensure_ascii=False))