import os
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import chardet

# Função para extrair informações do XML e criar o PDF
def extract_info_and_create_pdf(xml_file):
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
        return None

    return dest_info

# Pasta onde estão os arquivos XML
pasta_xml = "C:\\Users\\Usuario\\Downloads\\xml"
pasta_pdf = "C:\\Users\\Usuario\\Downloads\\pdf"

# Lista para armazenar as informações extraídas
info_list = []

# Listar arquivos XML na pasta
for filename in os.listdir(pasta_xml):
    if filename.endswith(".xml"):
        xml_file = os.path.join(pasta_xml, filename)

        # Extrair informações do XML e adicionar à lista
        info = extract_info_and_create_pdf(xml_file)
        if info:
            info_list.append(info)

# Criar PDF com todas as informações extraídas
pdf_file = os.path.join(pasta_pdf, "output.pdf")
c = canvas.Canvas(pdf_file, pagesize=letter)
y_position = 750
for info in info_list:
    c.drawString(500, y_position, f"NOME EMPRESA")
    c.drawString(100, y_position, f"CNPJ: {info['CNPJ']}")
    c.drawString(100, y_position - 20, f"Nome: {info['xNome']}")
    c.drawString(100, y_position - 40, f"CEP: {info['CEP']}")
    y_position -= 60  # Espaçamento entre as informações
# Adicione outras informações ao PDF conforme necessário
c.save()
