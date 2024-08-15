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

  # Extrair informações do XML
  dest_element = root.find(".//nfe:dest", namespaces=namespace)
  dest_info = {}

  if dest_element is not None:
    dest_info["CNPJ"] = dest_element.find(".//nfe:CNPJ", namespaces=namespace).text
    dest_info["xNome"] = dest_element.find(".//nfe:xNome", namespaces=namespace).text
    dest_info["CEP"] = dest_element.find(".//nfe:CEP", namespaces=namespace).text
    # Outras informações que você deseja extrair
  else:
    print(f"Tag <dest> não encontrada no arquivo {xml_file}")
    return

  # Criar PDF com informações extraídas
  c = canvas.Canvas(pdf_file, pagesize=letter)
  c.drawString(250, 750, f"NOME DA EMPRESA")
  c.drawString(100, 730, f"CNPJ: {dest_info['CNPJ']}")
  c.drawString(100, 710, f"{dest_info['xNome']}")
  c.drawString(100, 680, f"CEP: {dest_info['CEP']}")
  # Adicione outras informações ao PDF conforme necessário
  c.save()
