# import scrapy
# from urllib.parse import urlparse

# class BlogSpider(scrapy.Spider):
#     name = 'blogspider'

#     def start_requests(self):
#         # Insira aqui o link inicial do portal
#         start_url = 'https://www.tjpb.jus.br/transparencia'
#         filtered_links = []
#         domain = urlparse(start_url).netloc
#         yield scrapy.Request(url=start_url, callback=self.parse, meta={'level': 1, 'visited_urls': set()})

#     def parse(self, response):
#         level = response.meta['level']
#         domain = response.meta['domain']
#         visited_urls = response.meta['visited_urls']
#         # Extrair todos os links da página atual
#         links = response.css('a::attr(href)').getall()

#         for i in links: 
#             unido = response.urljoin(i)

#             if self.start_urls in unido:
#                 if not '#' in unido:
#                     self.filtered_links.append(unido)


#         # Filtrar links que não foram visitados anteriormente
#         self.filtered_links = [link for link in self.filtered_links if link not in visited_urls]

#         # Adicionar os links filtrados ao conjunto de URLs visitadas
#         visited_urls.update(self.filtered_links)

#         # Aqui você pode fazer a avaliação dos links, salvar em um arquivo, banco de dados, etc.

#         # Yield dos links filtrados
#         for link in self.filtered_links:
#             yield {'url': link}

#         # Se o nível atual for menor que 5, faça outra solicitação para cada link encontrado
#         if level < 3:
#             for link in self.filtered_links:
#                 yield response.follow(link, callback=self.parse, meta={'level': level + 1, 'visited_urls': visited_urls})