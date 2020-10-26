# Avaliação 1 Questão 2

# Implemente um programa que receba um produto como parâmetro e liste o nome e
# o preço de todos esses produtos no mercado livre, com paginação incluída.
# Busque uma forma de passar um parâmetro para o seu programa.

# scrapy crawl PegarProdutosMercadoLivre  -s LOG_ENABLED=False -o pesquisa_produtos_mercado_livre.csv -a pesquisa=livro-python

import scrapy


class PegarprodutosmercadolivreSpider(scrapy.Spider):

    name = 'PegarProdutosMercadoLivre'
    proxima_pagina = 1

    def __init__(self, pesquisa=None, *args, **kwargs):
        super(PegarprodutosmercadolivreSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://lista.mercadolivre.com.br/%s' % pesquisa]

    def parse(self, response):
        # produtos = response.xpath('/html/body/main/div[1]/div/section/ol/li')
        produtos = response.xpath('.//ol[contains(@class,"section") and contains(@class,"search-results")]/li')

        if self.proxima_pagina == 1:
            print('Iniciando crawler...')
            print('Lendo página 1')

        for produto in produtos:

            link_detail = produto.xpath('.//a[contains(@class,"item__js-link")]/@href').extract_first() 
       
            yield scrapy.Request(
                url=link_detail,
                callback=self.parse_detail
            )

        next_page = response.xpath(
            './/a[contains(@class,"prefetch")]/@href')

        if next_page:

            self.proxima_pagina += 1
            print('Lendo página %s' % self.proxima_pagina)

            yield scrapy.Request(
                url=next_page.extract_first(),
                callback=self.parse
            )
        else:
            print('Crawler concluído!')

    def parse_detail(self, response):

        descricao = (response.xpath(
            './/h1[contains(@class,"item-title__primary")]/text()').extract_first()).strip()

        preco_fracao = response.xpath(
            './/span[@class="price-tag-fraction"]/text()').extract_first()

        preco_decimal = response.xpath(
            './/span[@class="price-tag-cents"]/text()').extract_first()

        preco = float(preco_fracao + '.' +
                      ('00' if preco_decimal == None else preco_decimal))

        produto_nota = response.xpath(
            './/span[@class="review-summary-average"]/text()').extract_first()

        opnioes = response.xpath(
            '//div[@class="review-summary-average-legend"]/span[contains(text(), "Média entre")]/following-sibling::span/text()').extract_first()

        disponibilidade = response.xpath(
            './/span[@class="dropdown-quantity-available"]/text()').extract_first()

        imagem = response.xpath(
            './/div/figure[contains(@class, "gallery-image-container")]/a/img/@src').extract_first()
        imagem = 'sem imagem' if imagem == None else imagem

        yield {
            'produto': descricao,
            'preço': preco,
            'nota': produto_nota,
            'opniões': opnioes,
            'disponibilidade': disponibilidade,
            'imagem': imagem
        }