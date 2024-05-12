import requests
from bs4 import BeautifulSoup

def extract_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = []


    for link in soup.find_all('a', attrs={'data-testid': ['external-anchor', 'internal-link']}):
        title_element = link.find('h2', attrs={'data-testid': 'card-headline'})
        description_element = link.find('p', attrs={'data-testid': 'card-description'})
        if title_element and description_element:
            title = title_element.text.strip()
            description = description_element.text.strip()
            article_link = link['href']
            if not article_link.startswith('http'):
                article_link = 'https://www.bbc.com' + article_link  
            articles.append({'title': title, 'link': article_link, 'description': description})

    return articles

def main():
    bbc_articles = extract_data('https://www.bbc.com')
    


