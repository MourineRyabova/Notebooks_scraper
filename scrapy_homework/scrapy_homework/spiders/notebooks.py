import scrapy
from scrapy.spiders import CrawlSpider
import re
from datetime import datetime
import time
from ..items import CompItem

#Скрапер для нотика
class CompNotikSpider(CrawlSpider):

    name = 'notebooks_notik'
    allowed_domains = ['notik.ru']
    start_urls = ["https://www.notik.ru/search_catalog/filter/work.htm", 
    "https://www.notik.ru/search_catalog/filter/work.htm?page=2", 
    "https://www.notik.ru/search_catalog/filter/universal.htm",
    "https://www.notik.ru/search_catalog/filter/home.htm"]

    for i in range(2,40):
            start_urls.append("https://www.notik.ru/search_catalog/filter/home.htm" +f"?page={i}") 

    base_url = "https://www.notik.ru"

    default_headers = {}

    #При необходимости можно раскомментировать и вывести результаты парсинга в отдельный файл
    #custom_settings = {'FEEDS' : {'notik.csv' : {'format':'csv'}}}

    def scrap_computers(self, response):
        base_url = "https://www.notik.ru"
        for card in response.xpath("//tr[@class='goods-list-table']"):
            price_selector = card.xpath(".//td[@class='glt-cell gltc-cart']")
            price = re.findall(r'\d+', price_selector.xpath(".//b").css("::text").get())
            price = int("".join(price))

            proc_selector = card.xpath(".//td[@class='glt-cell w4']")
            proc_name = proc_selector.xpath(".//strong/text()[1]").get()
            proc = proc_selector.xpath(".//strong/text()[2]").get()
           
            #freq = proc_selector.xpath(".//text()[3]").get()
            freq = re.findall(r'\d+', proc_selector.xpath(".//text()[3]").get())
            freq = int("".join(freq)) 

            mem_selector = card.xpath(".//td[@class='glt-cell w4'][2]")
            mem = re.findall(r'\d+', mem_selector.xpath(".//strong/text()[1]").get())
            mem = int("".join(mem))

            hdd = re.findall(r'\d+', mem_selector.xpath(".//text()[4]").get())
            hdd = int("".join(hdd))

            link_selector = card.xpath(".//td[@class='glt-cell gltc-title show-mob hide-desktop']")
            link = link_selector.xpath(".//a[1]/@href").get()

            name = link_selector.xpath(".//a/text()").get()
            name = name.split(" ")
            name = " ".join(name[0:3])

            item = CompItem(name=name,
                            date=datetime.now(), 
                            price=price, 
                            proc= proc_name + ' ' + proc, 
                            freq=freq, 
                            mem=mem,    
                            hdd=hdd, 
                            link=str(base_url)+str(link))
            yield item

    
    def parse_start_url(self, response, **kwargs):
        url = self.start_urls[0]
        for url in self.start_urls:
            yield response.follow(
                url, callback=self.scrap_computers, headers=self.default_headers
            )

#Скрапер для Ситилинка (нельзя запускать часто без прокси, забанит)
class CompCitilinkSpider(CrawlSpider):

    name = 'notebooks_citi'
    allowed_domains = ['citilink.ru']
    start_urls = ["https://www.citilink.ru/catalog/noutbuki/"]

    for i in range(2,10):
        start_urls.append("https://www.citilink.ru/catalog/noutbuki/" +f"?p={i}")

    default_headers = {}

    custom_settings = {'FEEDS' : {'notebooks.csv' : {'format':'csv'}}}

    def scrap_computers(self, response):
            time.sleep(10)  # С паузой менее 2 сек может не получить данные
            for full_data in response.xpath("//div[@class='ProductCardVerticalLayout ProductCardVertical__layout']"):
                #price_selector = card.xpath(".//td[@class='glt-cell gltc-cart']")
                name_selector = full_data.xpath(".//div[@class='ProductCardVerticalLayout__header']")
                card = name_selector.xpath(".//a[@class=' ProductCardVertical__name  Link js--Link Link_type_default']")
                link = "https://www.citilink.ru" + card.attrib['href']
                full_name = card.attrib['title'].split(",")
                name_1 = full_name[0].split(" ")
                name = " ".join(name_1[1:])  
                freq = full_name[3]
                freq = re.findall(r'\d\.\d', freq)
                freq = "".join(freq)
                freq = int(freq)*1000
                mem = full_name[4]
                mem = re.findall(r'\d+', mem)
                mem = "".join(mem)
                hdd = full_name[5]
                hdd = re.findall(r'\d+', hdd)
                hdd = "".join(hdd)
                price = full_data.xpath(".//div[@class='ProductCardVerticalLayout__footer']")
                price = re.findall(r'\d+', full_data.xpath(".//span[@class='ProductCardVerticalPrice__price-current_current-price js--ProductCardVerticalPrice__price-current_current-price ']")[1].xpath(".//text()").get())
                price = "".join(price)

                item = CompItem(name=name, 
                                date=datetime.now(), 
                                price=price, 
                                proc= '', 
                                freq=freq, 
                                mem=mem,
                                hdd=hdd, 
                                link=link)
                yield item

    def parse_start_url(self, response, **kwargs):
        for url in self.start_urls:
            yield response.follow(
                url, callback=self.scrap_computers, headers=self.default_headers
                )


#Скрапер для КНС
class CompKNSSpider(CrawlSpider):

    name = 'notebooks_kns'
    allowed_domains = ['kns.ru']
    start_urls = ["https://www.kns.ru/catalog/noutbuki/?s_wordext=intel"]

    for i in range(2,21):
        start_urls.append("https://www.kns.ru/catalog/noutbuki/" + f"page{i}" + "/?s_wordext=intel")
    
    base_url = "https://kns.ru/"

    default_headers = {}

    custom_settings = {'FEEDS' : {'kns.csv' : {'format':'csv'}}}

    def scrap_computers(self, response):
            base_url = "https://kns.ru/"
            time.sleep(2)  # С паузой менее 2 сек может не получить данные
            for card in response.xpath("//div[contains(@class, 'item col')]"):
                full_chars = card.xpath(".//div[contains(@class, 'goods-annt')]/text()").get().split(" ")

                freq = float(full_chars[4])*1000

                mem = int(int(full_chars[9])/1000)

                proc = " ".join(full_chars[0:2])

                hdd = full_chars[15]

                name = card.xpath(".//a/span/text()").get().split(" ")
                name = " ".join(name[1:])

                link = base_url + card.xpath(".//a/@href").get()

                price = re.findall(r'\d+', card.xpath("//span[contains(@class, 'price')]/text()").get())
                price = int("".join(price))
                
                item = CompItem(name=name, 
                                date=datetime.now(), 
                                price=price, 
                                proc= proc, 
                                freq=freq, 
                                mem=mem,
                                hdd=hdd, 
                                link=link)
                yield item

    def parse_start_url(self, response, **kwargs):
        for url in self.start_urls:
            yield response.follow(
                url, callback=self.scrap_computers, headers=self.default_headers
                )



#Заготовка для парсинга каждой страницы с товаром в цикле
""" def parse(self, response):
        for card in response.xpath("//tr[@class='hide-mob']//a/@href"):
            yield response.follow(card, callback=self.parse_nout_notik)
        for page in response.xpath("//div[@class='paginator align-left']//a/@href"):
            yield response.follow(page, callback=self.parse)"""

"""Метод parse. Исследуем каждую ссылку на товар и переходим по ней - follow для этого используем. 
Передаем туда каждую ссылку и калбэчим с вызовом нового метода parse_nout_notik. 
В этом методе описаны все xpath селекторы по добыче информации со страницы с ноутбуком.
Дальше исследуем все страницы подобным образом, только вызов в калбэк самой себя, 
т.к. на новой странице нужно снова пройти процедуру изучения всех ноутбуков"""