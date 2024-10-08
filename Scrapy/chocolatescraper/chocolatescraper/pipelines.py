# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlite3 import adapters
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import mysql.connector

class ChocolatescraperPipeline:
    def process_item(self, item, spider):
        return item



class PriceUSDtoNRP:
    Rate= 176.89
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):
            floatprice = float(adapter.get('price'))
            adapter['price'] = floatprice * self.Rate
            return item
        else:
            raise DropItem(f"Missing price in {item}")
        



class DuplicatePipeline:
    def __init__(self):
        self.name_seen = set()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if adapter['name'] in self.name_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
             self.name_seen.add(adapter['name'])
             return item
        

class SaveToSQL(object):
    def __init__(self):
        self.creaate_connection()

    def create_connection(self):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'Doramon9841',
            database = 'chocolate'
        )
        self.curr = self.connection.cursor() 