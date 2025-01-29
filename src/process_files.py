import os
from tkinter import messagebox
from extract_info_and_create_pdf import extract_info_and_create_pdf

def process_files(input_folder_entry, output_folder_entry):
  input_folder = input_folder_entry.get()
  output_folder = output_folder_entry.get()

  if not os.path.exists(input_folder) or not os.path.exists(output_folder):
    messagebox.showerror("Erro", "Por favor, selecione pastas de entrada e saída válidas.")
    return

  for filename in os.listdir(input_folder):
    if filename.endswith(".xml"):
      xml_file = os.path.join(input_folder, filename)

      pdf_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.pdf")

      extract_info_and_create_pdf(xml_file, pdf_file)

  messagebox.showinfo("Concluído", "Processamento concluído. Os arquivos PDF foram criados com sucesso.")
