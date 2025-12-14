import threading
import requests
from bs4 import BeautifulSoup

urls = [
    'https://docs.langchain.com/oss/python/langchain/overview',
    'https://docs.langchain.com/oss/python/langchain/philosophy',
    'https://docs.langchain.com/oss/python/langchain/models'
]

def fetch_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(f'Fetched {len(soup.text)} characters from {url}')

threads = []

for url in urls:
    thread = threading.Thread(target=fetch_content, args=(url,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("All pages from web fetched ✅")
