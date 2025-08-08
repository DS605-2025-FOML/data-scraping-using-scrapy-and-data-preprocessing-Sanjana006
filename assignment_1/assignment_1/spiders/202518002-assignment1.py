import scrapy
from ..items import Assignment1Item

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['https://books.toscrape.com/catalogue/page-1.html']

    def parse(self, response):
        all_div_quotes = response.css('article.product_pod')


        for quote_div in all_div_quotes:
            items = Assignment1Item()
            items['book_name'] = quote_div.css('h3 a::attr(title)').extract()
            items['price'] = quote_div.css('p.price_color::text').extract()
            items['stock'] = ''.join(quote_div.css('p.availability::text').extract()).strip()
            items['rating'] = quote_div.css('p::attr(class)').re_first('star-rating\s+(\w+)')

            # items['book_name'] = book_name
            # items['price'] = price
            # items['stock'] = stock
            # items['rating'] = rating

            #store the data
            yield items
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

