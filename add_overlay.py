import os
import subprocess
import logging
import argparse
from PIL import ImageFont
import json

def setup_logger(log_file_name=None):
    logger = logging.getLogger('reddit_video_overlay')
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

def remove_extension(filename):
    if filename.endswith('.mp4'):
        return filename[:-4]
    return filename

def get_text_width(text, font_path, fontsize):
    font = ImageFont.truetype(font_path, fontsize)
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]

def split_text_to_fit(text, font_path, fontsize, max_width):
    font = ImageFont.truetype(font_path, fontsize)
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        line_width = get_text_width(test_line, font_path, fontsize)

        if line_width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines

def get_video_resolution(video_path):
    # Usa ffprobe per ottenere la risoluzione del video
    result = subprocess.run([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
        '-of', 'json', video_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    info = json.loads(result.stdout)
    width = info['streams'][0]['width']
    height = info['streams'][0]['height']

    return width, height

def process_videos(input_folder, output_folder, logger):
    logger.info(f"Avvio dell'elaborazione video. Cartella di input: {input_folder}, Cartella di output: {output_folder}")
    
    os.makedirs(output_folder, exist_ok=True)
    
    video_files = [f for f in os.listdir(input_folder) if f.endswith('.mp4')]
    video_files.sort()

    if not video_files:
        logger.warning("Nessun video trovato nella cartella.")
        return

    font_path = 'Poppins-Regular.ttf'
    fontsize = 24
    padding = 10  # Padding per il rettangolo di testo e il testo stesso
    text_padding = 10  # Padding interno al rettangolo di testo

    try:
        for video in video_files:
            video_path = os.path.join(input_folder, video)
            text = remove_extension(video)
            logger.info(f"Elaborazione del video: {video} con testo overlay: {text}")

            # Ottieni la risoluzione del video
            video_width, video_height = get_video_resolution(video_path)
            max_text_width = video_width - 2 * padding  # Imposta la larghezza massima del testo

            # Spezza il testo in più righe se necessario
            lines = split_text_to_fit(text, font_path, fontsize, max_text_width)

            # Calcola la larghezza del rettangolo basandosi sulla riga più lunga
            text_width = max(get_text_width(line, font_path, fontsize) for line in lines)
            rect_width = text_width + 2 * text_padding  # Aggiungi padding interno al rettangolo

            # Calcola l'altezza in base al numero di righe
            rect_height = fontsize * len(lines) + 2 * text_padding  # Include padding verticale

            # Calcola la posizione del rettangolo e del testo
            rect_x = padding
            rect_y = padding
            drawtext_commands = ",".join([f"drawtext=text='{line}':x={rect_x + text_padding}:y={rect_y + text_padding + fontsize * i}:fontsize={fontsize}:fontcolor=white@0.8:fontfile={font_path}" for i, line in enumerate(lines)])

            output_file = os.path.join(output_folder, video)
            logger.info(f"Salvataggio del video elaborato in: {output_file}")
            
            subprocess.run([
                'ffmpeg', '-i', video_path,
                '-vf', f"drawbox=x={rect_x - padding}:y={rect_y - padding}:w={rect_width + 2 * padding}:h={rect_height + 2 * padding}:color=black@0.1:t=fill,{drawtext_commands}",
                '-codec:a', 'copy', output_file
            ], check=True)

        logger.info(f"Video elaborati e salvati nella cartella {output_folder}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Errore durante l'elaborazione dei video: {e}")

def main():
    parser = argparse.ArgumentParser(description="Aggiungi overlay di testo ai video in una cartella.")
    parser.add_argument('--input', type=str, required=True, help='Cartella di input contenente i video')
    parser.add_argument('--output', type=str, default='edited', help='Cartella di output per i video elaborati')
    parser.add_argument('--log', action='store_true', help='Abilita il logging')
    parser.add_argument('--logfile', type=str, default='reddit.log', help='Nome del file di log')

    args = parser.parse_args()

    logger = setup_logger(args.logfile if args.log else None)

    process_videos(args.input, args.output, logger)

if __name__ == '__main__':
    main()
