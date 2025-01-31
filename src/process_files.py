import os
from tkinter import messagebox
from extract_info_and_create_pdf import extract_info_and_create_pdf

def process_files(input_paths, output_folder_entry):
  output_folder = output_folder_entry.get()

  if not output_folder or not os.path.exists(output_folder):
    messagebox.showerror("Erro", "Por favor, selecione uma pasta de saída válida.")
    return

  for input_path in input_paths:
    if os.path.isfile(input_path) and input_path.endswith(".xml"):
      xml_file = input_path
      pdf_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_path))[0]}.pdf")
      extract_info_and_create_pdf(xml_file, pdf_file)
    elif os.path.isdir(input_path):
      for filename in os.listdir(input_path):
        if filename.endswith(".xml"):
          xml_file = os.path.join(input_path, filename)
          pdf_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.pdf")
          extract_info_and_create_pdf(xml_file, pdf_file)

  messagebox.showinfo("Concluído", "Processamento concluído. Os arquivos PDF foram criados com sucesso.")
