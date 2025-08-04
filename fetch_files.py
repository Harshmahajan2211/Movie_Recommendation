import gdown
import os

def download_files():
    files = {
        "model/movie_list.pkl": "1h9e2ATaNGlfRG79_nW344ZNoihN5u972",      # replace with your actual ID
        "model/similarity.pkl": "12CZB0HoG-T28csjdzKXM-YBwmCWaJFte"       # replace with your actual ID
    }

    if not os.path.exists('model'):
        os.makedirs('model')

    for path, file_id in files.items():
        if not os.path.exists(path):
            url = f'https://drive.google.com/uc?id={file_id}'
            print(f"Downloading {path}...")
            gdown.download(url, path, quiet=False)
        else:
            print(f"{path} already exists.")
