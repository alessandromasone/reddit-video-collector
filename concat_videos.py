import os
import subprocess
import logging
import argparse

def setup_logger(log_file_name=None):
    logger = logging.getLogger('reddit_video_concat')
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

def concat_videos(input_folder, output_file, logger):
    logger.info('Inizio concatenazione video')

    # Trova tutti i file video nella cartella
    video_files = [f for f in os.listdir(input_folder) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    if not video_files:
        logger.warning('Nessun file video trovato nella cartella')
        return

    video_files.sort()  # Ordina i file per nome (facoltativo)
    logger.info(f'Trovati {len(video_files)} file video')

    # Crea un file temporaneo che contiene l'elenco dei file video
    with open("file_list.txt", "w") as file_list:
        for video_file in video_files:
            file_list.write(f"file '{os.path.join(input_folder, video_file)}'\n")
    
    logger.info('File di elenco video creato')

    # Usa ffmpeg per concatenare i video
    command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'file_list.txt', '-c', 'copy', output_file]
    logger.info(f'Esecuzione comando: {" ".join(command)}')
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        logger.info('Concatenazione completata con successo')
    else:
        logger.error(f'Errore durante la concatenazione: {result.stderr}')

    # Rimuove il file temporaneo
    os.remove("file_list.txt")
    logger.info('File temporaneo rimosso')

def main():
    parser = argparse.ArgumentParser(description="Aggiungi overlay di testo ai video in una cartella.")
    parser.add_argument('--input', type=str, default='edited', help='Cartella di input contenente i video')
    parser.add_argument('--output', type=str, required=True, help='Cartella di output per i video elaborati')
    parser.add_argument('--log', action='store_true', help='Abilita il logging')
    parser.add_argument('--logfile', type=str, default='reddit.log', help='Nome del file di log')

    args = parser.parse_args()

    logger = setup_logger(args.logfile if args.log else None)

    concat_videos(args.input, args.output, logger)

if __name__ == '__main__':
    main()
