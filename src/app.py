import tkinter as tk
from tkinter import filedialog
from process_files import process_files

root = tk.Tk()
root.title("Gerador de Etiquetas")

def select_input_paths():
  paths = filedialog.askopenfilenames(filetypes=[("XML files", "*.xml")])
  input_paths_entry.delete(0, tk.END)
  input_paths_entry.insert(0, ";".join(paths))

input_paths_label = tk.Label(root, text="Arquivos de Entrada:")
input_paths_label.pack(pady=10)
input_paths_entry = tk.Entry(root, width=50)
input_paths_entry.pack()
input_button = tk.Button(root, text="Selecionar Arquivos XML", command=select_input_paths)
input_button.pack(pady=5)

output_folder_label = tk.Label(root, text="Pasta de Saída:")
output_folder_label.pack(pady=10)
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.pack()
output_folder_button = tk.Button(root, text="Selecionar Pasta", command=lambda: output_folder_entry.insert(0, filedialog.askdirectory()))
output_folder_button.pack(pady=10)

process_button = tk.Button(root, text="Processar", command=lambda: process_files(input_paths_entry.get().split(";"), output_folder_entry))
process_button.pack(pady=10)

root.mainloop()
