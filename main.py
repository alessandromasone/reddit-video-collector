import os
import tempfile
import argparse
import json
import datetime
from scraper import scarica_clip, get_top_posts, union_video_ffmpeg


# Funzione principale
def main(subreddits, period):
    # Per ottenere solo video
    top_posts = get_top_posts(subreddits, period, limit=10, media_type='video')

    # Crea una cartella temporanea
    with tempfile.TemporaryDirectory() as temp_dir:
        # Inizializziamo il contatore per il nome del file
        counter = 1

        for subreddit, posts in top_posts.items():
            for post in posts:
                # Crea il nome del file con il contatore
                nome_file = f"video{counter}"

                # Scarica il video nella cartella temporanea
                path = scarica_clip(
                    url=post['url'],
                    destinazione=temp_dir,
                    nome_file=nome_file
                )

                # Incrementa il contatore per il prossimo file
                counter += 1

        # Ottieni la data di oggi nel formato desiderato (ad esempio, YYYY-MM-DD)
        oggi = datetime.datetime.now().strftime("%Y-%m-%d")

        # Usa la data di oggi come nome del file
        union_video_ffmpeg(temp_dir, f"{oggi}.mp4")


def parse_args():
    parser = argparse.ArgumentParser(description="Scarica e unisci video da Reddit")
    parser.add_argument('-s', '--subreddits', type=str, help="Lista di subreddit separati da virgola", 
                        default="funny,AskReddit,memes,dankvideos")
    parser.add_argument('-p', '--period', type=str, choices=['hour', 'day', 'week', 'month', 'year', 'all'], 
                        help="Periodo per ottenere i top post", default='day')
    return parser.parse_args()


if __name__ == "__main__":
    # Ottieni i parametri dalla linea di comando
    args = parse_args()

    # Ottieni i subreddit e il periodo dalla linea di comando, o usa i valori di default
    subreddits = args.subreddits.split(',') if args.subreddits else ['funny', 'AskReddit', 'memes', 'dankvideos']
    period = args.period if args.period else 'day'

    # Esegui la funzione principale
    main(subreddits, period)
