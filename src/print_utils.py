import os
import subprocess
from logger import logger

def print_pdf(pdf_file):
  try:
    if os.name == "nt":  # Windows
      os.startfile(pdf_file, "print")
      logger.info(f"Enviando {pdf_file} para impressão no Windows...")
    elif os.name == "posix":  # Unix
      try:
        subprocess.run(["lp", pdf_file], check=True)
        logger.info(f"Enviando {pdf_file} para impressão no macOS/Linux...")
      except subprocess.CalledProcessError as error:
        logger.error(f"Erro ao enviar o arquivo para impressão: {error}")
      except FileNotFoundError:
        logger.error("O comando 'lp' não foi encontrado. Certifique-se de que o sistema de impressão está configurado.")
    else:
      logger.warning("Sistema operacional não suportado para impressão automática.")
  except Exception as error:
    logger.error(f"Erro inesperado ao tentar imprimir: {error}")