import os
import subprocess
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, script_path):
        self.script_path = script_path
        self.process = None
        self.start_process()
        print("\n✅ Aplicação iniciada com sucesso!")

    def start_process(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.process = subprocess.Popen([sys.executable, self.script_path])

        os.system('cls' if os.name == 'nt' else 'clear')

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            self.start_process()
            print(f"\n🔁 Reiniciando devido a mudanças em: {event.src_path}")

def main():
    event_handler = ReloadHandler("app.py")
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            event_handler.process.terminate()
    observer.join()

if __name__ == "__main__":
    main()
