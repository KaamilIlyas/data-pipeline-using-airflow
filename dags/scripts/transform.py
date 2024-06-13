import re
import json

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespaces with single space
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.strip()  # Remove leading and trailing whitespace
    return text

def transform_data(articles):
    # Add logging to check the type and content of articles
    print(f"Received articles: {articles}")
    print(f"Type of articles: {type(articles)}")
    
    # Deserialize JSON if articles is a string
    if isinstance(articles, str):
        articles = json.loads(articles)

    for article in articles:
        article['title'] = clean_text(article['title'])
        article['description'] = clean_text(article['description'])
    
    print(f"Transformed articles: {articles}")
    return articles
