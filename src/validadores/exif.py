from PIL import Image, ExifTags


def ler_metadados_exif(imagem: Image.Image) -> dict:
    exif = imagem.getexif()

    if not exif:
        return {"aviso": "Imagem sem metadados EXIF."}

    metadados = {}

    for tag_id, valor in exif.items():
        nome_tag = ExifTags.TAGS.get(tag_id, f"TAG_{tag_id}")
        metadados[nome_tag] = valor

    return metadados