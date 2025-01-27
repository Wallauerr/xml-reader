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

  # Função para centralizar texto com a fonte especificada
  def draw_centered_string(c, x_center, y, text, font_size, font_name='Helvetica'):
    c.setFont(font_name, font_size)
    text_width = c.stringWidth(text, font_name, font_size)
    x = x_center - (text_width / 2)
    c.drawString(x, y, text)

  # Criar PDF com informações extraídas
  c = canvas.Canvas(pdf_file, pagesize=letter)

  # Definir centro da página
  page_width = c._pagesize[0]
  center_x = page_width / 2

  draw_centered_string(c, center_x, 750, f"NFE {nfe_info['numero']}", 24, 'Helvetica-Bold')
  draw_centered_string(c, center_x, 690, f"Volumes {vol_info['qVol']}", 24, 'Helvetica-Bold') #TODO Fazer lógica para mostrar 1/1 ou 1/2, 2/2 Volumes ou volume se for 1/1
  draw_centered_string(c, center_x, 550, f"Para: {dest_info['xNome']}", 18, 'Helvetica-Bold')
  draw_centered_string(c, center_x, 530, f"Endereço: {dest_info['endereco']['xLgr']}, {dest_info['endereco']['nro']}", 12)
  draw_centered_string(c, center_x, 510, f"Bairro: {dest_info['endereco']['xBairro']}", 12)
  draw_centered_string(c, center_x, 490, f"Cidade: {dest_info['endereco']['xMun']} - {dest_info['endereco']['UF']}", 12)
  draw_centered_string(c, center_x, 410, f"Remetente: {emit_info['xNome']}", 12)
  draw_centered_string(c, center_x, 350, f"Transportadora: {transp_info['xNome']}", 12)

  c.save()
