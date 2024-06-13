import json
import os
import subprocess

def store_data(articles, filename='articles.json'):
    if isinstance(articles, str):
        import json
        articles = json.loads(articles)
        
    with open(filename, 'w') as f:
        json.dump(articles, f, indent=4)

    if not os.path.exists('.dvc'):
        os.system('dvc init')

    subprocess.run(['dvc', 'add', filename], check=True)
    subprocess.run(['git', 'add', f'{filename}.dvc', filename, '.gitignore'], check=True)
    subprocess.run(['git', 'commit', '-m', f'Add/update {filename}'], check=True)
    subprocess.run(['git', 'push'], check=True)
    subprocess.run(['dvc', 'push'], check=True)

def main(articles):
    store_data(articles)
