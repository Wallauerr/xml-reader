import os
from logger import logger

def print_pdf(pdf_file):
  try:
    if os.name == "nt":
      if not os.path.exists(pdf_file):
        logger.error(f"Arquivo não encontrado: {pdf_file}")
        return
      
      os.startfile(pdf_file)
      logger.info(f"Abrindo {pdf_file} no visualizador padrão...")
    else:
      logger.warning("A funcionalidade de abertura automática é suportada apenas no Windows.")
  except Exception as error:
    logger.error(f"Erro inesperado ao tentar abrir o PDF: {error}")