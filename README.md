# Semantic Search with Transformers


## Python Backend

The backend was built with Modal. It loads saved embeddings and models and executes queries and calls to OpenAI.

For debugging:
```
uvicorn serve_mr_results:web_app --reload
```

To deploy:
```
uvicorn serve_mr_results:web_app
```
