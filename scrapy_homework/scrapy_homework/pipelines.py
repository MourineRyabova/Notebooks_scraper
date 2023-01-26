# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class SimpleSqlitePipeline:
    
    def __init__(self):
        self.con = sqlite3.connect('computers.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS computers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date DATETIME,
            price INTEGER,
            proc TEXT,
            'freq, MHz' INTEGER,
            'memory, Gb' INTEGER,
            'hdd, Gb' INTEGER,
            link TEXT

        );
        """)


    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT INTO computers (name, date, price, proc, 'freq, MHz', 'memory, Gb', 'hdd, Gb', link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            item['name'],
            item['date'],
            item['price'],
            item['proc'],
            item['freq'],
            item['mem'],
            item['hdd'],
            item['link']
        ))

        self.con.commit()
        return item


