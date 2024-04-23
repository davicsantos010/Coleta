import scrapy
from urllib.parse import urlparse
import os.path

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    
    #start_url = 'https://www.tjpb.jus.br/transparencia'
    #start_url = 'http://portaltransparencia.belem.pa.gov.br/'
    start_url = 'http://www.transparencia.am.gov.br/'

    #start_url = 'https://dados.ac.gov.br/dataset'

    parsed_url = urlparse(start_url)
    domain = parsed_url.netloc

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
        yield scrapy.Request(url=self.start_url, callback=self.parse, meta={'level': 1})

    def parse(self, response):
        level = response.meta['level']
        links = response.css('a::attr(href)').getall()
        new_filtered_links = []


        for i in links: 
            unido = response.urljoin(i)

            parsed_url2 = urlparse(unido)
            domain2 = parsed_url2.netloc

            if self.domain == domain2:
                if unido not in self.filtered_links:
                    if not '#' in unido and not self.url_ends_with_extension(unido):
                        new_filtered_links.append(unido)
                        self.filtered_links.append(unido)
                        

        for link in new_filtered_links:
            yield {'url': link}

        if level < 2:
            for link in self.filtered_links:
                yield response.follow(link, callback=self.parse, meta={'level': level + 1})

    def url_ends_with_extension(self, url):
        ext = os.path.splitext(url)[1]
        return ext.lower() in self.extensions