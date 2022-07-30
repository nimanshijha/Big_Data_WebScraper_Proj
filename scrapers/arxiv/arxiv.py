from scrapper import Scraper
import pandas as pd
import dbm, json

def write_to_db(ex,string):
    ex = ex.to_dict('records')
    number = len(ex)
    with dbm.open('arxiv', 'c') as d:
        d[string] = str(number)
        d.sync()

def run():
    AI = Scraper(category='cs',date_from='2022-07-07',t=10, filters={'categories':['cs.AI']})
    ML = Scraper(category='cs',date_from='2022-07-07',t=10, filters={'categories':['cs.LG']})
    CV = Scraper(category='cs',date_from='2022-07-07',t=10, filters={'categories':['cs.CV']}) #fecthes all papers to current date
    RO = Scraper(category='cs',date_from='2022-07-07',t=10, filters={'categories':['cs.RO']})
    #fecthes all papers to current date#fecthes all papers to current date
    ML = ML.scrape()
    AI = AI.scrape()
    CV = CV.scrape()
    RO = RO.scrape()

    cols = ('id', 'title', 'categories', 'authors')
    ML = pd.DataFrame(ML,columns=cols)
    AI = pd.DataFrame(AI,columns=cols)
    CV = pd.DataFrame(CV,columns=cols)
    RO = pd.DataFrame(RO,columns=cols)
    write_to_db(ML,"ML")
    write_to_db(AI,"AI")
    write_to_db(CV,"CV")
    write_to_db(RO,"RO")

if __name__ == "__main__":
    run()
