'''
This is the object in charge of linking the data from the apis, it is important to recognize 
that the variables associated with **kwargs** are the parameters with which they are sent from the main program

'''
import pandas as pd
from requests import Request, Session
import json
import io
import pytz
from datetime import datetime
import snscrape.modules.twitter as sntwitter
import pandas as pd
import itertools
import nltk

class apiReader:
    def __init__(self):
        '''
        Here constants are started throughout the program
        '''
        self.header = {'Content-type': 'text/json',
                        'Accept': 'text/plain'}
        self.ACCESS_KEY ='1ff453cc42278d0985d675b52f8906c5'
        self.GEOAPI = f'http://api.positionstack.com/v1/forward?access_key={self.ACCESS_KEY}&query='
        self.pattern = r'''(?x)          # set flag to allow verbose regexps
            (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
          | \w+(?:-\w+)*        # words with optional internal hyphens
          | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
          | \.\.\.              # ellipsis
          | [][.,;"'?():_`-]    # these are separate tokens; includes ], [
          '''
        self.stopwords = pd.read_csv('stopwords_es.csv')['STOPWORD'].tolist()+['https','http']

    def getData(self, **kwargs):
        '''
        Esta funcion obtiene el scrapping de twitter
        '''
        try:
            loc=kwargs['loc']
            keyword=kwargs['keyword'].replace('+',' ')

            self.stopwords.append(keyword)
            query = keyword+' '+f'since:{kwargs["start"]} until:{kwargs["end"]} geocode:'+'"{}"'

            df = pd.DataFrame(
                itertools.islice(
                    sntwitter.TwitterSearchScraper(
                        query.format(loc)
                        ).get_items(), 500))
            df=self.mytokenize(df=df['content'])
            return df
        except Exception as ex:
            pass
    
    def mytokenize(self, **kwargs):
        '''
        Esta funcion toqueniza las palabras
        '''
        df=kwargs['df']
         # hacer un analisis de sentimientos
        doc = ''
        for text in df:
            doc = doc + text.lower()
        words=nltk.regexp_tokenize(doc, self.pattern)

        #filtrar las palabras
        filtered = []
        for word in words:
            if len(word)>3:
                filtered.append(word)
        freq = {}
        for word in filtered:
            if word in freq:
                freq[word] += 1
            else:
                freq[word] = 1
        data = [ [k,v] for k,v in freq.items() if v>2 and k not in self.stopwords]
        df=pd.DataFrame(data,columns=['palabra','frecuencia']).sort_values('frecuencia', ascending=False)
        return df

    def getCoordinates(self, **kwargs):
        try:
            country = kwargs['country']
            s = Session()
            ##print(apiSearchCP+self.id_patient)
            req = Request('GET', self.GEOAPI+country,
                headers=self.header
            )
            prepped = req.prepare()
            resp = s.send(prepped)
            my_bytes_value=resp.content
            fix_bytes_value = my_bytes_value.replace(b"'", b'"')
            my_json = json.load(io.BytesIO(fix_bytes_value))
            #return my_json
            return f"{my_json['data'][0]['latitude']}, {my_json['data'][0]['longitude']}, 200km"
        except Exception as ex:
            print(ex)

    def getApi(self,**kwargs):
        try:
            keyword=kwargs['keyword']
            s = Session()
            ##print(apiSearchCP+self.id_patient)
            req = Request('GET', f'https://sandbox.getonbrd.dev/api/v0/search/jobs?query={keyword}',
                headers=self.header
            )
            prepped = req.prepare()
            resp = s.send(prepped)
            my_bytes_value=resp.content
            fix_bytes_value = my_bytes_value.replace(b"'", b'')
            my_json = json.load(io.BytesIO(fix_bytes_value))
            description = []
            salary = []
            for i in range(len(my_json['data'])-1):
                if True:#(my_json['data'][i+1]['attributes']['country'] == kwargs['country'] or my_json['data'][i+1]['attributes']['country'] == 'Remote') and my_json['data'][i+1]['attributes']['category_name'] == kwargs['keyword'].replace('+',' '):
                    salary.append([my_json['data'][i+1]['attributes']['min_salary'],my_json['data'][i+1]['attributes']['max_salary']])
                    description.append(my_json['data'][i+1]['attributes']['description'])
                    description.append(my_json['data'][i+1]['attributes']['projects'])
                    description.append(my_json['data'][i+1]['attributes']['functions'])
                    description.append(my_json['data'][i+1]['attributes']['desirable'])
                

            df=pd.DataFrame(salary,columns=['minimo','maximo']).dropna()
            description = pd.DataFrame(description,columns=['words']).dropna()
            description = self.mytokenize(df=description['words'])
            return (df.mean(),description)


        except Exception as ex:
            print(ex)

    


