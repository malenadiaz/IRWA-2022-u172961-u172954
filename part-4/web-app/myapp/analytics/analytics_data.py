import json
import random


class AnalyticsData:
    """
    An in memory persistence object.
    Declare more variables to hold analytics tables.
    """
    fact_clicks = dict([])
    fact_queries = dict([])
    fact_numbers = dict([])
    fact_time = dict([])


    def save_query_terms(self, terms: str) -> int:
        print(self)
        return random.randint(0, 100000)


class ClickedDoc:
    def __init__(self, doc_id, description, counter):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)
