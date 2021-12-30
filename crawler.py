import requests
from bs4 import BeautifulSoup
from requests.api import request

class Content:

    def __init__(self, topic, url, title, body):
        """Classe-base comum para todos os artigos/páginas"""
        self.topic = topic
        self.title = title
        self.body = body
        self.url = url

    def print(self):
        """Uma função flexível de exibição controla a saída"""
        print(f'New article found for topic: {self.topic}')
        print(f'TITLE: {self.title}')
        print(f'BODY: {self.body}')
        print(f'URL: {self.url}')

class Website:
    """Contém informações sobre a estrutura do site"""
    def __init__(self, name, url, search_url, result_listing, result_url, absolute_url, title_tag, body_tag):
        self.name = name
        self.url = url
        self.search_url = search_url
        self.result_listing = result_listing
        self.result_url = result_url
        self.absolute_url = absolute_url
        self.title_tag = title_tag
        self.body_tag = body_tag

class Crawler:

    def get_page(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safe_get(self, page_obj, selector):
        child_obj = page_obj.select(selector)
        if child_obj is not None and len(child_obj) > 0:
            return child_obj[0].get_text()
        return ""

    def search(self, topic, site):
        "Pesquisa um dado site em busca de um dado tópico e registra todas as páginas encontradas"

        soup = self.get_page(site.search_url + topic)
        search_results = soup.select(site.result_listing)
        for result in search_results:
            url = result.select(site.result_url)[0].attrs['href']
            # Verifica se é um URL relativo ou absoluto
            if (site.absolute_url):
                soup = self.get_page(url)
            else:
                soup = self.get_page(site.url + url)
            if soup is None:
                print('Something was wrong with that page or URL. Skipping!')
                return
            title = self.safe_get(soup, site.title_tag)
            body = self.safe_get(soup, site.body_tag)
            if title != '' and body != '':
                content = Content(topic, title, body, url)
                content.print()

if __name__ == '__main__':
    crawler = Crawler()
    
    site_data = [
        [
            "O'Reilly Media", 'http://oreilly.com',
            'https://ssearch.oreilly.com/?q=',
            'article.product-result',
            'p.title a',
            True,
            'h1',
            'section#product-description'
        ],
        [
            'Reuters',
            'http://reuters.com',
            'http://www.reuters.com/search/bews?blob=',
            'div.search-result-content',
            'h3.search-result-title a',
            False,
            'h1',
            'div.StandardArticleBody_body_1gnLA'
        ],
        [
            'Brookings',
            'http://brookings.edu/'
            'https://www.brookings.edu/search/?s=',
            'div.list-content article',
            'h4.title a',
            True,
            'h1',
            'div.post-body'
        ]
    ]

    sites = []
    for row in site_data:
        name, url, search_url, result_listing, result_url, absolute_url, title_tag, body_tag = row
        sites.append(Website(name, url, search_url, result_listing, result_url, absolute_url, title_tag, body_tag))
        topics = ['python', 'data science']
        for topic in topics:
            print(f'GETTING INFO ABOUT: {topic}')
            for target_site in sites:
                crawler.search(topic, target_site)