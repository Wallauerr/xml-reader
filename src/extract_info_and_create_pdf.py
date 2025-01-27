import xml.etree.ElementTree as ET
import chardet
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Função para extrair informações do XML e criar o PDF
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

  # Extrair informações do emitente
  emit_element = root.find(".//nfe:emit", namespaces=namespace)
  emit_info = {}
  if emit_element is not None:
    emit_info["CNPJ"] = emit_element.find(".//nfe:CNPJ", namespaces=namespace).text
    emit_info["xNome"] = emit_element.find(".//nfe:xNome", namespaces=namespace).text
    endereco_emit = emit_element.find(".//nfe:enderEmit", namespaces=namespace)
    emit_info["endereco"] = {
      "xLgr": endereco_emit.find(".//nfe:xLgr", namespaces=namespace).text,
      "nro": endereco_emit.find(".//nfe:nro", namespaces=namespace).text,
      "xBairro": endereco_emit.find(".//nfe:xBairro", namespaces=namespace).text,
      "xMun": endereco_emit.find(".//nfe:xMun", namespaces=namespace).text,
      "UF": endereco_emit.find(".//nfe:UF", namespaces=namespace).text,
      "CEP": endereco_emit.find(".//nfe:CEP", namespaces=namespace).text,
    }

  # Extrair informações do destinatário
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
      "CEP": endereco_dest.find(".//nfe:CEP", namespaces=namespace).text,
    }

  # Extrair informações da transportadora
  transp_element = root.find(".//nfe:transporta", namespaces=namespace)
  transp_info = {}
  if transp_element is not None:
    transp_info["CNPJ"] = transp_element.find(".//nfe:CNPJ", namespaces=namespace).text
    transp_info["xNome"] = transp_element.find(".//nfe:xNome", namespaces=namespace).text
    transp_info["endereco"] = transp_element.find(".//nfe:xEnder", namespaces=namespace).text

  # Extrair informações de volumes
  volume_element = root.find(".//nfe:vol", namespaces=namespace)
  vol_info = {}
  if volume_element is not None:
    vol_info["qVol"] = volume_element.find(".//nfe:qVol", namespaces=namespace).text

  # Criar PDF com informações extraídas
  c = canvas.Canvas(pdf_file, pagesize=letter)
  c.drawString(250, 750, f"NOME DA EMPRESA")

  # Informações do emitente
  c.drawString(100, 730, f"Emitente:")
  c.drawString(100, 710, f"CNPJ: {emit_info['CNPJ']}")
  c.drawString(100, 690, f"Nome: {emit_info['xNome']}")
  c.drawString(100, 670, f"Endereço: {emit_info['endereco']['xLgr']}, {emit_info['endereco']['nro']}")
  c.drawString(100, 650, f"Bairro: {emit_info['endereco']['xBairro']}")
  c.drawString(100, 630, f"Cidade: {emit_info['endereco']['xMun']} - {emit_info['endereco']['UF']}")
  c.drawString(100, 610, f"CEP: {emit_info['endereco']['CEP']}")

  # Informações do destinatário
  c.drawString(100, 590, f"Destinatário:")
  c.drawString(100, 570, f"CNPJ: {dest_info['CNPJ']}")
  c.drawString(100, 550, f"Nome: {dest_info['xNome']}")
  c.drawString(100, 530, f"Endereço: {dest_info['endereco']['xLgr']}, {dest_info['endereco']['nro']}")
  c.drawString(100, 510, f"Bairro: {dest_info['endereco']['xBairro']}")
  c.drawString(100, 490, f"Cidade: {dest_info['endereco']['xMun']} - {dest_info['endereco']['UF']}")
  c.drawString(100, 470, f"CEP: {dest_info['endereco']['CEP']}")

  # Informações da transportadora
  c.drawString(100, 450, f"Transportadora:")
  c.drawString(100, 430, f"CNPJ: {transp_info['CNPJ']}")
  c.drawString(100, 410, f"Nome: {transp_info['xNome']}")
  c.drawString(100, 390, f"Endereço: {transp_info['endereco']}")

  # Informações de volumes
  c.drawString(100, 370, f"Volumes:")
  c.drawString(100, 350, f"Quantidade de Volumes: {vol_info['qVol']}")

  c.save()
