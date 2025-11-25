import os
import tkinter as tk
from tkinter import filedialog, messagebox

from config_handler import load_config, save_config
from logger import logger
from process_files import process_files


def main():
    try:
        root = tk.Tk()
        root.title("Gerador de Etiquetas")

        icon_path = os.path.join(
            os.path.dirname(__file__), "assets", "favicon-sulmag_96x96.ico"
        )
        root.iconbitmap(icon_path)

        config = load_config()
        last_input_folder = config.get("input_folder", "")
        last_output_folder = config.get("output_folder", "")

        def select_input_paths():
            paths = filedialog.askopenfilenames(
                initialdir=last_input_folder, filetypes=[("XML files", "*.xml")]
            )
            if paths:
                input_paths_entry.delete(0, tk.END)
                input_paths_entry.insert(0, ";".join(paths))
                save_config(os.path.dirname(paths[0]), last_output_folder)

        def select_output_folder():
            folder = filedialog.askdirectory(initialdir=last_output_folder)
            if folder:
                output_folder_entry.delete(0, tk.END)
                output_folder_entry.insert(0, folder)
                save_config(last_input_folder, folder)

        input_paths_label = tk.Label(root, text="Arquivos de Entrada:")
        input_paths_label.pack(pady=10)
        input_paths_entry = tk.Entry(root, width=50)
        input_paths_entry.pack()
        input_button = tk.Button(
            root, text="Selecionar Arquivos XML", command=select_input_paths
        )
        input_button.pack(pady=5)

        output_folder_label = tk.Label(root, text="Pasta de Saída:")
        output_folder_label.pack(pady=10)
        output_folder_entry = tk.Entry(root, width=50)
        output_folder_entry.pack()
        output_folder_button = tk.Button(
            root, text="Selecionar Pasta", command=select_output_folder
        )
        output_folder_button.pack(pady=10)

        if last_input_folder:
            input_paths_entry.insert(0, last_input_folder)
        if last_output_folder:
            output_folder_entry.insert(0, last_output_folder)

        process_button = tk.Button(
            root,
            text="Processar",
            command=lambda: process_files(
                input_paths_entry.get().split(";"), output_folder_entry
            ),
        )
        process_button.pack(pady=10)

        root.mainloop()
    except Exception as error:
        logger.error(f"Erro ao executar o aplicativo: {error}", exc_info=True)
        messagebox.showerror(
            "Erro",
            "Ocorreu um erro inesperado. Verifique o arquivo app.log para mais detalhes.",
        )


if __name__ == "__main__":
    main()
