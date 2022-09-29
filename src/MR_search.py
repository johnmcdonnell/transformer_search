import os
import re
#import html2text
from bs4 import BeautifulSoup
import pandas as pd
import torch
#import sentence_transformers

output_dir = 'output'

def traverse_wp_articles_dir(root_dir):
    for root, dirs, files in os.walk(root_dir):
        #import pdb; pdb.set_trace()
        for file in files:
            filename = file.split('/')[-1]
            # regex checking file name contains letters
            if filename.endswith(".html") and not re.match(r'^\d+\.html$', filename) and not filename=='.html':
                file_path = os.path.join(root, file)
                yield file_path


def article_to_dict(file_path):
    with open(file_path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
        title = soup.find('h1', {'class': 'entry-title'}).text
        author = soup.find('span', {'class': 'author'}).text
        publish_date = soup.find('time', {'class': 'entry-date'}).attrs['datetime']

        content_soup = soup.find('div', {'class': 'entry-content'})
        content = content_soup.text
        outlinks = [a.attrs['href'] for a in content_soup.find_all('a', href=True)]

        tags = [a.text for a in soup.find_all('li', {'class': 'text'})]
        link = soup.find('link').attrs['href']
        local_path = filename

        return {
            'title': title,
            'author': author,
            'publish_date': publish_date,
            'content': content,
            'outlinks': outlinks,
            'tags': tags,
            'link': link,
            'local_path': local_path
        }

class WP_Article():
    def __init__(self, filename):
        with open(filename, 'r') as f:
            raw_html = f.read()
            
        soup = BeautifulSoup(raw_html, "lxml")

        self.title = soup.find('h1', {'class': 'entry-title'}).text
        self.author = soup.find('span', {'class': 'author'}).text
        self.publish_date = soup.find('time', {'class': 'entry-date'}).attrs['datetime']

        content_soup = soup.find('div', {'class': 'entry-content'})
        self.content = content_soup.text
        self.outlinks = [a.attrs['href'] for a in content_soup.find_all('a', href=True)]

        self.tags = [a.text for a in soup.find_all('li', {'class': 'text'})]
        self.link = soup.find('link').attrs['href']
        self.local_path = filename

        self.device = identify_tensor_device()
        self.initialize_model()

    def string_for_model(self):
        formatted_repr = f"""Title: {self.title}
        Tags: {self.tags}
        Content: {self.content}
        """
        
        return formatted_repr

    def initialize_model(self):
        self.model = sentence_transformers.SentenceTransformer('msmarco-distilbert-dot-v5')
    
    def get_embeddings(self):
        pass

    def __repr__(self):
        return f'<WP_Article title={self.link}>'


root_dir = '/Users/jvm/Development/web_crawling/marginal_revolution/marginalrevolution.com/marginalrevolution'

articles = []
for filename in traverse_wp_articles_dir(root_dir):
    article = article_to_dict(filename)
    articles.append(article)

    # Concatenate articles into a pandas Dataframe
    df = pd.DataFrame(articles)

    # Save to csv
    df.to_csv(os.path.join(output_dir, 'mr_archive.csv'), index=False)


print('Archived articles count:', len(articles))
#        import pdb; pdb.set_trace()




