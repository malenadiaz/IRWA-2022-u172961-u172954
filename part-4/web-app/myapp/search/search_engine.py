import random

from myapp.search.objects import ResultItem, Document
from myapp.search.build_index import create_index_tfidf
from myapp.search.algorithms import build_popularity_score, rank_our_score
import pickle


def build_demo_results(corpus: dict, search_id):
    """
    Helper method, just to demo the app
    :return: a list of demo docs sorted by ranking
    """
    res = []
    size = len(corpus)
    ll = list(corpus.values())
    for index in range(random.randint(0, 40)):
        item: Document = ll[random.randint(0, size)]
        res.append(ResultItem(item.id, item.title, item.description, item.doc_date,
                              "doc_details?id={}&search_id={}&param2=2".format(item.id, search_id), random.random()))

    # for index, item in enumerate(corpus['Id']):
    #     # DF columns: 'Id' 'Tweet' 'Username' 'Date' 'Hashtags' 'Likes' 'Retweets' 'Url' 'Language'
    #     res.append(DocumentInfo(item.Id, item.Tweet, item.Tweet, item.Date,
    #                             "doc_details?id={}&search_id={}&param2=2".format(item.Id, search_id), random.random()))

    # simulate sort by ranking
    res.sort(key=lambda doc: doc.ranking, reverse=True)
    print(res)
    return res


class SearchEngine:
    """educational search engine"""

    def __init__(self, corpus, analytics_data, build=False):
        # build indexes
        self.corpus = corpus
        if build:
            print('Building index...')
            index, tf, df, dl, adl, idf, title_index = create_index_tfidf(corpus, len(corpus))
            print('Finished building index')

            self.index = index
            self.tf = tf
            self.df = df
            self.dl = dl
            self.adl = adl
            self.idf = idf
            self.title_index = title_index

            print('Saving index...')

            data_to_store = {"index": index, 'tf': tf, 'df': df, 'dl':dl, 'adl': adl, 'idf': idf, 'title_index':title_index}
            with open('saved_index.pkl', 'wb') as file:
                pickle.dump(data_to_store, file)

        else:
            # read index from somewhere else
            print('Loading index...')
            with open('saved_index.pkl', 'rb') as file:
                data = pickle.load(file)

                self.index = data['index']
                self.tf = data['tf']
                self.df = data['df']
                self.dl = data['dl']
                self.adl = data['adl']
                self.idf = data['idf']
                self.title_index = data['title_index']
        
        self.clicks = analytics_data.fact_clicks
        self.popularity = build_popularity_score(self.corpus, self.clicks)

        

    def search(self, search_query, search_id):
        print("Search query:", search_query)
        results = []
       
        #results = build_demo_results(self.corpus, search_id)  # replace with call to search algorithm
        #results = rank_tf_idf_cos(search_query, self.index, self.idf, self.tf, self.corpus, search_id)        
        results = rank_our_score(search_query, self.index, self.idf, self.tf, self.popularity, self.corpus, search_id)
        return results

    def get_doc(self, doc_id, corpus):
        for item in corpus.values():
            if item.id == doc_id:
                return item
