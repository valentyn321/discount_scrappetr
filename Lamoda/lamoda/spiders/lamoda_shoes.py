import scrapy
from lamoda.db import add_item
from ..items import LamodaItem

def script_for_adding_pages_to_start_ulrs(entry_list):
    output_list = []
    for url in entry_list:
        for i in range(1, 20):
            output_list.append(url+'&page='+str(i))
    return output_list



class LamodaShoesSpider(scrapy.Spider):
    name = 'lamoda_shoes'
    page_number = 2
    input_your_urls_here = [
        'https://www.lamoda.ua/c/17/shoes-men/?display_locations=outlet&is_sale=1&brands=1061%2C1163%2C6158%2C2047%2C1107%2C1063%2C18583%2C573',
        'https://www.lamoda.ua/c/15/shoes-women/?display_locations=outlet&is_sale=1&brands=1061%2C1163%2C6158%2C2047%2C1107%2C1063%2C18583'
    ]
    start_urls = script_for_adding_pages_to_start_ulrs(input_your_urls_here)

    def parse(self, response):

        one_item = LamodaItem()

        sale = response.css('div.products-list-item')

        for item in sale:
            brand = item.css('div.products-list-item__brand::text')[0].extract()
            title = item.css('span.products-list-item__type::text')[0].extract()
            link = item.css('a.products-list-item__link::attr(href)')[0].extract()
            price = item.css('span.price__new::text')[0].extract()
            sizes = item.css('a.products-list-item__size-item::text').extract()
           
            one_item['brand'] = brand
            one_item['title'] = title
            one_item['link'] = response.urljoin(link)
            one_item['price'] = price
            one_item['sizes'] = '; '.join(sizes)
            if 'shoes-men' in response.url:
                one_item['sex'] = 'муж'
            else:
                one_item['sex'] = 'жен'

            yield one_item