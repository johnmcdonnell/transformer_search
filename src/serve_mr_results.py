import os
import modal
import torch
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

#import sentence_transformers

web_app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

web_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


stub = modal.Stub()
image = modal.Image.debian_slim().pip_install(["torch", "pandas", "sentence_transformers"])

# TODO Cache the model so we don't have to load it on each call
# TODO Return properly formatted JSON
# TODO Figure out GPUs (low priority)

# Identify output directory for passing into modal
local_dir = os.path.dirname(os.path.realpath(__file__))
local_output_dir = os.path.join(local_dir, "output")
remote_output_dir = "/root/output"

@web_app.get("/search")
def serve_mr_search_results(query_string):
    import pandas as pd
    import sentence_transformers
    import torch

    top_n_results = 5

    # Fetch assets
    #model = sentence_transformers.SentenceTransformer('all-MiniLM-L12-v2')
    model = sentence_transformers.SentenceTransformer(os.path.join(remote_output_dir, 'MiniLM-L12-v2'))
    embedding_file = os.path.join(remote_output_dir, "mr_embeddings.pt")
    archive_file = os.path.join(remote_output_dir, "mr_archive.csv")
    corpus_embeddings = torch.tensor(torch.load(embedding_file))
    mr_archive = pd.read_csv(archive_file)

    def search_mr_for_query(query, top_n_results):
        query_embedding = model.encode(query, convert_to_tensor=True)
        cos_scores = sentence_transformers.util.cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_n_results)
        print(top_results)
        
        return top_results

    results = search_mr_for_query(query_string, top_n_results)
    
    def hit_to_json(result_number, score, hit):
        blob = {
            'result_number': i+1,
            'score': score,
            'title': hit["title"],
            'author': hit["author"],
            'date': hit["publish_date"],
            'content': hit["content"],
            'link': hit["link"]
        }
        return blob

    hits_to_return = []
    for i in range(top_n_results):
        hit = mr_archive.iloc[results.indices[i].item()]
        blob = hit_to_json(i+1, results.values[i], hit)
        hits_to_return.append(blob)

    return {'results': hits_to_return}

@stub.asgi(image=image,
        mounts=[modal.Mount(local_dir=local_output_dir, remote_dir=remote_output_dir)])
def fastapi_app():
    return web_app


if __name__ == "__main__":
    stub.serve()
