from sentence_transformers import SentenceTransformer
import torch


def load_embedding_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"Loading E5 model on {device}...")
    model = SentenceTransformer(
        "intfloat/multilingual-e5-base",
        device=device
    )

    print("Model loaded.")
    return model