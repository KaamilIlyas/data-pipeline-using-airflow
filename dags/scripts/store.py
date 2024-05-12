import json
import os

def store_data(articles, filename):
    # Save the articles to a file
    with open(filename, 'w') as f:
        json.dump(articles, f, indent=4)
    
    # Ensure that the file is tracked by DVC
    if not os.path.exists('.dvc'):
        # Only initialize DVC if it hasn't been done in this project directory
        os.system('dvc init')
    
    # Add the file to DVC tracking
    os.system(f'dvc add {filename}')
    
    # Commit changes to git (optional, if you want to keep the dvc files in git)
    os.system(f'git add {filename}.dvc .gitignore')
    os.system(f'git commit -m "Add/update {filename}"')

    # Push the file to the DVC remote
    os.system(f'dvc push {filename}')

def main(articles):
    store_data(articles, 'articles.json')

if __name__ == "__main__":
    # Example articles data
    articles = [
        {'title': 'Example Title 1', 'link': 'http://example.com/1', 'description': 'Description 1'},
        {'title': 'Example Title 2', 'link': 'http://example.com/2', 'description': 'Description 2'},
    ]
    main(articles)
