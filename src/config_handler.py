import json
import os

CONFIG_FILE = "config.json"

def load_config():
  if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as file:
      return json.load(file)
  return {"input_folder": "", "output_folder": ""}

def save_config(input_folder, output_folder):
  config = {
    "input_folder": input_folder,
    "output_folder": output_folder
  }
  with open(CONFIG_FILE, "w") as file:
    json.dump(config, file)