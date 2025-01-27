import tkinter as tk
from tkinter import filedialog
import process_files

# Configurar a janela principal
root = tk.Tk()
root.title("Processador de XML para PDF v4.0") #TODO ajustar para procurar arquivos e não a pasta, e também se tiver mais arquivos que não sejam xml

# Etiqueta e entrada para a pasta de entrada
input_folder_label = tk.Label(root, text="Pasta de Entrada:")
input_folder_label.pack(pady=10)
input_folder_entry = tk.Entry(root, width=50)
input_folder_entry.pack()
input_folder_button = tk.Button(root, text="Selecionar Pasta", command=lambda: input_folder_entry.insert(0, filedialog.askdirectory()))
input_folder_button.pack(pady=10)

# Etiqueta e entrada para a pasta de saída
output_folder_label = tk.Label(root, text="Pasta de Saída:")
output_folder_label.pack(pady=10)
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.pack()
output_folder_button = tk.Button(root, text="Selecionar Pasta", command=lambda: output_folder_entry.insert(0, filedialog.askdirectory()))
output_folder_button.pack(pady=10)

# Botão para iniciar o processamento
process_button = tk.Button(root, text="Processar", command=lambda: process_files.process_files(input_folder_entry, output_folder_entry))
process_button.pack(pady=10)

root.mainloop()
