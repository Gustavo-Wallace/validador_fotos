from pathlib import Path
from PIL import Image, ImageOps
from dataclasses import asdict
import json

from src.models.resultado_validacao import ResultadoValidacao
from src.validadores.tamanho import validar_tamanho_arquivo
from src.validadores.formato import validar_formato
from src.validadores.resolucao import validar_resolucao
from src.validadores.proporcao import validar_proporcao
from src.validadores.cor import validar_imagem_colorida
from src.validadores.nitidez import validar_nitidez

from src.validadores.exif import ler_metadados_exif


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
        
        exif = ler_metadados_exif(imagem)

        # orientação correta antes das validações
        imagem_corrigida = ImageOps.exif_transpose(imagem)

        tamanho_valido, msg_tamanho, tamanho_kb = validar_tamanho_arquivo(caminho_imagem)
        formato_valido, msg_formato, formato = validar_formato(imagem)
        resolucao_valida, msg_resolucao, largura, altura = validar_resolucao(imagem_corrigida)
        proporcao_valida, msg_proporcao, proporcao_calculada = validar_proporcao(imagem_corrigida)
        cor_valida, msg_cor = validar_imagem_colorida(imagem_corrigida)
        nitifez_valida, msg_nitidez, valor_nitidez = validar_nitidez(imagem_corrigida)

        validacoes = {
            "tamanho": tamanho_valido,
            "formato": formato_valido,
            "resolucao": resolucao_valida,
            "proporcao": proporcao_valida,
            "colorida": cor_valida,
            "nitidez": nitifez_valida
        }

        mensagens = [
            msg_tamanho,
            msg_formato,
            msg_resolucao,
            msg_proporcao,
            msg_cor,
            msg_nitidez
        ]

        status = "APROVADO" if all(validacoes.values()) else "REPROVADO"

        detalhes = {
            "tamanho_kb": round(tamanho_kb, 2),
            "formato": formato,
            "largura": largura,
            "altura": altura,
            "proporcao_calculada": round(proporcao_calculada, 3),
            "nitidez_calculada": round(valor_nitidez, 2),

            "exif": exif
        }

        return ResultadoValidacao(
            arquivo=caminho_imagem.name,
            status=status,
            validacoes=validacoes,
            detalhes=detalhes,
            mensagens=mensagens
        )


if __name__ == "__main__":
    caminho_imagem = Path(__file__).parent.parent / "imagens_teste" / "image.png"

    resultado = validar_imagem(str(caminho_imagem))

    print(json.dumps(asdict(resultado), indent=4, ensure_ascii=False, default=str))