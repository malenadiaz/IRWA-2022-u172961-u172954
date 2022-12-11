import json
import datetime


class Document:
    """
    Original corpus data as an object
    """

    def __init__(self, id, title, description, doc_date, likes, retweets, url, hashtags):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.likes = likes
        self.retweets = retweets
        self.url = url
        self.hashtags = hashtags

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class StatsDocument:
    """
    Original corpus data as an object
    """

    def __init__(self, id, title, description, doc_date, url, count):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.url = url
        self.count = count

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class ResultItem:
    def __init__(self, id, title, description, doc_date, url, ranking):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.url = url
        self.ranking = ranking

class Search:
    def __init__(self, search_id, query, docs_retrieved):
        self.id = search_id
        self.query = query
        self.docs_retrieved = docs_retrieved
        self.docs = []

class Session_Info:
    def __init__(self):
        self.OS = ""
        self.OSV = ""
        self.browser = ""
        self.browserV = ""
        self.user_ip = ""
        self.searches = []
        self.start_time = datetime.datetime.now()

    def get_runTime(self):
        return str(datetime.datetime.now() - self.start_time)

    def to_json(self):
        return self.__dict__

    def new_search(self, search_id, query, docs_retrieved):
        s = Search(search_id, query, docs_retrieved)
        self.searches.append(s)