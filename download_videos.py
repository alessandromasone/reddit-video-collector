import os
import json
import logging
import argparse
from RedDownloader import RedDownloader

# Configura il logger
def setup_logger(log_file_name=None):
    logger = logging.getLogger('reddit_video_download')
    logger.setLevel(logging.DEBUG)

    if log_file_name:
        # Handler per il file di log
        file_handler = logging.FileHandler(log_file_name, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

        # Handler per la console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)

        # Formato del log
        file_name = os.path.basename(__file__)
        formatter = logging.Formatter(f'%(asctime)s - {file_name} - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
    else:
        # Disabilita la gestione dei log se log_file_name è None
        logger.handlers = []

    return logger

# Main function
def main():
    parser = argparse.ArgumentParser(description="Scarica video da un file JSON di Reddit.")
    parser.add_argument('--jsonfile', type=str, required=True, help='Nome del file JSON contenente i post')
    parser.add_argument('--savedir', type=str, default='download', help='Directory per salvare i video')
    parser.add_argument('--quality', type=int, default=720, help='Qualità del video da scaricare (es. 720)')
    parser.add_argument('--log', action='store_true', help='Abilita il logging')
    parser.add_argument('--logfile', type=str, default='reddit.log', help='Nome del file di log')

    args = parser.parse_args()

    # Configura il logger in base al parametro --log
    logger = setup_logger(args.logfile if args.log else None)

    json_file = args.jsonfile
    save_directory = args.savedir
    quality = args.quality

    # Legge il file JSON con codifica UTF-8
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            posts = json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"Errore nella decodifica del JSON: {e}")
        exit(1)
    except FileNotFoundError:
        logger.error("Il file JSON non è stato trovato.")
        exit(1)

    os.makedirs(save_directory, exist_ok=True)

    for post in posts:
        title = post['title']
        url = post['url']
        
        # Rimuove caratteri non validi per i nomi dei file
        safe_title = "".join(char for char in title if char.isalnum() or char in (' ', '_', '-')).rstrip()
        
        # Crea il percorso del file
        file_path = os.path.join(save_directory, safe_title)
        
        if logger:
            logger.info(f"Scaricando '{title}' da {url}")

        try:
            # Usa RedDownloader per scaricare il video
            downloader = RedDownloader.Download(url=url, output=file_path, quality=quality)
            if logger:
                logger.info(f"Video '{title}' scaricato con successo!")
        except Exception as e:
            if logger:
                logger.error(f"Errore durante il download del video '{title}': {e}")

    if logger:
        logger.info("Download completato.")

if __name__ == "__main__":
    main()
