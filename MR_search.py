import os
import re
import html2text
from bs4 import BeautifulSoup

text_maker = html2text.HTML2Text()

def remove_html_tags(string):
    #return BeautifulSoup(string, "lxml").text
    return text_maker.handle(string)

def traverse_wp_articles(root_dir):
    for root, dirs, files in os.walk(root_dir):
        #import pdb; pdb.set_trace()
        for file in files:
            filename = file.split('/')[-1]
            # regex checking file name contains letters
            if filename.endswith(".html") and not re.match(r'^\d+\.html$', filename) and not filename=='.html':
                file_path = os.path.join(root, file)
                yield file_path


mr_endtext_regexp = re.compile('\nThe post.*appeared first on Marginal REVOLUTION')

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

    def string_for_model(self):
        formatted_repr = f"""Title: {self.title}
        Author: {self.author}
        Content: {self.content}"""

        return formatted_repr
    
    def __repr__(self):
        return f'<WP_Article title={self.link}>'


root_dir = '/Users/jvm/Development/web_crawling/marginal_revolution/marginalrevolution.com/marginalrevolution'

articles = []
for filename in traverse_wp_articles(root_dir):
    article = WP_Article(filename)
    articles.append(article)

print('Total articles:', len(articles))
#        import pdb; pdb.set_trace()




