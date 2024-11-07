from RedDownloader import RedDownloader
import os

def scarica_clip(url, destinazione, nome_file, risoluzione=1080):
    # Creiamo il percorso completo per il file
    percorso_completo = os.path.join(destinazione, nome_file)

    # Verifica se la cartella di destinazione esiste, altrimenti la crea
    if not os.path.exists(destinazione):
        os.makedirs(destinazione)

    try:
        # Scarica il video
        RedDownloader.Download(url=url, output=percorso_completo, quality=risoluzione)
        
        # Ritorna True se il download è stato completato con successo
        return True

    except Exception as e:
        
        # Ritorna False in caso di errore
        return False
