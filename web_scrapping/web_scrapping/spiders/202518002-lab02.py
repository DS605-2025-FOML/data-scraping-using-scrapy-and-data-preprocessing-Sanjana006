import scrapy
from ..items import WebScrappingItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        all_div_quotes = response.css('div.quote')

        items = WebScrappingItem()

        for quote_div in all_div_quotes:
            text = quote_div.css('span.text::text').extract_first()
            author = quote_div.css('.author::text').extract_first()
            tags = quote_div.css('.tag::text').extract()

            items['text'] = text
            items['author'] = author
            items['tags'] = tags

            #store the data
            yield items
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)




# import scrapy

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = ['https://quotes.toscrape.com']

#     def parse(self, response):
#         for quote in response.css('div.quote'):
#             yield {
#                 'text': quote.css('span.text::text').get(),
#                 'author': quote.css('small.author::text').get(),
#                 'tags': quote.css('div.tags a.tag::text').getall()
#             }

#         next_page = response.css('li.next a::attr(href)').get()
#         if next_page:
#             yield response.follow(next_page, callback=self.parse)
