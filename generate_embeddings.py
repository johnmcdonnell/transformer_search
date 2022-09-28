import numpy as np
import pandas as pd
import torch
import sentence_transformers

def identify_tensor_device():
    if torch.backends.mps.is_available():
        device = "mps"
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    return device

device = identify_tensor_device()

# Concatenate title with text
def concatenate_title_text(row):
    return f'''Title: {row["title"]}
    Tags: {', '.join(row["tags"])}
    Content: {row["content"]}'''


if __name__ == '__main__':
    # Load the model
    #model = sentence_transformers.SentenceTransformer('msmarco-distilbert-base-v4', device=device)
    model = sentence_transformers.SentenceTransformer('all-MiniLM-L12-v2', device=device)
    model.save('output/MiniLM-L12-v2')

    # Load the dataset
    df = pd.read_csv("output/mr_archive.csv")


    df["concatenated"] = df.apply(concatenate_title_text, axis=1)

    # Fetch embeddings for corpus
    list_to_generate = df["concatenated"].tolist()
    embeddings = model.encode(list_to_generate, show_progress_bar=True)

    print('Embedding shape:', embeddings.shape)

    def test_consistency(first_item_text, embeddings):
        embeddings_test = model.encode([first_item_text])
        cos_sims = sentence_transformers.util.cos_sim(embeddings, embeddings_test)
        
        try:
            assert np.argmax(cos_sims) == 0, "First item wasn't the best match with itself"
        except AssertionError:
            print(cos_sims)


    test_consistency(df["concatenated"].head(1)[0], embeddings)
    print('Consistency check passed')


    # Save the embeddings
    torch.save(embeddings, "output/mr_embeddings.pt")

