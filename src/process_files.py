import os
from tkinter import messagebox
import extract_info_and_create_pdf

# Função para processar os arquivos XML na pasta selecionada
def process_files(input_folder_entry, output_folder_entry):
  input_folder = input_folder_entry.get()
  output_folder = output_folder_entry.get()

  if not os.path.exists(input_folder) or not os.path.exists(output_folder):
    messagebox.showerror("Erro", "Por favor, selecione pastas de entrada e saída válidas.")
    return

  # Listar arquivos XML na pasta de entrada
  for filename in os.listdir(input_folder):
    if filename.endswith(".xml"):
      xml_file = os.path.join(input_folder, filename)

      # Gerar nome do arquivo PDF correspondente
      pdf_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.pdf")

      # Extrair informações do XML e criar o PDF
      extract_info_and_create_pdf(xml_file, pdf_file)

  messagebox.showinfo("Concluído", "Processamento concluído. Os arquivos PDF foram criados com sucesso.")