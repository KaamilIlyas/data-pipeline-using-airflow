import re

def clean_text(text):
    # Normalize whitespace and remove unwanted characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespaces with single space
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.strip()  # Remove leading and trailing whitespace
    return text

def transform_data(articles):
    for article in articles:
        article['title'] = clean_text(article['title'])
        article['description'] = clean_text(article['description'])
    return articles
