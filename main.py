from scrapers.scrape_trends import *
from scrapers.scrape_academia import *
from scrapers.scrape_google_scholar import *
from scrapers.scrape_resurchify import *
from scrapers.arxiv import arxiv as arxiv


def main():
    #scrape google trends
    obj1 = Trend_scraper()
    obj1.scrape()

    #scrape google scholar 
    obj2 = Gscholar_scraper()
    obj2.df_gen()

    #scrape Academia.edu
    obj3 = Academia_scraper()
    obj3.scrape()

    #scrape resurchify
    obj4 = Resurchify_scraper()
    obj4.scrape()

    #Scrape Arxiv
    arxiv.run()

    
if __name__ == "__main__":
    main()