#academia
from lxml import etree
import pandas as pd 
from pytrends.request import TrendReq 
from bs4 import BeautifulSoup #0.0.1
import requests, lxml, os, json
import re
import time
import numpy as np

class Academia_scraper():

    def __init__(self):
        pass

    def scrape(self):

        #ml
        url_ml= 'https://www.academia.edu/search?q=Machine%20Learning%20PY=(2017-2020)&utf8=%E2%9C%93'
        result_ml = requests.get(url_ml)
        src_ml = result_ml.content
        soup_ml=BeautifulSoup(src_ml,'lxml')

        span_ml = etree.HTML("""<span class="fadeTransition-CountText-cls2-Tctw fadeTransition-CountText-cls1-19yx" style="opacity: 1;">7,021 Papers</span>""")

        for i in span_ml.xpath("//span/text()"):
            print(i)
            ml = i

        #dl
        url_dl= 'https://www.academia.edu/search?q=Deep%20Learning%20PY=(2017-2020)&utf8=%E2%9C%93'
        result_dl = requests.get(url_dl)
        src_dl = result_dl.content
        soup_dl=BeautifulSoup(src_dl,'lxml')

        span_dl = etree.HTML("""<span class="fadeTransition-CountText-cls2-Tctw fadeTransition-CountText-cls1-19yx" style="opacity: 1;">7,485 Papers</span>""")

        for i in span_dl.xpath("//span/text()"):
            print(i)
            dl = i


        #ai
        url_ai= 'https://www.academia.edu/search?q=Artificial%20Intelligence%20PY=(2017-2020)&utf8=%E2%9C%93'
        result_ai = requests.get(url_dl)
        src_ai = result_ai.content
        soup_ai=BeautifulSoup(src_ai,'lxml')

        span_ai = etree.HTML("""<span class="fadeTransition-CountText-cls2-Tctw fadeTransition-CountText-cls1-19yx" style="opacity: 1;">4,759 Papers</span>""")

        for i in span_ai.xpath("//span/text()"):
            print(i)
            ai = i

        #big data
        url = 'https://www.academia.edu/search?pubtype=journal-article&q=Big%20data%20PY=(2017-2020)&tab=0&utf8=%E2%9C%93/robots.txt'
        result = requests.get(url)
        src_bd = result.content
        soup_bigd=BeautifulSoup(src_bd,'lxml')


        span_bigd = etree.HTML("""<span class="fadeTransition-CountText-cls2-Tctw fadeTransition-CountText-cls1-19yx" style="opacity: 1;">9,492 Papers</span>""")

        for i in span_bigd.xpath("//span/text()"):
            print(i)
            bd = i

        ml = re.findall(r'[-+]?\d*\.\d+|\d+', ml)
        ml=(','.join(ml))

        dl = re.findall(r'[-+]?\d*\.\d+|\d+', dl)
        dl=(','.join(dl))

        ai = re.findall(r'[-+]?\d*\.\d+|\d+',ai)
        ai=(','.join(ai))

        bd = re.findall(r'[-+]?\d*\.\d+|\d+', bd)
        bd=(','.join(bd))



        # List of Tuples
        users = [ ('Machine Learning', ml),
                    ('Deep Learning', dl ),
                    ('Artificial Intelligence', ai ),
                    ('Big Data', bd ),
                    ]
        #Create a DataFrame object
        df_academia = pd.DataFrame(  users, 
                            columns = ['Field of Research', 'No of Papers'],
                            index=['1', '2','3','4'])

        ex = df_academia.to_dict('records')

        import dbm, json
        with dbm.open('Academia', 'c') as d:
            d[str(183)] = json.dumps(ex)
            d.sync()

        return(print("Academia.edu scrapped Successfully"))

if __name__ == "__main__":
    obj1 = Academia_scraper()
    obj1.scrape()