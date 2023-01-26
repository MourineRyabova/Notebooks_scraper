from scrapy_homework.spiders.notebooks import CompNotikSpider, CompCitilinkSpider, CompKNSSpider
#from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
import sqlite3
import pandas as pd

def main():

    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        #yield runner.crawl(CompCitilinkSpider) #разблокируйте эту строку, если хотите парсить Ситилинк. После нескольких попыток парсинга он банит ip
        yield runner.crawl(CompKNSSpider)
        yield runner.crawl(CompNotikSpider)
        reactor.stop()

    crawl()
    reactor.run() 

    con = sqlite3.connect('computers.db')
    sql = """SELECT  DISTINCT name, price, link, "memory, Gb", "hdd, Gb", (price/100000*(-1) + "memory, Gb"*2 + "hdd, Gb"*4) as rank

                                            FROM computers
                                            WHERE "hdd, Gb" < 1000
                                            GROUP BY name
                                            ORDER BY rank DESC
                                            LIMIT 5"""
    table = pd.read_sql_query(sql, con)
    print("Лучшие 5 ноутбуков, берите - не пожалеете, зуб даю!")
    print(table)


if __name__ == 'main':
    main()
