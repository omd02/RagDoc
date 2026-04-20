from fastembed import TextEmbedding

def download():
    print("Downloading fastembed model...")
    # This will download the model to the default cache directory
    TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    print("Download complete.")

if __name__ == "__main__":
    download()
