import collections
from collections import defaultdict
from numpy import linalg as la
import numpy as np
import random

from myapp.search.objects import ResultItem
from myapp.search.build_index import build_terms

def build_popularity_score(corpus, clicks):
    global analytics_data
    scores = {}
    for doc in corpus.values():
        like_score = np.log(doc.likes + 100) - np.log(100)
        retweet_score = np.log(doc.retweets + 10) - np.log(10)
        hashtag_score = np.log(len(doc.hashtags) + 10) - np.log(10)
        
        try:
            click_score = np.log(clicks[doc.id] + 10) - np.log(10)
        except:
            click_score = 0

        score = 0.5 * like_score + 0.5 * retweet_score + hashtag_score + 2 * click_score
        scores[doc.id] = score 
    return scores

def return_documents(top, corpus, search_id): 
    res = []
    counter = 1 #store the ranking position
    for i, num in zip(top, range(len(top))):
        item = corpus[i]
        res.append(ResultItem(item.id, item.title, item.description, item.doc_date,
                              "doc_details?id={}&search_id={}&ranking={}".format(item.id, search_id, counter), num+1))
        counter+=1
    return res


def rank_ourScore_cos(terms, docs, index, idf, tf, pop_score, w):
    """
    Perform the ranking of the results of a search based on the tf-idf weights
    
    Argument:
    terms -- list of query terms
    docs -- list of documents, to rank, matching the query
    index -- inverted index data structure
    idf -- inverted document frequencies
    tf -- term frequencies
    title_index -- mapping between page id and page title
    pop_score -- dictionary of popularity scores per document
    w -- weight for the popularity score term
    
    Returns:
    A list of the doc_ids sorted from the one with highest similarity to the one with lowest similarity. 
    """
    doc_vectors = defaultdict(lambda: [0] * len(terms))
    query_vector = [0] * len(terms)

    # compute the norm for the query tf
    query_terms_count = collections.Counter(terms)
    query_norm = la.norm(list(query_terms_count.values()))

    for termIndex, term in enumerate(terms):
        if term not in index: #if term is not in index go to the next term 
            continue

        query_vector[termIndex]=query_terms_count[term]/query_norm * idf[term]  #tf of the term * idf term 

        # Generate doc_vectors. For each doc & each term we have a score 
        for doc_index, (doc, postings) in enumerate(index[term]): 
         
            if doc in docs: 
                doc_vectors[doc][termIndex] = tf[term][doc_index] * idf[term]  

    # compute cosine similarity between query_vector & the doc_vecotr and ADD POPULARITY SCORE with weight w
    doc_scores = [[np.dot(curDocVec, query_vector)  + w * pop_score[doc] , doc] for doc, curDocVec in doc_vectors.items()]
    doc_scores.sort(reverse=True)  
    result_docs = [x[1] for x in doc_scores]

    if len(result_docs) == 0:
        print("No results found, try again")

    return result_docs

def select_docs_query (query, index):
    """
    Given a query string (without pre-processing), select the documents that contain all index terms of the query
    
    Argument:
    query -- the query as the raw un-pre-processed string 
    index -- inverted index data structure
    
    Returns:
    List of doc_ids that contain all index terms of the query 
    """
    query = build_terms(query) #pre-process the string 
    docs =  set()
    first_time = True

    for term in query: #take a list of all documents that contain all the terms
        try:
            # store in term_docs the ids of the docs that contain the term                       
            term_docs=[posting[0] for posting in index[term]]
            if first_time: #first term
                docs = docs.union(set(term_docs))
                first_time = False
            else:
                docs = docs.intersection(set(term_docs))
        except:
            #term is not in index
            pass

    docs = list(docs)
    return query, docs

def rank_our_score(query, index, idf, tf, popularity_score, corpus, search_id, w=0.75):
    query, docs = select_docs_query(query, index)
    ranked_docs = rank_ourScore_cos(query, docs, index, idf, tf, popularity_score, w)
    
    return return_documents(ranked_docs, corpus, search_id)
