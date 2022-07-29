import datetime
import time
import xml.etree.ElementTree as ET
from typing import Dict, List
from urllib.error import HTTPError
from urllib.request import urlopen

from constants import OAI, ARXIV, BASE
from record import Record


class Scraper(object):
    def __init__(
        self,
        category: str,
        date_from: str = None,
        date_until: str = None,
        t: int = 30,
        timeout: int = 300,
        filters: Dict[str, str] = {},
    ):
        self.cat = str(category)
        self.t = t
        self.timeout = timeout
        DateToday = datetime.date.today()
        if date_from is None:
            self.f = str(DateToday.replace(day=1))
        else:
            self.f = date_from
        if date_until is None:
            self.u = str(DateToday)
        else:
            self.u = date_until
        self.url = (
            BASE
            + "from="
            + self.f
            + "&until="
            + self.u
            + "&metadataPrefix=arXiv&set=%s" % self.cat
        )
        self.filters = filters
        if not self.filters:
            self.append_all = True
        else:
            self.append_all = False
            self.keys = filters.keys()

    def scrape(self) -> List[Dict]:
        url = self.url
        ds = []
        k = 1
        while True:
            print("fetching up to ", 1000 * k, "records...")
            try:
                response = urlopen(url)
            except HTTPError as e:
                if e.code == 503:
                    to = int(e.hdrs.get("retry-after", 30))
                    print("Got 503. Retrying after {0:d} seconds.".format(self.t))
                    time.sleep(self.t)
                    continue
                else:
                    raise
            k += 1
            xml = response.read()
            root = ET.fromstring(xml)
            records = root.findall(OAI + "ListRecords/" + OAI + "record")
            for record in records:
                meta = record.find(OAI + "metadata").find(ARXIV + "arXiv")
                record = Record(meta).output()
                if self.append_all:
                    ds.append(record)
                else:
                    save_record = False
                    for key in self.keys:
                        for word in self.filters[key]:
                            if word.lower() in record[key]:
                                save_record = True

                    if save_record:
                        ds.append(record)
            try:
                token = root.find(OAI + "ListRecords").find(OAI + "resumptionToken")
            except:
                return 1
            if token is None or token.text is None:
                break
            else:
                url = BASE + "resumptionToken=%s" % token.text
        print("Total number of records {:d}".format(len(ds)))
        return ds
