import xml.etree.ElementTree as ET
import chardet
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def extract_info_and_create_pdf(xml_file, pdf_file):
  # Detecta a codificação do arquivo XML
  with open(xml_file, "rb") as xml_content:
    result = chardet.detect(xml_content.read())
  encoding = result["encoding"]

  # Lê o arquivo XML com a codificação detectada
  with open(xml_file, "r", encoding=encoding) as xml_content:
    xml_data = xml_content.read()

  # Parse do XML
  root = ET.fromstring(xml_data)

  # Define o namespace
  namespace = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

  # Extrair numero
  ide_element = root.find(".//nfe:ide", namespaces=namespace)
  nfe_info = {}
  if ide_element is not None:
    nfe_info["numero"] = ide_element.find(".//nfe:nNF", namespaces=namespace).text

  # Extrair emitente
  emit_element = root.find(".//nfe:emit", namespaces=namespace)
  emit_info = {}
  if emit_element is not None:
    emit_info["xNome"] = emit_element.find(".//nfe:xNome", namespaces=namespace).text

  # Extrair destinatário
  dest_element = root.find(".//nfe:dest", namespaces=namespace)
  dest_info = {}
  if dest_element is not None:
    dest_info["CNPJ"] = dest_element.find(".//nfe:CNPJ", namespaces=namespace).text
    dest_info["xNome"] = dest_element.find(".//nfe:xNome", namespaces=namespace).text
    endereco_dest = dest_element.find(".//nfe:enderDest", namespaces=namespace)
    dest_info["endereco"] = {
      "xLgr": endereco_dest.find(".//nfe:xLgr", namespaces=namespace).text,
      "nro": endereco_dest.find(".//nfe:nro", namespaces=namespace).text,
      "xBairro": endereco_dest.find(".//nfe:xBairro", namespaces=namespace).text,
      "xMun": endereco_dest.find(".//nfe:xMun", namespaces=namespace).text,
      "UF": endereco_dest.find(".//nfe:UF", namespaces=namespace).text,
    }

  # Extrair transportadora
  transp_element = root.find(".//nfe:transporta", namespaces=namespace)
  transp_info = {}
  if transp_element is not None:
    transp_info["xNome"] = transp_element.find(".//nfe:xNome", namespaces=namespace).text

  # Extrair volumes
  volume_element = root.find(".//nfe:vol", namespaces=namespace)
  vol_info = {}
  if volume_element is not None:
    vol_info["qVol"] = volume_element.find(".//nfe:qVol", namespaces=namespace).text

  # Criar PDF com informações extraídas
  c = canvas.Canvas(pdf_file, pagesize=letter)

  # Numero
  c.setFontSize(16)
  c.drawString(250, 750, f"{nfe_info['numero']}")

  # Emit
  c.setFontSize(12)
  c.drawString(100, 690, f"Nome: {emit_info['xNome']}")

  # Dest
  c.setFontSize(12)
  c.drawString(100, 590, f"Destinatário:")
  c.setFontSize(12)
  c.drawString(100, 570, f"CNPJ: {dest_info['CNPJ']}")
  c.setFontSize(12)
  c.drawString(100, 550, f"Nome: {dest_info['xNome']}")
  c.setFontSize(12)
  c.drawString(100, 530, f"Endereço: {dest_info['endereco']['xLgr']}, {dest_info['endereco']['nro']}")
  c.setFontSize(12)
  c.drawString(100, 510, f"Bairro: {dest_info['endereco']['xBairro']}")
  c.setFontSize(12)
  c.drawString(100, 490, f"Cidade: {dest_info['endereco']['xMun']} - {dest_info['endereco']['UF']}")

  # Transportadora
  c.setFontSize(12)
  c.drawString(100, 450, f"Transportadora:")
  c.setFontSize(12)
  c.drawString(100, 410, f"Nome: {transp_info['xNome']}")

  # Volumes
  c.setFontSize(12)
  c.drawString(100, 350, f"{vol_info['qVol']}")

  c.save()
