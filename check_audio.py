import os
import subprocess
import json
import logging
import argparse

def has_audio(file_path):
    # Usa ffprobe per ottenere i dettagli delle tracce del file
    command = [
        'ffprobe', '-v', 'error', '-show_entries',
        'stream=codec_type', '-of', 'json', file_path
    ]
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Parse l'output JSON
    probe_info = json.loads(result.stdout)
    
    # Controlla se tra i flussi (streams) c'è una traccia di tipo 'audio'
    for stream in probe_info.get('streams', []):
        if stream.get('codec_type') == 'audio':
            return True
    return False

def setup_logger(log_file_name=None):
    logger = logging.getLogger('reddit_video_audio')
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

def check_videos_in_folder(folder_path, logger):
    # Controlla tutti i file nella cartella
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path):
            # Verifica se il file ha audio
            if has_audio(file_path):
                logger.info(f"{file_name}: ha traccia audio.")
            else:
                logger.warning(f"{file_name}: non ha traccia audio. Elimino il file.")
                os.remove(file_path)
                logger.info(f"{file_name}: file eliminato.")

def main():
    parser = argparse.ArgumentParser(description="Controlla se i video in una cartella hanno tracce audio e rimuove i file senza audio.")
    parser.add_argument('--folder', type=str, required=True, help='Percorso della cartella contenente i video')
    parser.add_argument('--log', action='store_true', help='Abilita il logging')
    parser.add_argument('--logfile', type=str, default='reddit.log', help='Nome del file di log')

    args = parser.parse_args()

    # Configura il logger in base al parametro --log
    logger = setup_logger(args.logfile if args.log else None)

    folder_path = args.folder

    check_videos_in_folder(folder_path, logger)

if __name__ == "__main__":
    main()
