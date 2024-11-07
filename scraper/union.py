import os
import subprocess

def union_video_ffmpeg(input_folder, output_name):
    # Trova tutti i file mp4 nella cartella e li ordina
    video_files = [f for f in os.listdir(input_folder) if f.endswith(".mp4")]
    video_files.sort()
    
    # Controlla se ci sono video
    if not video_files:
        print("Nessun file video trovato nella cartella specificata.")
        return
    
    # Crea un file temporaneo con la lista dei video
    with open("filelist.txt", "w") as f:
        for file in video_files:
            f.write(f"file '{os.path.join(input_folder, file)}'\n")
    
    # Usa ffmpeg per unire i video
    try:
        subprocess.run(
            ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "filelist.txt", "-c", "copy", output_name],
            check=True
        )
        print(f"Video unito creato con successo: {output_name}")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'unione dei video: {e}")
    finally:
        # Elimina il file temporaneo
        os.remove("filelist.txt")

# Esempio di utilizzo:
# union_video_ffmpeg("percorso/della/cartella", "video_unito.mp4")
