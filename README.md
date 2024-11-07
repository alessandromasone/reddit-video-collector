# Reddit Video Collector

**Reddit Video Collector** è uno script Python progettato per scaricare e unire automaticamente i video più popolari da subreddit specificati, in un unico file video. Non necessita dell'API di Reddit, lo script recupera i post video più apprezzati in un dato periodo di tempo e li unisce in un singolo video per una visualizzazione semplice e immediata.

## Funzionalità principali
- **Scarica i video da Reddit**: Estrae i video dai subreddit più popolari come `funny`, `AskReddit`, `memes`, e `dankvideos`, con la possibilità di personalizzare i subreddit.
- **Filtra per periodo**: Puoi scegliere tra vari periodi di tempo (ora, giorno, settimana, mese, anno, o tutti i tempi) per raccogliere i post più votati.
- **Unisci i video**: I video scaricati vengono uniti automaticamente in un unico file, pronto per essere visualizzato.
- **Facile da usare**: Grazie alla riga di comando, puoi facilmente personalizzare il comportamento dello script senza modificare il codice.

## Installazione

1. **Clona il repository**:
   ```bash
   git clone https://github.com/alessandromasone/reddit-video-collector.git
   cd reddit-video-collector
   ```

2. **Installazione ffmpeg**:
    FFmpeg è necessario per unire i video scaricati. Installalo e aggiungerlo alla tua variabile di ambiente PATH

3. **Configura l'ambiente**:
   Se vuoi configurare un ambiente virtuale, esegui il file env.bat, che creerà l'ambiente virtuale per il progetto o ti permetterà di entrare in un ambiente già esistente:
   ```bash
   env.bat
   ```

4. **Installa le dipendenze**:
   Assicurati di avere Python 3.x installato, quindi esegui:
   ```bash
   pip install -r requirements.txt
   ```

5. **Esegui lo script**:
   Puoi avviare lo script utilizzando il file batch run.bat, che eseguirà automaticamente il programma e rimuoverà eventuali cartelle `__pycache__` nel progetto:
   ```bash
   run.bat
   ```

## Utilizzo

Lo script può essere eseguito dalla riga di comando con i seguenti parametri:

### Sintassi:
```bash
python reddit_video_collector.py -s <subreddits> -p <period>
```

### Parametri:
- `-s` o `--subreddits`: Una lista di subreddit separati da virgola da cui scaricare i video. (Es. `funny,memes,dankvideos`). Il valore predefinito è `funny,AskReddit,memes,dankvideos`.
- `-p` o `--period`: Il periodo per i top post. Può essere uno dei seguenti: `hour`, `day`, `week`, `month`, `year`, `all`. Il valore predefinito è `day`.

### Esempio:
```bash
python reddit_video_collector.py -s "funny,memes,dankvideos" -p "week"
```

Questo comando scaricherà i video più popolari della settimana dai subreddit `funny`, `memes` e `dankvideos` e li unirà in un unico file video.

## Contributi

Se desideri contribuire a questo progetto, sentiti libero di aprire un **issue** o inviare una **pull request**.

## Licenza

Distribuito sotto la **MIT License**. Vedi il file [LICENSE](LICENSE) per maggiori dettagli.