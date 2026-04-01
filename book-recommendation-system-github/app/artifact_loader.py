import os
import pandas as pd
import numpy as np
import gdown


BOOKS_FILE_ID = "1xiLi-JzVZzC5Dt7VJJT3M4HHVIy39sQM"
EMBEDDINGS_FILE_ID = "177wmDD_c5826DKBMLqSRgCMY5ii96eVt"


def download_if_needed(books_path, embeddings_path):
    books_url = f"https://drive.google.com/uc?id={BOOKS_FILE_ID}"
    embeddings_url = f"https://drive.google.com/uc?id={EMBEDDINGS_FILE_ID}"

    if not os.path.exists(books_path):
        print("Downloading books.pkl...")
        gdown.download(books_url, books_path, quiet=False)

    if not os.path.exists(embeddings_path):
        print("Downloading embeddings.npy...")
        gdown.download(embeddings_url, embeddings_path, quiet=False)


def load_artifacts(books_path="books.pkl", embeddings_path="embeddings.npy"):
    download_if_needed(books_path, embeddings_path)

    print("Loading books...")
    books = pd.read_pickle(books_path).reset_index(drop=True)

    print("Loading embeddings...")
    embeddings = np.load(embeddings_path)

    return books, embeddings