# Reddit Video Collector

Questo progetto raccoglie i video più votati dai subreddit scelti, applica un overlay con il titolo del video e unisce i video in un unico file. Il progetto include un'interfaccia grafica (GUI) per gestire le varie fasi e fornisce anche uno script CLI per eseguire il processo in modo automatico.

## Funzionalità

- Raccoglie i video più votati da uno o più subreddit.
- Scarica i video selezionati e controlla se contengono tracce audio.
- Aggiunge un overlay di testo sui video scaricati con il titolo del post.
- Unisce tutti i video scaricati in un unico file.
- Interfaccia grafica (GUI) per semplificare il processo.

## Requisiti

- Python 3.x
- Librerie richieste (installabili tramite `pip`):
  - `praw`
  - `ffmpeg-python`
  - `RedDownloader`
  - `Pillow`
  - `tkinter`
  
Puoi installare le librerie richieste con:

```bash
pip install -r requirements.txt
```

## Configurazione

Per usare questo script, è necessario creare un file `reddit.config` con le credenziali dell'API di Reddit. Ecco un esempio:

```ini
[reddit]
client_id = xxx
client_secret = xxx
user_agent = xxx
username = xxx
password = xxx
```

Assicurati di sostituire i valori con le tue credenziali personali.

## Utilizzo

### 1. Interfaccia grafica (GUI)

Per avviare l'interfaccia grafica, esegui il comando:

```bash
python main.py
```

L'interfaccia è suddivisa in 5 fasi:

- **Fase 1**: Scarica i post più votati dai subreddit selezionati.
- **Fase 2**: Scarica i video dai post raccolti in formato JSON.
- **Fase 3**: Controlla la presenza di tracce audio nei video scaricati.
- **Fase 4**: Aggiunge un overlay di testo ai video.
- **Fase 5**: Unisce i video in un unico file.

### 2. Avvio rapido con CLI

Se preferisci eseguire il processo in modo automatico, puoi usare lo script `raw.py`. Questo script esegue tutte le fasi di raccolta e unione dei video in un unico passaggio.

Esegui il comando:

```bash
python raw.py
```

### 3. Singole fasi

Puoi anche eseguire manualmente ciascuna fase:

1. Scarica i post:

    ```bash
    python download_reddit.py --subreddits xxx,yyy --limit 10 --output reddit.json --log
    ```

2. Scarica i video:

    ```bash
    python download_videos.py --jsonfile reddit.json --savedir download --quality 720 --log
    ```

3. Controlla la presenza di tracce audio:

    ```bash
    python check_audio.py --folder download --log
    ```

4. Aggiungi overlay ai video:

    ```bash
    python add_overlay.py --input download --output edited --log
    ```

5. Unisci i video:

    ```bash
    python concat_videos.py --input edited --output final_video.mp4 --log
    ```

## Note

- I video senza traccia audio vengono eliminati automaticamente durante la fase di controllo audio.
- La qualità dei video scaricati può essere specificata con il parametro `--quality`.
- I log sono salvati in un file `reddit.log` se abilitati.

## Autore

Questo progetto è stato creato per semplificare la raccolta e la gestione dei video dai subreddit di Reddit.
