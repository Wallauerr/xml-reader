import os
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import chardet
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

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

# Função para processar os arquivos XML na pasta selecionada
def process_files():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()

    if not os.path.exists(input_folder) or not os.path.exists(output_folder):
        messagebox.showerror("Erro", "Por favor, selecione pastas de entrada e saída válidas.")
        return

    # Lista para armazenar as informações extraídas
    info_list = []

    # Listar arquivos XML na pasta de entrada
    for filename in os.listdir(input_folder):
        if filename.endswith(".xml"):
            xml_file = os.path.join(input_folder, filename)

            # Extrair informações do XML e adicionar à lista
            info = extract_info_and_create_pdf(xml_file)
            if info:
                info_list.append(info)

    # Criar PDF com todas as informações extraídas
    pdf_file = os.path.join(output_folder, "output.pdf")
    c = canvas.Canvas(pdf_file, pagesize=letter)
    c.drawString(500, 750, f"NOME EMPRESA")
    y_position = 750
    for info in info_list:
        c.drawString(100, y_position, f"CNPJ: {info['CNPJ']}")
        c.drawString(100, y_position - 20, f"Nome: {info['xNome']}")
        c.drawString(100, y_position - 40, f"CEP: {info['CEP']}")
        y_position -= 60  # Espaçamento entre as informações
    # Adicione outras informações ao PDF conforme necessário
    c.save()
    messagebox.showinfo("Concluído", "Processamento concluído. O arquivo PDF foi criado com sucesso.")

# Configurar a janela principal
root = tk.Tk()
root.title("Processador de XML para PDF")

# Etiqueta e entrada para a pasta de entrada
input_folder_label = tk.Label(root, text="Pasta de Entrada:")
input_folder_label.pack()
input_folder_entry = tk.Entry(root, width=50)
input_folder_entry.pack()
input_folder_button = tk.Button(root, text="Selecionar Pasta", command=lambda: input_folder_entry.insert(0, filedialog.askdirectory()))
input_folder_button.pack()

# Etiqueta e entrada para a pasta de saída
output_folder_label = tk.Label(root, text="Pasta de Saída:")
output_folder_label.pack()
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.pack()
output_folder_button = tk.Button(root, text="Selecionar Pasta", command=lambda: output_folder_entry.insert(0, filedialog.askdirectory()))
output_folder_button.pack()

# Botão para iniciar o processamento
process_button = tk.Button(root, text="Processar", command=process_files)
process_button.pack()

root.mainloop()