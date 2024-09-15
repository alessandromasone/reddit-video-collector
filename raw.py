import os
import platform
import subprocess

def run_script(script_name, *args):
    # Determina il percorso dello script (assume che main.py si trovi nella stessa directory degli altri script)
    script_path = os.path.join(os.getcwd(), script_name)
    command = ['python' if platform.system() == 'Windows' else 'python3', script_path] + list(args)
    
    try:
        print(f"Running {' '.join(command)}...")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    # Esegue gli script con i parametri specificati
    run_script('download_reddit.py', '--subreddits', 'funny,AskReddit,memes,dankvideos', '--limit', '100', '--log')
    run_script('download_videos.py', '--jsonfile', 'reddit.json', '--log')
    run_script('check_audio.py', '--input', 'download', '--log')
    run_script('add_overlay.py', '--input', 'download', '--output', 'edited', '--log')
    run_script('concat_videos.py', '--input', 'edited', '--output', 'output.mp4', '--log')

if __name__ == "__main__":
    main()
