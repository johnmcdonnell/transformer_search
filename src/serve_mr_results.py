import os
import torch
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config import output_dir, logger, gpt3_token_limit

# Set up logging
loglevel = logging.DEBUG

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(loglevel)
ch.setFormatter(formatter)
logger.addHandler(ch)


os.environ["TOKENIZERS_PARALLELISM"] = "false"

web_app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://vibecheck.network",
    "https://www.vibecheck.network"
]

web_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_token_count(text, tokenizer):
    import numpy as np
    return np.sum(tokenizer(text)['attention_mask'])

def format_hit_for_gpt3(hit):
    return f"""Title: {hit["title"]}
    Tags: {hit["tags"]}
    Content: {hit["content"]}
    """
def generate_query_for_gpt3(hits, query):
    import pickle
    
    with open(os.path.join(remote_output_dir, 'gpt2_tokenizer.pkl'), 'rb') as f:
        tokenizer = pickle.load(f)
    
    hits_encoded = [format_hit_for_gpt3(hit) for hit in hits]
    article_prompt = f"""A user queried: '{query}'
    
    Please read the following articles and respond truthfully.
    
    """

    footer = f"""
    What do these articles have to say about '{query}'? Respond in detail."""
    
    tokens_so_far = get_token_count(article_prompt, tokenizer) + get_token_count(footer, tokenizer)
    articles_so_far = 0
    for i, hit in enumerate(hits_encoded):
        hit_token_count = get_token_count(hit, tokenizer)
        if tokens_so_far + hit_token_count < gpt3_token_limit:
            article_prompt += f"""{hit}"""
            tokens_so_far += hit_token_count
            articles_so_far += 1
        elif articles_so_far == 0:
            logger.warn("Haven't yet found an article over the token limit")
            continue
        else:
            logger.warn(f"Articles exceeded token limit, could only include {i} articles")
            break
    if articles_so_far == 0: 
        logger.warn("None of the articles were within GPT3's token limit.")
        return ""
    
    article_prompt += footer
    return article_prompt

def summarize_results(hits, query):
    gpt3_temperature = 0
    
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    gpt3_prompt = generate_query_for_gpt3(hits, query)
    if gpt3_prompt:
        response = openai.Completion.create(model="text-davinci-002", prompt=gpt3_prompt, temperature=gpt3_temperature, max_tokens=500)
        logging.debug(response)
        
        return response['choices'][0]['text'].strip()
    else:
        return ""
    

@web_app.get("/search")
async def serve_mr_search_results(query_string):
    import pandas as pd
    import sentence_transformers
    import torch

    top_n_results = 5

    # Fetch assets
    model = sentence_transformers.SentenceTransformer(os.path.join(remote_output_dir, 'MiniLM-L12-v2'))
    embedding_file = os.path.join(remote_output_dir, "mr_embeddings.pt")
    archive_file = os.path.join(remote_output_dir, "mr_archive.csv")
    corpus_embeddings = torch.tensor(torch.load(embedding_file))
    mr_archive = pd.read_csv(archive_file)

    def search_mr_for_query(query, top_n_results):
        query_embedding = model.encode(query, convert_to_tensor=True)
        cos_scores = sentence_transformers.util.cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_n_results)
        
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
            'tags': hit["tags"],
            'link': hit["link"]
        }
        return blob

    hits_to_return = []
    for i in range(top_n_results):
        hit = mr_archive.iloc[results.indices[i].item()]
        blob = hit_to_json(i+1, results.values[i], hit)
        hits_to_return.append(blob)
   
    # Using a placeholder to spare my OpenAI balance

    summary = summarize_results(hits_to_return, query_string)
    
    return {'results': hits_to_return,
            'summary': summary}

