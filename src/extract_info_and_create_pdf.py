import xml.etree.ElementTree as ET

import chardet
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas

from logger import logger
from print_utils import print_pdf


def extract_info_and_create_pdf(xml_file, pdf_file):
    try:
        with open(xml_file, "rb") as xml_content:
            result = chardet.detect(xml_content.read())
        encoding = result["encoding"]

        with open(xml_file, "r", encoding=encoding) as xml_content:
            xml_data = xml_content.read()

        root = ET.fromstring(xml_data)

        namespace = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

        # Extrair informações do XML
        nfe_info = {}
        emit_info = {}
        dest_info = {}
        transp_info = {}
        vol_info = {}

        # Extrair número
        ide_element = root.find(".//nfe:ide", namespaces=namespace)
        if ide_element is not None:
            nfe_info["numero"] = ide_element.find(
                ".//nfe:nNF", namespaces=namespace
            ).text

        # Extrair emitente
        emit_element = root.find(".//nfe:emit", namespaces=namespace)
        if emit_element is not None:
            emit_info["xNome"] = emit_element.find(
                ".//nfe:xNome", namespaces=namespace
            ).text

        # Extrair destinatário
        dest_element = root.find(".//nfe:dest", namespaces=namespace)
        if dest_element is not None:
            dest_info["xNome"] = dest_element.find(
                ".//nfe:xNome", namespaces=namespace
            ).text
            endereco_dest = dest_element.find(".//nfe:enderDest", namespaces=namespace)
            if endereco_dest is not None:
                dest_info["endereco"] = {
                    "xLgr": endereco_dest.find(
                        ".//nfe:xLgr", namespaces=namespace
                    ).text,
                    "nro": endereco_dest.find(".//nfe:nro", namespaces=namespace).text,
                    "xBairro": endereco_dest.find(
                        ".//nfe:xBairro", namespaces=namespace
                    ).text,
                    "xMun": endereco_dest.find(
                        ".//nfe:xMun", namespaces=namespace
                    ).text,
                    "UF": endereco_dest.find(".//nfe:UF", namespaces=namespace).text,
                }

        # Extrair transportadora
        transp_element = root.find(".//nfe:transporta", namespaces=namespace)
        if transp_element is not None:
            transp_info["xNome"] = transp_element.find(
                ".//nfe:xNome", namespaces=namespace
            ).text

        # Extrair volumes
        volume_element = root.find(".//nfe:vol", namespaces=namespace)
        if volume_element is not None:
            vol_info["qVol"] = int(
                volume_element.find(".//nfe:qVol", namespaces=namespace).text
            )

        def draw_centered_string(
            c, x_center, y, text, font_size, font_name="Helvetica"
        ):
            c.setFont(font_name, font_size)
            text_width = c.stringWidth(text, font_name, font_size)
            x = x_center - (text_width / 2)
            c.drawString(x, y, text)

        c = canvas.Canvas(pdf_file, pagesize=landscape(letter))

        page_width = c._pagesize[0]
        center_x = page_width / 2

        qVol = vol_info.get("qVol", 1)
        volume_text = "Volume" if qVol == 1 else "Volumes"

        for volume in range(1, qVol + 1):
            if volume > 1:
                c.showPage()

            draw_centered_string(
                c, center_x, 405, f"NFE {nfe_info['numero']}", 18, "Helvetica-Bold"
            )
            volume_info = f"{volume}/{qVol}"
            draw_centered_string(
                c, center_x, 380, f"{volume_text} {volume_info}", 18, "Helvetica-Bold"
            )
            draw_centered_string(
                c, center_x, 330, f"Para: {dest_info['xNome']}", 14, "Helvetica-Bold"
            )
            draw_centered_string(
                c,
                center_x,
                310,
                f"Endereço: {dest_info['endereco']['xLgr']}, {dest_info['endereco']['nro']}",
                10,
            )
            draw_centered_string(
                c, center_x, 290, f"Bairro: {dest_info['endereco']['xBairro']}", 10
            )
            draw_centered_string(
                c,
                center_x,
                270,
                f"Cidade: {dest_info['endereco']['xMun']} - {dest_info['endereco']['UF']}",
                10,
            )
            draw_centered_string(
                c, center_x, 220, f"Remetente: {emit_info['xNome']}", 10
            )
            draw_centered_string(
                c, center_x, 200, f"Transportadora: {transp_info['xNome']}", 10
            )

        c.save()
        logger.info(f"PDF gerado com sucesso: {pdf_file}")

        print_pdf(pdf_file)

    except Exception as error:
        logger.error(
            f"Erro ao processar o arquivo XML {xml_file}: {error}", exc_info=True
        )
        raise
