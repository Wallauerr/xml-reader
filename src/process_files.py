import os
from tkinter import messagebox
from extract_info_and_create_pdf import extract_info_and_create_pdf
from logger import logger

def process_files(input_paths, output_folder_entry):
  output_folder = output_folder_entry.get()

  if not output_folder or not os.path.exists(output_folder):
    logger.error("Pasta de saída inválida ou não selecionada.")
    messagebox.showerror("Erro", "Por favor, selecione uma pasta de saída válida.")
    return

  for input_path in input_paths:
    if os.path.isfile(input_path) and input_path.endswith(".xml"):
      xml_file = input_path
      pdf_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_path))[0]}.pdf")
      try:
        logger.info(f"Processando arquivo: {xml_file}")
        extract_info_and_create_pdf(xml_file, pdf_file)
        logger.info(f"Arquivo processado com sucesso: {pdf_file}")
      except Exception as e:
        logger.error(f"Erro ao processar o arquivo {xml_file}: {e}", exc_info=True)

  messagebox.showinfo("Concluído", "Processamento concluído. Os arquivos PDF foram criados com sucesso.")
