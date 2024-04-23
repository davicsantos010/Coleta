import scrapy
from urllib.parse import urlparse
import os.path
import csv
import sys

class BlogSpider(scrapy.Spider):
    name = 'blogspider'

    # custom_settings = {
    #     'CONCURRENT_REQUESTS': 1 
    # }
    
    extensions = [
    '.txt', '.doc', '.docx', '.odt', '.rtf', '.pdf', '/pdf'
    '.csv', '.xls', '.xlsx', '.ods',
    '.ppt', '.pptx', '.odp', '.key',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg',
    '.mp3', '.wav', '.ogg',
    '.mp4', '.avi', '.mov', '.wmv',
    '.zip', '.rar', '.tar.gz',
    '.html', '.htm', '.css', '.js', '.json', '.xml', '.sql', '.py', '.exe'
    ]
    
    filtered_links = []
    

    def start_requests(self):
        if 'file' not in self.__dict__:
            raise ValueError("O argumento 'file' não foi passado corretamente.")
    

        if 'stop' not in self.__dict__:
            raise ValueError("O argumento'stop' não foi passado corretamente.")
        
        
        # Lê as URLs do arquivo CSV
        with open(self.file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Verifica se a linha não está vazia
                    url = row[0].strip()  # Obtém a URL e remove espaços em branco
                    yield scrapy.Request(url=url, callback=self.parse, meta={'start_url': url, 'level': 1})

    def parse(self, response):
        level = response.meta['level']
        start_url = response.meta['start_url']
        links = response.css('a::attr(href)').getall()
        new_filtered_links = []

        parsed_url = urlparse(start_url)
        domain = parsed_url.netloc

        for i in links: 
            unido = response.urljoin(i)

            parsed_url2 = urlparse(unido)
            domain2 = parsed_url2.netloc

            if domain == domain2:
                if unido not in self.filtered_links:
                    if not '#' in unido and not self.url_ends_with_extension(unido):
                        new_filtered_links.append(unido)
                        self.filtered_links.append(unido)
                        

        for link in new_filtered_links:
            yield {'url': link, 'nivel': level}

        output_file_name = f"PortaisColetados/{domain}.csv"
        with open(output_file_name, 'a', newline='') as file:
                writer = csv.writer(file)
                for link in new_filtered_links:
                    writer.writerow([link])

        if level < int(self.stop):
            for link in self.filtered_links:
                yield response.follow(link, callback=self.parse, meta={'start_url': self.encontrar_url_com_mesmo_dominio(link), 'level': level + 1})

    def url_ends_with_extension(self, url):
        ext = os.path.splitext(url)[1]
        return ext.lower() in self.extensions
    
    def encontrar_url_com_mesmo_dominio(self, link):
        parsed_link = urlparse(link)
        dominio_link = parsed_link.netloc

        url_encontrada = None

        with open('urls.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Verifica se a linha não está vazia
                    url = row[0].strip()  # Obtém a URL e remove espaços em branco
                    parsed_url = urlparse(url)
                    dominio_url = parsed_url.netloc

                    if dominio_url == dominio_link:
                        url_encontrada = url
                        break

        return url_encontrada