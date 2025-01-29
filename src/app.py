import tkinter as tk
from tkinter import filedialog
import process_files

root = tk.Tk()
root.title("Processador de XML para PDF v4.0")

def select_input_paths():
  paths = filedialog.askopenfilenames(filetypes=[("XML files", "*.xml"), ("All files", "*.*")])
  input_paths_entry.delete(0, tk.END)
  input_paths_entry.insert(0, ";".join(paths))

def select_input_folder():
  folder = filedialog.askdirectory()
  input_paths_entry.delete(0, tk.END)
  input_paths_entry.insert(0, folder)

input_paths_label = tk.Label(root, text="Arquivos/Pasta de Entrada:")
input_paths_label.pack(pady=10)
input_paths_entry = tk.Entry(root, width=50)
input_paths_entry.pack()
input_files_button = tk.Button(root, text="Selecionar Arquivos", command=select_input_paths)
input_files_button.pack(pady=5)
input_folder_button = tk.Button(root, text="Selecionar Pasta", command=select_input_folder)
input_folder_button.pack(pady=5)

output_folder_label = tk.Label(root, text="Pasta de Saída:")
output_folder_label.pack(pady=10)
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.pack()
output_folder_button = tk.Button(root, text="Selecionar Pasta", command=lambda: output_folder_entry.insert(0, filedialog.askdirectory()))
output_folder_button.pack(pady=10)

process_button = tk.Button(root, text="Processar", command=lambda: process_files.process_files(input_paths_entry.get().split(";"), output_folder_entry))
process_button.pack(pady=10)

root.mainloop()
