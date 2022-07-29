from scrape_trends import *
from scrape_academia import *
from scrape_google_scholar import *
from scrape_resurchify import *
from arxiv import arxiv as arxiv


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