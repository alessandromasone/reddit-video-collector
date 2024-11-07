import praw
import datetime

def get_top_posts(subreddits, period='day', limit=10, media_type=None):
    # Crea un'istanza di Reddit API con praw
    reddit = praw.Reddit(
        client_id='DiyPwdEEdIuuiS389RpIEA',         # Sostituisci con il tuo client_id
        client_secret='48jgPmrj1MkaF_07h746H8Ae83Dl5A', # Sostituisci con il tuo client_secret
        user_agent='Downloader 1.0 by /u/AlessandroMasone'        # Sostituisci con il tuo user_agent
    )

    # Definisci un dizionario per raccogliere i risultati
    top_posts = {}

    # Definisci la mappa dei periodi per l'API di Reddit
    period_mapping = {
        'hour': 'hour',
        'day': 'day',
        'week': 'week',
        'month': 'month',
        'year': 'year',
        'all': 'all'
    }
    
    if period not in period_mapping:
        raise ValueError(f"Periodo non valido. I periodi validi sono: {list(period_mapping.keys())}")

    # Cicla attraverso ogni subreddit fornito
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)

        # Ottieni i post più votati del periodo specificato
        top_posts[subreddit_name] = []
        
        for post in subreddit.top(time_filter=period_mapping[period], limit=limit):
            # Se il filtro per media è 'image', aggiungi solo post che contengono immagini
            if media_type == 'image' and (post.url.endswith('.jpg') or post.url.endswith('.jpeg') or post.url.endswith('.png')):
                top_posts[subreddit_name].append({
                    'title': post.title,
                    'url': post.url,
                    'subreddit' : subreddit_name
                })
            # Se il filtro per media è 'video', aggiungi solo post che contengono video
            elif media_type == 'video' and ('v.redd.it' in post.url or 'youtube.com' in post.url):
                top_posts[subreddit_name].append({
                    'title': post.title,
                    'url': post.url,
                    'subreddit' : subreddit_name
                })
            # Se nessun filtro media è specificato, aggiungi tutti i post
            elif media_type is None:
                top_posts[subreddit_name].append({
                    'title': post.title,
                    'url': post.url,
                    'subreddit' : subreddit_name
                })

    return top_posts