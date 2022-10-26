import os
import logging
import pickle
import numpy as np
import pandas as pd
import torch
import sentence_transformers

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config import on_laptop, output_dir, gpt3_token_limit, default_openai_model, available_openai_models

# Set up logging
if  on_laptop:
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO

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
    "https://www.vibecheck.network",
]

web_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

assets = {}

@web_app.on_event('startup')
def load_assets():
    logging.debug('Loading model, tokenizer, archive, cached embeddings to memory')
    model_file = output_dir / 'MiniLM-L12-v2'
    embedding_file = output_dir / "mr_embeddings.pt"
    archive_file = output_dir / "mr_archive.csv"
    tokenizer_file = output_dir / 'gpt2_tokenizer.pkl'

    assets["mr_archive"] = pd.read_csv(archive_file)
    assets["corpus_embeddings"] = torch.tensor(torch.load(embedding_file))
    assets["model"] = sentence_transformers.SentenceTransformer(model_file)
    with open(tokenizer_file, 'rb') as f:
        assets["tokenizer"] = pickle.load(f)


def get_token_count(text, tokenizer):
    return np.sum(tokenizer(text)['attention_mask'])

def format_hit_for_gpt3(hit):
    return f"""Title: {hit["title"]}
    Tags: {hit["tags"]}
    Content: {hit["content"]}
    """
def generate_query_for_gpt3(hits, query, query_length_limit=gpt3_token_limit):
    
    hits_encoded = [format_hit_for_gpt3(hit) for hit in hits]
    article_prompt = f"""A user queried: '{query}'
    
    Please read the following articles and respond truthfully.
    
    """

    footer = f"""
    What do these articles have to say about '{query}'? Respond in detail."""
    
    tokenizer = assets["tokenizer"]

    tokens_so_far = get_token_count(article_prompt, tokenizer) + get_token_count(footer, tokenizer)
    articles_so_far = 0
    for i, hit in enumerate(hits_encoded):
        hit_token_count = get_token_count(hit, tokenizer)
        if tokens_so_far + hit_token_count < query_length_limit:
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

def summarize_results(hits, query, openai_model):
    gpt3_temperature = 0
    
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    print(f'Using OpenAI model {openai_model}')
    if openai_model.find('davinci') != -1:
        gpt3_token_limit = 4096 - 512
    else:
        # Sometimes when debugging I don't use davinci
        gpt3_token_limit = 2048 - 512
 
    gpt3_prompt = generate_query_for_gpt3(hits, query, gpt3_token_limit)
    if gpt3_prompt:
        logger.debug(f'openai_model: {openai_model}')
        response = openai.Completion.create(model=openai_model, prompt=gpt3_prompt, temperature=gpt3_temperature, max_tokens=500)
        logger.info(response)
        
        return response['choices'][0]['text'].strip()
    else:
        return ""

# FastAPI endpoint that wraps summarize_results to be used with FastAPI
@web_app.post("/summarize_results")
async def summarize_results_endpoint(request: Request):
    # Get javascript array hit_uris from the request
    request_json = await request.json()
    query = request_json['query']
    hits = assets["mr_archive"].set_index('link').loc[request_json["hit_uris"]].to_dict('records')
    if 'openai_model' in request_json:
        assert request_json['openai_model'] in available_openai_models, f"Invalid model: {request_json['openai_model']}"
        openai_model = request_json['openai_model']
    else:
        openai_model = default_openai_model

    summary = summarize_results(hits, query, openai_model)
    print(f'Summary: {summary}')
    return {'summary': summary}

def search_mr_for_query(query, top_n_results):
    query_embedding = assets["model"].encode(query, convert_to_tensor=True)
    cos_scores = sentence_transformers.util.cos_sim(query_embedding, assets["corpus_embeddings"])[0]
    top_results = torch.topk(cos_scores, k=top_n_results)
    
    return top_results

def hit_to_json(result_number, score, hit):
    blob = {
        'result_number': result_number,
        'score': score,
        'title': hit["title"],
        'author': hit["author"],
        'date': hit["publish_date"],
        'content': hit["content"],
        'tags': hit["tags"],
        'link': hit["link"]
    }
    return blob


@web_app.get("/search")
async def serve_mr_search_results(query_string):
    top_n_results = 5
    
    results = search_mr_for_query(query_string, top_n_results)

    hits_to_return = []
    for i in range(top_n_results):
        hit = assets["mr_archive"].iloc[results.indices[i].item()]
        blob = hit_to_json(i+1, results.values[i], hit)
        hits_to_return.append(blob)
       
    return {'results': hits_to_return }

