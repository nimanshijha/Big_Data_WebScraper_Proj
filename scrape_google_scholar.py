import pandas as pd 
from bs4 import BeautifulSoup #0.0.1
import requests, lxml, os, json
import re
import time
import numpy as np

class Gscholar_scraper():
    def __init__(self):
        pass    
    
    def scrape_url(self):
        """
        Scrape data from URL
        """
        url= 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&as_ylo=2017&as_yhi=2021&q=Artificial+Intelligence+topics&btnG='
    
        
        headers = {'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36'}

        seconds =  round((30-20)*np.random.random()+20)
        print("Sleeping {} seconds to avoid bot detection".format(seconds))
        time.sleep(seconds) 
        
        response = requests.get(url, headers=headers)
        self.soup = BeautifulSoup(response.content,'lxml')
        
        if "Our systems have detected unusual traffic from your computer network" in str(self.soup):
            print ("Google has blocked this computer for a short time (24h?) because it has detected this scraping script.")
            
        
        return self.soup

    def parse_soup(self):
        
        """"""
        
        df_list = []
        num_articles = len(self.soup.select('[data-lid]'))
        
        for item in self.soup.select('[data-lid]'):
            #print(item)
            try:
                # extarct from HTML
                title = [item.select('h3')[0].get_text()]
                title = [x.replace('[HTML][HTML] ', "") for x in title]
                title = [x.replace('[PDF][PDF] ', "") for x in title]
                link = [item.select('a')[0]['href']]
                abstract = [item.select('.gs_rs')[0].get_text()]
                info = item.select('.gs_a')[0].get_text()

                # parse info
                info_split = info.split("- ")
                first_author = [info_split[0].split(", ")[0]]
                website = [info_split[len(info_split)-1]]

                
                if len(info_split) == 3:
                    journal = info_split[1].split(", ")
                    if len(journal) == 2:
                        journal_name = [journal[0]]
                        journal_year = [journal[1]]
                    else:
                        journal_year = [journal[0]]
                        journal_name = ['unknown']
                else:
                    journal_year = ['0000']
                    journal_name = ['unknown']
                article = [*title, *journal_year , *first_author, *website, *journal_name, *link]
                article = [x.strip(' ') for x in article]
                article = [x.replace('\xa0', "") for x in article]
                article = [x.replace('…', "") for x in article]

            except Exception as e:
                #raise e 
                print('==cant parse this soup')            
                article=[]
                
            df_list.append(article)  
            
        return(df_list)

    def df_gen(self):

        
        total_df = pd.DataFrame() # scrape 10 pages by 10 results in each
        for i in range(0, 220, 10):
            print("Results from {} to {}".format(i, i+9))
            soup_data = self.scrape_url()
            df_list = self.parse_soup()
            df = pd.DataFrame(df_list, columns=['title', 'year', 'first_author', 'website', 'journal_name', 'link'])
            df['page_no'] = i
            total_df = pd.concat([total_df,df]).drop_duplicates()

        total_df.to_csv(r"C:\Users\DELL\Desktop\test\test_gs.csv") 

        return total_df       