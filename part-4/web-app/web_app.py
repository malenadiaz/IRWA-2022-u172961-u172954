import os
from json import JSONEncoder
import json

# pip install httpagentparser
import httpagentparser  # for getting the user agent as json
import nltk
from flask import Flask, render_template, session
from flask import request

import datetime

from myapp.analytics.analytics_data import AnalyticsData, ClickedDoc
from myapp.search.load_corpus import load_corpus, load_clicks_data, load_queries_data, load_numbers_data
from myapp.core.utils import write_csv_file, get_location
from myapp.search.objects import Document, StatsDocument, Session_Info
from myapp.search.search_engine import SearchEngine
from myapp.search.build_index import clean_query


# *** for using method to_json in objects ***
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default

# end lines ***for using method to_json in objects ***

# instantiate the Flask application
app = Flask(__name__)

# random 'secret_key' is used for persisting data in secure cookie
app.secret_key = 'afgsreg86sr897b6st8b76va8er76fcs6g8d7'
# open browser dev tool to see the cookies
app.session_cookie_name = 'IRWA_SEARCH_ENGINE'

# instantiate our in memory persistence
analytics_data = AnalyticsData()


full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)

# load documents corpus into memory.
file_path = path + "/tweets-data-who.json"
corpus = load_corpus(file_path)

#analytics Data
file_path_clicks = path + "/analytics_data/clicks_data.csv"
analytics_data.fact_clicks = load_clicks_data(file_path_clicks)

file_path_queries = path + "/analytics_data/queries.csv"
analytics_data.fact_queries = load_queries_data(file_path_queries)

file_path_numbers = path + "/analytics_data/numbers_data.csv"
analytics_data.fact_numbers = load_numbers_data(file_path_numbers)
analytics_data.fact_numbers["corpus_length"] = len(corpus)

file_path_time = path + "/analytics_data/time_data.csv"
analytics_data.fact_time = load_queries_data(file_path_time)

# instantiate our search engine
search_engine = SearchEngine(corpus, analytics_data)

#session info
sess =  []

# Home URL "/"
@app.route('/')
def index():
    print("starting home url /...")
    #first connection
    if("id" not in session or len(sess) < session["id"]+1):
        print("storing session information")
        #store the session information
        user_agent = request.headers.get('User-Agent')
        user_ip = request.remote_addr
        agent = httpagentparser.detect(user_agent)

        new_sess = Session_Info()
        new_sess.OS = agent['platform']['name']
        new_sess.OSV = agent['platform']['version']
        new_sess.browser = agent['browser']['name']
        new_sess.browserV = agent['browser']['version']
        new_sess.user_ip = user_ip
        
        #new_sess.location = get_location(request.remote_addr))
        session["id"] = len(sess)
        sess.append(new_sess)

    return render_template('index.html', page_title="Welcome")

#when form is filled 
@app.route('/search', methods=['POST'])
def search_form_post():
    search_query = request.form['search-query']
    search_id = analytics_data.save_query_terms(search_query)

    #measure search time
    start = datetime.datetime.now()
    results = search_engine.search(search_query, search_id)
    end = datetime.datetime.now()
    search_time = (end-start).total_seconds()

    #analytics data store query 
    clean_q = clean_query(search_query)
    for term in clean_q:
        if term in analytics_data.fact_queries.keys():
            analytics_data.fact_queries[term] += 1
        else:
            analytics_data.fact_queries[term] = 1
    write_csv_file(file_path_queries, analytics_data.fact_queries)

    #analytics store time 
    avg_time = analytics_data.fact_numbers["time"] * analytics_data.fact_numbers["searches"]
    avg_time += search_time
    avg_time = avg_time/(analytics_data.fact_numbers["searches"] + 1)
    analytics_data.fact_numbers["time"] = avg_time

    #analytics store one more search
    analytics_data.fact_numbers["searches"] += 1
    write_csv_file(file_path_numbers, analytics_data.fact_numbers)

    #analytics store hour
    hour = datetime.datetime.now().strftime("%H")
    analytics_data.fact_time[hour] += 1
    write_csv_file(file_path_time, analytics_data.fact_time)

    found_count = len(results)

    #store search in session
    sess[session["id"]].new_search(search_id, search_query, found_count)

    return render_template('results.html', results_list=results, page_title="Results", found_counter=found_count, search_time = search_time)

#to get the previous search without sending the form 
@app.route('/search', methods=['GET'])
def search():
    #get the previous query and query id 
    search_query = sess[session["id"]].searches[-1].query
    search_id = sess[session["id"]].searches[-1].id

    #search again the results 
    start = datetime.datetime.now()
    results = search_engine.search(search_query, search_id)
    end = datetime.datetime.now()
    search_time = (end-start).total_seconds()

    found_count = len(results)

    return render_template('results.html', results_list=results, page_title="Results", found_counter=found_count, search_time = search_time)


@app.route('/doc_details', methods=['GET'])
def doc_details():

    # get the query string parameters from request
    clicked_doc_id = int(request.args["id"])
    search_id = int(request.args["search_id"])  # transform to Integer
    ranking = int(request.args["ranking"])  # transform to Integer
    print("click in id={}".format(clicked_doc_id))

    #get the tweet
    doc = search_engine.get_doc(clicked_doc_id, corpus)
    
    for search in sess[session["id"]].searches: #get the search id and append that doc 
       if search.id == search_id:
        search.docs.append(doc)

    # store data in statistics table 1
    if clicked_doc_id in analytics_data.fact_clicks.keys():
        analytics_data.fact_clicks[clicked_doc_id] += 1
    else:
        analytics_data.fact_clicks[clicked_doc_id] = 1
    write_csv_file(file_path_clicks, analytics_data.fact_clicks)

    #count number of docs clicked that were retrieved at 1st position
    if ranking == 1:
        analytics_data.fact_numbers["first_clicked"] += 1
    write_csv_file(file_path_numbers, analytics_data.fact_numbers)

    print("fact_clicks count for id={} is {}".format(clicked_doc_id, analytics_data.fact_clicks[clicked_doc_id]))
    return render_template('doc_details.html', doc = doc, clicks = analytics_data.fact_clicks[clicked_doc_id])


@app.route('/stats', methods=['GET'])
def stats():
    """
    Show simple statistics example. ### Replace with dashboard ###
    :return:
    """
   
    docs = []

    for doc_id in analytics_data.fact_clicks:
        row: Document = corpus[int(doc_id)]
        count = analytics_data.fact_clicks[doc_id]
        doc = StatsDocument(row.id, row.title, row.description, row.doc_date, row.url, count)
        docs.append(doc)

    docs.sort(key=lambda doc: doc.count, reverse=True)
    return render_template('stats.html', clicks_data=docs)


@app.route('/dashboard', methods=['GET'])
def dashboard():

    #retrieved the visited docs as class ClickedDoc
    visited_docs = []
    for doc_id in analytics_data.fact_clicks.keys():
        d: Document = corpus[int(doc_id)]
        doc = ClickedDoc(doc_id, d.description, analytics_data.fact_clicks[doc_id])
        visited_docs.append(doc)

    searched_terms = json.dumps(analytics_data.fact_queries)
    numbers =  json.dumps(analytics_data.fact_numbers)
    time_data = json.dumps(analytics_data.fact_time)
    
    # sort the documents by click_count 
    visited_docs.sort(key=lambda doc: doc.counter, reverse=True)
    visited_docs = [d.to_json() for d in visited_docs ]
    return render_template('dashboard.html', visited_docs=visited_docs[0:10], searched_terms =searched_terms, numbers = numbers,time_data=time_data, page_title="Dashboard")

#show session details 
@app.route('/session', methods=['GET'])
def session_info():
    my_sess = sess[session["id"]]
    return render_template('session.html', page_title="Session Info",
     sess=my_sess, time=my_sess.get_runTime() )

#functionality that already came
@app.route('/sentiment')
def sentiment_form():
    return render_template('sentiment.html',  page_title="Sentiment Analysis")
@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score,  page_title="Sentiment Analysis")


if __name__ == "__main__":
    app.run(port=8088, host="0.0.0.0", threaded=False, debug=True)
