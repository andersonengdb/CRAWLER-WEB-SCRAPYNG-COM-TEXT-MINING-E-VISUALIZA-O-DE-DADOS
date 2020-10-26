# Avaliação 1 Questão 1

# Implemente um programa que entre no site do UOL e imprima apenas a seguinte
# mensagem: A cotação atual do dólar é: <cotação>, onde <cotação> vai ser o valor
# capturado do site no momento. Procure uma forma de omitir as mensagens de log na
# execução do seu programa para aparecer apenas essa mensagem como saída.

# scrapy crawl PegarCotacaoDolarUol -s LOG_ENABLED=False

import scrapy


class PegarcotacaodolaruolSpider(scrapy.Spider):
    name = 'PegarCotacaoDolarUol'
    start_urls = ['https://www.uol.com.br/']

    def parse(self, response):
        dolarCotacaoAtual = response.css(
            ".HU_currency__quote.HU_currency__quote-up::text"
        ).extract_first()

        print('A cotação atual do dólar é:', dolarCotacaoAtual) 