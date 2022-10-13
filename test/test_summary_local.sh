curl \
	--request POST \
	--header "Content-Type: application/json" \
	--data '{"query": "testing", "hit_uris": ["https://marginalrevolution.com/marginalrevolution/2013/03/self-punishment-and-incentives.html", "https://marginalrevolution.com/marginalrevolution/2013/03/assorted-links-748.html"], "openai_model": "text-ada-001"}' \
	--url 'http://127.0.0.1:8000/summarize_results'


