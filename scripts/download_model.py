from fastembed import TextEmbedding

def download():
    print("Pre-downloading lightweight embedding model (BAAI/bge-small-en-v1.5)...")
    # This downloads only the ONNX model (~130MB)
    TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    print("Download complete.")

if __name__ == "__main__":
    download()
