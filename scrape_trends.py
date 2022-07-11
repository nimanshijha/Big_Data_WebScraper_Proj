import pandas as pd 
from pytrends.request import TrendReq 


class Trend_scraper():

    def __init__(self):
        pass
        
    def scrape(self):
        pytrends = TrendReq(hl='en-US', tz = 360)

        keyword_list = ['Big Data']
        pytrends.build_payload(keyword_list, cat=0, timeframe='today 5-y', geo='', gprop='')

        # Interest by Region
        dict_data = pytrends.interest_by_region(resolution='COUNTRY').to_dict()
        #print(df.head(10))
        #df = df.reset_index()
        #df.plot(x="geoName", y="Big Data", figsize=(120, 10), kind ="bar")

        nw = dict_data['Big Data']

        self.df = pd.DataFrame(nw.items(),columns =['Country', 'Big_Data'])
        self.df = self.df[self.df.Big_Data!=0]
        self.df.to_csv(r'C:\Users\DELL\Desktop\test\google_trends.csv')

        return(print("Google Trends scrapped Successfully"))