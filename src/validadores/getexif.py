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


def ler_gps_exif(imagem: Image.Image) -> dict:
    exif = imagem.getexif()

    if not exif:
        return {"aviso": "Imagem sem EXIF."}

    gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)

    if not gps_ifd:
        return {"aviso": "Imagem sem dados GPS."}

    gps_dados = {}

    for tag_id, valor in gps_ifd.items():
        nome_tag = ExifTags.GPSTAGS.get(tag_id, f"GPS_{tag_id}")
        gps_dados[nome_tag] = valor

    return gps_dados