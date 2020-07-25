# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .db import add_item, init_db


class LamodaPipeline:
    def process_item(self, item, spider):
        item['brand'] = item['brand'].replace('\n                ', '').replace('\n                ', '')
        item['title'] = item['title'].replace('\n                    ', '').replace('\n                ', '')
        item['price'] = item['price'].replace(' ', '')
        add_item(
            brand=item['brand'],
            title=item['title'],
            link=item['link'],
            price=item['price'],
            sizes=item['sizes'],
            sex=item['sex'],
            name_of_table='../lamoda_shoes.db'
        )
        print("Added element!")
        return item
