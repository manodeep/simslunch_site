from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import datetime

def scrape_doodle(link):
    soup = BeautifulSoup(urlopen(link), )
    jscript = soup.find_all('script')[-6].string
    data = json.loads(re.search('\{("poll":.*)\}', jscript).group(0))['poll']

    df = pd.DataFrame([list(d['preferences'])for d in data['participants']]).T
    df.index = pd.MultiIndex.from_tuples([tuple(d.split()[1:]) for d in data['optionsText']])
    df.index.names = ['date', 'type']
    df.columns = [d['name'] for d in data['participants']]
    df.replace('n', False, inplace=True)
    df.replace('y', True, inplace=True)

    # remove past dates
    today = datetime.date.today()
    sel = [datetime.datetime.strptime(v[0], '%m/%d/%y').date() > today for v in df.index.ravel()]
    df = df[sel]

    return df
