import praw
import logging
import json
import ffmpeg
import argparse
import configparser
import os

# Configura il logger
def setup_logger(log_to_file, log_file_name):
    logger = logging.getLogger('reddit_video_scraper')
    logger.setLevel(logging.DEBUG)

    # Handler per il file di log, se richiesto
    if log_to_file:
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
    for handler in logger.handlers:
        handler.setFormatter(formatter)

    return logger

# Configura le credenziali dell'API di Reddit
def setup_reddit_client(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    return praw.Reddit(
        client_id=config['reddit']['client_id'],
        client_secret=config['reddit']['client_secret'],
        user_agent=config['reddit']['user_agent'],
        username=config['reddit']['username'],
        password=config['reddit']['password']
    )

import re
import emoji

# Funzione per rimuovere emoji
def remove_emoji(text):
    return emoji.replace_emoji(text, replace='')

# Ottieni i post più votati da un subreddit
def get_funny_posts(subreddit_name, limit_post, logger):
    logger.info(f"Raccolta dei post dal subreddit: {subreddit_name}")
    try:
        subreddit = reddit.subreddit(subreddit_name)
        posts = subreddit.top(time_filter='day', limit=limit_post)
        post_list = []
        video_count = 0
        
        for post in posts:
            # Filtra i post NSFW
            if post.over_18:
                logger.debug(f"Post escluso (NSFW): {post.title}")
                continue

            # Pulisci e controlla il titolo
            cleaned_title = remove_emoji(post.title).strip()
            if not cleaned_title:
                logger.debug(f"Post escluso (titolo vuoto dopo pulizia): {post.title}")
                continue

            logger.debug(f"Controllo post: {post.title}, tipo: {'video' if hasattr(post, 'is_video') and post.is_video else 'non-video'}")
            
            if hasattr(post, 'is_video') and post.is_video:
                video_url = post.media['reddit_video']['fallback_url']
                metadata = {
                    "title": cleaned_title,
                    "url": post.url,
                    "score": post.score,
                    "subreddit": subreddit_name,
                    "id": post.id,
                    "duration": "N/A",
                    "resolution": "N/A"
                }

                # Ottieni la durata e la risoluzione del video
                try:
                    probe = ffmpeg.probe(video_url)
                    format_info = probe['format']
                    duration = float(format_info.get('duration', '0'))
                    metadata["duration"] = duration

                    if duration <= 30:  # Filtra i video che superano i 30 secondi
                        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
                        if video_stream:
                            width = video_stream.get('width', 'N/A')
                            height = video_stream.get('height', 'N/A')
                            metadata["resolution"] = f"{width}x{height}"

                        post_list.append(metadata)
                        video_count += 1
                        if video_count >= limit_post:
                            break
                    else:
                        logger.debug(f"Video escluso (durata > 30s): {video_url}")

                except ffmpeg.Error as e:
                    logger.error(f"Errore durante il probing del video {video_url}: {e}")

        logger.info(f"Raccolti {video_count} video dal subreddit {subreddit_name}")
        return post_list
    except Exception as e:
        logger.error(f"Errore durante la raccolta dei post da {subreddit_name}: {e}")
        return []


# Main function
def main():
    parser = argparse.ArgumentParser(description="Scarica video dai subreddit di Reddit.")
    parser.add_argument('--subreddits', type=str, required=True, help='Subreddits separati da virgola (es. funny,AskReddit)')
    parser.add_argument('--limit', type=int, default=10, help='Numero di post da raccogliere per subreddit')
    parser.add_argument('--output', type=str, default='reddit.json', help='Nome del file JSON di output')
    parser.add_argument('--log', action='store_true', help='Abilita logging in un file')
    parser.add_argument('--logfile', type=str, default='reddit.log', help='Nome del file di log')

    args = parser.parse_args()

    logger = setup_logger(args.log, args.logfile)
    global reddit
    reddit = setup_reddit_client('reddit.config')

    subreddits = args.subreddits.split(',')
    all_posts = []

    for subreddit in subreddits:
        all_posts.extend(get_funny_posts(subreddit, args.limit, logger))

    logger.info(f"Totale post raccolti: {len(all_posts)}")

    try:
        with open(args.output, "w", encoding="utf-8") as f:
            logger.info(f"Salvataggio dei metadati nel file {args.output}")
            json.dump(all_posts, f, ensure_ascii=False, indent=4)
        logger.info("Salvataggio dei metadati completato")
    except Exception as e:
        logger.error(f"Errore durante il salvataggio dei metadati: {e}")

    logger.info("Processo di raccolta dei dati completato")

if __name__ == "__main__":
    main()
