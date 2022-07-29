import pandas as pd 
from bs4 import BeautifulSoup #0.0.1
import requests, lxml, os, json
import re
import time
import numpy as np

class Resurchify_scraper():

    def __init__(self):
        pass

    def scrape(self):
        
        url_re= 'https://www.resurchify.com/find/?query=Big+Data+'
        result_re = requests.get(url_re)
        src_re = result_re.content
        soup_re=BeautifulSoup(src_re,'lxml')


        title_r=[]
        impact_score_r=[]
        h_index_r=[]
        sjr_r=[]
        overall_rank_r=[]
        link_r=[]


        for item in soup_re.find_all('div',attrs={'class':'w3-white w3-container w3-card-4 w3-hover-light-gray'}):
        
            
            title = item.find('h3',attrs={'class':'w3-hover-text-blue heading_h3'})
            if title is not None:
                title = title.text 
                title_r.append(title)
            

            impact_score = item.find('span',attrs={'class':'w3-tag w3-medium w3-sand w3-border w3-margin-bottom'})
            if impact_score is not None:
                impact_score = impact_score.text 
                impact_score = re.findall(r'[-+]?\d*\.\d+|\d+', impact_score)
                impact_score=(','.join(impact_score))
                impact_score_r.append(impact_score)
            

            h_index = item.find('span',attrs={'class':'w3-tag w3-medium w3-pale-green w3-border  w3-margin-bottom'})
            if h_index is not None:
                h_index = h_index.text
                h_index = re.findall(r'[-+]?\d*\.\d+|\d+',  h_index)
                h_index=(','.join(h_index))
                h_index_r.append(h_index)
            

            sjr = item.find('span',attrs={'class':'w3-tag w3-medium w3-pale-blue w3-border w3-margin-bottom'})
            if sjr is not None:
                sjr = sjr.text 
                sjr = re.findall(r'[-+]?\d*\.\d+|\d+', sjr)
                sjr=(','.join(sjr))
                sjr_r.append(sjr)
                

            overall_rank = item.find('span',attrs={'class':'w3-tag w3-medium w3-pale-red w3-border w3-margin-bottom'})
            if  overall_rank is not None:
                overall_rank =  overall_rank.text 
                overall_rank = re.findall(r'[-+]?\d*\.\d+|\d+', overall_rank)
                overall_rank=(','.join(overall_rank))
                overall_rank_r.append(overall_rank)
            
            link = item.a['href']
            link_r.append(link)

        df_resurchify=pd.DataFrame(
            {'Journal Name': title_r,
            'Impact_score': impact_score_r,
            'SJR': sjr_r,
            'Overall_rank': overall_rank_r,
            'Link': link_r
            })

        ex = df_resurchify.to_dict('records')

        import dbm, json
        with dbm.open('resurchify', 'c') as d:
            d[str(183)] = json.dumps(ex)
            d.sync()

        return(print("Resurchify scrapped Successfully"))

if __name__ == "__main__":
    obj1 = Resurchify_scraper()
    obj1.scrape()