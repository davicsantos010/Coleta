import scrapy
from urllib.parse import urlparse
import os.path
import csv
import psycopg2

class BlogSpider(scrapy.Spider):
    name = 'blogspider'

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
        start_url = self.file
        yield scrapy.Request(url=start_url, callback=self.parse, meta={'level': 1})

    def parse(self, response):
        level = response.meta['level']
        links = response.css('a::attr(href)').getall()
        new_filtered_links = []

        parsed_url = urlparse(self.file)
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
            yield {'url': link}

        try:
            connection = psycopg2.connect(
                user="postgres",
                password="crazydata",
                host="localhost",
                port="5432",
                database="framecolector"
            )
            cursor = connection.cursor()

            for link in new_filtered_links:
                cursor.execute("INSERT INTO opendata.pages (url, site_id, created_at) VALUES (%s, %s, CURRENT_DATE)", (link, int(self.site_id)))
                connection.commit()

        except (psycopg2.Error, psycopg2.DatabaseError) as error:
            print("Erro ao conectar ou inserir dados no banco de dados PostgreSQL:", error)

        if level < int(self.stop):
            for link in self.filtered_links:
                yield response.follow(link, callback=self.parse, meta={'level': level + 1})
        
        if connection: 
            cursor.close()
            connection.close()

    def url_ends_with_extension(self, url):
        ext = os.path.splitext(url)[1]
        return ext.lower() in self.extensions