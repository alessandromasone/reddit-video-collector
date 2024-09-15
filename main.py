import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import json
import subprocess


PREFERENCES_FILE = 'preferences.json'

class VideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Video Reddit")
        self.preferences = self.load_preferences()
        self.create_widgets()
        self.load_preferences_into_widgets()

    def create_widgets(self):
        # Imposta le righe e colonne per la griglia
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)

        # Fase 1: Download da Reddit
        tk.Label(self.root, text="Fase 1: Download Reddit").grid(row=0, column=0, columnspan=2, pady=5)
        
        tk.Label(self.root, text="Subreddits (separati da virgola):").grid(row=1, column=0, sticky="e", padx=5)
        self.subreddits_entry = tk.Entry(self.root)
        self.subreddits_entry.grid(row=1, column=1, padx=5, sticky="ew")

        tk.Label(self.root, text="Numero di post per subreddit:").grid(row=2, column=0, sticky="e", padx=5)
        self.limit_entry = tk.Entry(self.root)
        self.limit_entry.grid(row=2, column=1, padx=5, sticky="ew")

        tk.Label(self.root, text="Nome del file JSON di output:").grid(row=3, column=0, sticky="e", padx=5)
        self.output_entry = tk.Entry(self.root)
        self.output_entry.grid(row=3, column=1, padx=5, sticky="ew")

        self.download_log_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Abilita logging", variable=self.download_log_var).grid(row=4, column=1, padx=5, sticky="w")

        tk.Label(self.root, text="Nome del file di log:").grid(row=5, column=0, sticky="e", padx=5)
        self.download_logfile_entry = tk.Entry(self.root)
        self.download_logfile_entry.grid(row=5, column=1, padx=5, sticky="ew")

        tk.Button(self.root, text="Avvia Download", command=self.download_reddit).grid(row=6, column=0, columnspan=2, pady=5)

        # Fase 2: Scarica video da JSON
        tk.Label(self.root, text="Fase 2: Scarica Video da JSON").grid(row=7, column=0, columnspan=2, pady=5)

        tk.Label(self.root, text="Nome del file JSON contenente i post:").grid(row=8, column=0, sticky="e", padx=5)
        self.jsonfile_entry = tk.Entry(self.root)
        self.jsonfile_entry.grid(row=8, column=1, padx=5, sticky="ew")

        tk.Label(self.root, text="Directory di salvataggio:").grid(row=9, column=0, sticky="e", padx=5)
        self.savedir_entry = tk.Entry(self.root)
        self.savedir_entry.grid(row=9, column=1, padx=5, sticky="ew")

        tk.Label(self.root, text="Qualità del video:").grid(row=10, column=0, sticky="e", padx=5)
        self.quality_entry = tk.Entry(self.root)
        self.quality_entry.grid(row=10, column=1, padx=5, sticky="ew")

        self.download_video_log_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Abilita logging", variable=self.download_video_log_var).grid(row=11, column=1, padx=5, sticky="w")

        tk.Label(self.root, text="Nome del file di log:").grid(row=12, column=0, sticky="e", padx=5)
        self.download_video_logfile_entry = tk.Entry(self.root)
        self.download_video_logfile_entry.grid(row=12, column=1, padx=5, sticky="ew")

        tk.Button(self.root, text="Avvia Download Video", command=self.download_videos).grid(row=13, column=0, columnspan=2, pady=5)

        # Fase 3: Controlla tracce audio
        tk.Label(self.root, text="Fase 3: Controlla Tracce Audio").grid(row=14, column=0, columnspan=2, pady=5)

        tk.Label(self.root, text="Cartella contenente i video:").grid(row=15, column=0, sticky="e", padx=5)
        self.folder_entry = tk.Entry(self.root)
        self.folder_entry.grid(row=15, column=1, padx=5, sticky="ew")

        self.audio_log_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Abilita logging", variable=self.audio_log_var).grid(row=16, column=1, padx=5, sticky="w")

        tk.Label(self.root, text="Nome del file di log:").grid(row=17, column=0, sticky="e", padx=5)
        self.audio_logfile_entry = tk.Entry(self.root)
        self.audio_logfile_entry.grid(row=17, column=1, padx=5, sticky="ew")

        tk.Button(self.root, text="Controlla Audio", command=self.check_audio).grid(row=18, column=0, columnspan=2, pady=5)

        # Fase 4: Aggiungi overlay di testo
        tk.Label(self.root, text="Fase 4: Aggiungi Overlay di Testo").grid(row=19, column=0, columnspan=2, pady=5)

        tk.Label(self.root, text="Cartella di input:").grid(row=20, column=0, sticky="e", padx=5)
        self.input_folder_entry = tk.Entry(self.root)
        self.input_folder_entry.grid(row=20, column=1, padx=5, sticky="ew")

        tk.Label(self.root, text="Cartella di output:").grid(row=21, column=0, sticky="e", padx=5)
        self.output_folder_entry = tk.Entry(self.root)
        self.output_folder_entry.grid(row=21, column=1, padx=5, sticky="ew")

        self.overlay_log_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Abilita logging", variable=self.overlay_log_var).grid(row=22, column=1, padx=5, sticky="w")

        tk.Label(self.root, text="Nome del file di log:").grid(row=23, column=0, sticky="e", padx=5)
        self.overlay_logfile_entry = tk.Entry(self.root)
        self.overlay_logfile_entry.grid(row=23, column=1, padx=5, sticky="ew")

        tk.Button(self.root, text="Aggiungi Overlay", command=self.add_overlay).grid(row=24, column=0, columnspan=2, pady=5)

        # Fase 5: Concatenazione video
        tk.Label(self.root, text="Fase 5: Concatenazione Video").grid(row=25, column=0, columnspan=2, pady=5)

        tk.Label(self.root, text="Cartella di input:").grid(row=26, column=0, sticky="e", padx=5)
        self.concat_input_folder_entry = tk.Entry(self.root)
        self.concat_input_folder_entry.grid(row=26, column=1, padx=5, sticky="ew")

        tk.Label(self.root, text="Nome del file di output:").grid(row=27, column=0, sticky="e", padx=5)
        self.concat_output_file_entry = tk.Entry(self.root)
        self.concat_output_file_entry.grid(row=27, column=1, padx=5, sticky="ew")

        self.concat_log_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Abilita logging", variable=self.concat_log_var).grid(row=28, column=1, padx=5, sticky="w")

        tk.Label(self.root, text="Nome del file di log:").grid(row=29, column=0, sticky="e", padx=5)
        self.concat_logfile_entry = tk.Entry(self.root)
        self.concat_logfile_entry.grid(row=29, column=1, padx=5, sticky="ew")

        tk.Button(self.root, text="Concatenare Video", command=self.concat_videos).grid(row=30, column=0, columnspan=2, pady=5)

        # Salva le preferenze all'uscita
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_preferences(self):
        if os.path.exists(PREFERENCES_FILE):
            with open(PREFERENCES_FILE, 'r') as file:
                return json.load(file)
        return {}

    def load_preferences_into_widgets(self):
        preferences = self.preferences
        self.subreddits_entry.insert(0, preferences.get('subreddits', ''))
        self.limit_entry.insert(0, preferences.get('limit', ''))
        self.output_entry.insert(0, preferences.get('output_json', ''))
        self.download_log_var.set(preferences.get('download_log', False))
        self.download_logfile_entry.insert(0, preferences.get('download_logfile', ''))
        self.jsonfile_entry.insert(0, preferences.get('jsonfile', ''))
        self.savedir_entry.insert(0, preferences.get('savedir', ''))
        self.quality_entry.insert(0, preferences.get('quality', ''))
        self.download_video_log_var.set(preferences.get('download_video_log', False))
        self.download_video_logfile_entry.insert(0, preferences.get('download_video_logfile', ''))
        self.folder_entry.insert(0, preferences.get('folder', ''))
        self.audio_log_var.set(preferences.get('audio_log', False))
        self.audio_logfile_entry.insert(0, preferences.get('audio_logfile', ''))
        self.input_folder_entry.insert(0, preferences.get('input_folder', ''))
        self.output_folder_entry.insert(0, preferences.get('output_folder', ''))
        self.overlay_log_var.set(preferences.get('overlay_log', False))
        self.overlay_logfile_entry.insert(0, preferences.get('overlay_logfile', ''))
        self.concat_input_folder_entry.insert(0, preferences.get('concat_input_folder', ''))
        self.concat_output_file_entry.insert(0, preferences.get('concat_output_file', ''))
        self.concat_log_var.set(preferences.get('concat_log', False))
        self.concat_logfile_entry.insert(0, preferences.get('concat_logfile', ''))

    def save_preferences(self):
        preferences = {
            'subreddits': self.subreddits_entry.get(),
            'limit': self.limit_entry.get(),
            'output_json': self.output_entry.get(),
            'download_log': self.download_log_var.get(),
            'download_logfile': self.download_logfile_entry.get(),
            'jsonfile': self.jsonfile_entry.get(),
            'savedir': self.savedir_entry.get(),
            'quality': self.quality_entry.get(),
            'download_video_log': self.download_video_log_var.get(),
            'download_video_logfile': self.download_video_logfile_entry.get(),
            'folder': self.folder_entry.get(),
            'audio_log': self.audio_log_var.get(),
            'audio_logfile': self.audio_logfile_entry.get(),
            'input_folder': self.input_folder_entry.get(),
            'output_folder': self.output_folder_entry.get(),
            'overlay_log': self.overlay_log_var.get(),
            'overlay_logfile': self.overlay_logfile_entry.get(),
            'concat_input_folder': self.concat_input_folder_entry.get(),
            'concat_output_file': self.concat_output_file_entry.get(),
            'concat_log': self.concat_log_var.get(),
            'concat_logfile': self.concat_logfile_entry.get(),
        }
        with open(PREFERENCES_FILE, 'w') as file:
            json.dump(preferences, file)



    def download_reddit(self):
        try:
            # Costruisci la lista dei parametri del comando
            command = ['python', 'download_reddit.py']
            
            # Aggiungi i parametri se sono presenti
            if self.subreddits_entry.get():
                command += ['--subreddits', self.subreddits_entry.get()]
            if self.limit_entry.get():
                command += ['--limit', self.limit_entry.get()]
            if self.output_entry.get():
                command += ['--output', self.output_entry.get()]
            if self.download_log_var.get():
                command += ['--log', str(self.download_log_var.get()).lower()]
            if self.download_logfile_entry.get():
                command += ['--logfile', self.download_logfile_entry.get()]
            
            subprocess.run(command, check=True)
            messagebox.showinfo("Info", "Download Reddit completato con successo.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Errore", f"Errore durante il download: {e}")

        self.save_preferences()

    def download_videos(self):
        try:
            # Costruisci la lista dei parametri del comando
            command = ['python', 'download_videos.py']
            
            # Aggiungi i parametri se sono presenti
            if self.jsonfile_entry.get():
                command += ['--jsonfile', self.jsonfile_entry.get()]
            if self.savedir_entry.get():
                command += ['--savedir', self.savedir_entry.get()]
            if self.quality_entry.get():
                command += ['--quality', self.quality_entry.get()]
            if self.download_video_log_var.get():
                command += ['--log', str(self.download_video_log_var.get()).lower()]
            if self.download_video_logfile_entry.get():
                command += ['--logfile', self.download_video_logfile_entry.get()]
            
            subprocess.run(command, check=True)
            messagebox.showinfo("Info", "Download video completato con successo.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Errore", f"Errore durante il download dei video: {e}")

        self.save_preferences()

    def check_audio(self):
        try:
            # Costruisci la lista dei parametri del comando
            command = ['python', 'check_audio.py']
            
            # Aggiungi i parametri se sono presenti
            if self.folder_entry.get():
                command += ['--folder', self.folder_entry.get()]
            if self.audio_log_var.get():
                command += ['--log', str(self.audio_log_var.get()).lower()]
            if self.audio_logfile_entry.get():
                command += ['--logfile', self.audio_logfile_entry.get()]
            
            subprocess.run(command, check=True)
            messagebox.showinfo("Info", "Controllo delle tracce audio completato.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Errore", f"Errore durante il controllo audio: {e}")

        self.save_preferences()

    def add_overlay(self):
        try:
            # Costruisci la lista dei parametri del comando
            command = ['python', 'add_overlay.py']
            
            # Aggiungi i parametri se sono presenti
            if self.input_folder_entry.get():
                command += ['--input', self.input_folder_entry.get()]
            if self.output_folder_entry.get():
                command += ['--output', self.output_folder_entry.get()]
            if self.overlay_log_var.get():
                command += ['--log', str(self.overlay_log_var.get()).lower()]
            if self.overlay_logfile_entry.get():
                command += ['--logfile', self.overlay_logfile_entry.get()]
            
            subprocess.run(command, check=True)
            messagebox.showinfo("Info", "Aggiunta overlay completata.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Errore", f"Errore durante l'aggiunta dell'overlay: {e}")

        self.save_preferences()

    def concat_videos(self):
        try:
            # Costruisci la lista dei parametri del comando
            command = ['python', 'concat_videos.py']
            
            # Aggiungi i parametri se sono presenti
            if self.concat_input_folder_entry.get():
                command += ['--input', self.concat_input_folder_entry.get()]
            if self.concat_output_file_entry.get():
                command += ['--output', self.concat_output_file_entry.get()]
            if self.concat_log_var.get():
                command += ['--log', str(self.concat_log_var.get()).lower()]
            if self.concat_logfile_entry.get():
                command += ['--logfile', self.concat_logfile_entry.get()]
            
            subprocess.run(command, check=True)
            messagebox.showinfo("Info", "Concatenazione video completata.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Errore", f"Errore durante la concatenazione dei video: {e}")

        self.save_preferences()


    def on_closing(self):
        self.save_preferences()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root)
    root.mainloop()
