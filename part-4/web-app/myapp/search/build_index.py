from collections import defaultdict
import math
import numpy as np
import string
import re
from word2number import w2n
import nltk
nltk.download('stopwords')
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# to handle turning written numbers into digits

def is_written_num(word):
  # returns True only if it is a written number
  # returns False if it is a digit or something else
  try:
    w2n.word_to_num(word)
    try: 
      int(word)
      return False
    except:
      return True
  except:
    return False

# given an array of strings, takes all written numbers and makes them digits
def make_numbers_digits(text):
  consec_num = False
  num_string = ''
  result = []

  for word in text:
    if not is_written_num(word):
      if consec_num:
        result.append(str(w2n.word_to_num(num_string)))
        consec_num = False
        num_string = ''
      result.append(word)
    else:
      consec_num = True
      num_string += ' ' + word

  if consec_num:
    result.append(str(w2n.word_to_num(num_string)))

  return result

def treat_hashtags(text):
  remove_hashtag = text[1:]
  split_lower_upper = re.sub(r"([A-Z])", r" \1", remove_hashtag)
  return split_lower_upper

def build_terms_without_stemming(line):
    """
    Preprocess the article text (title + body) removing stop words, stemming,
    transforming in lowercase and return the tokens of the text.
    
    Argument:
    line -- string (text) to be preprocessed
    
    Returns:
    line - a list of tokens corresponding to the input text after the preprocessing
    """

    # define stemmer and reference lists
    stop_words = set(stopwords.words("english"))
    whitelist = string.ascii_letters + string.digits + ' '

    # clean text
    line = re.sub(r'http\S+', '', line) # remove urls
    line = re.sub(r'@\S+', '', line) # remove mentioned users
    line = ' '.join([treat_hashtags(i) if i.startswith("#") else i for i in line.split()]) # deal with hashtags
    line = line.replace("-", " ") # deal with dashes
    line = line.replace("$", " dollars") # deal with currencies  
    line = line.replace("€", " euros") # deal with currencies  
    line = ''.join([char if char in whitelist else ' ' for char in line]) # remove all symbols (leave only letters, digits, # and spaces)
    line = line.lower() ## Transform in lowercase
    line = line.split() ## Tokenize the text to get a list of terms
    line = [x for x in line if x not in stop_words]  ##eliminate the stopwords (HINT: use List Comprehension)
    line = make_numbers_digits(line) # turn written numbers into digits
    line = [x for x in line if (len(x) > 1 or x.isdigit()) ] # remove single letters

    return line

def build_terms(line):
    """
    Preprocess the article text (title + body) removing stop words, stemming,
    transforming in lowercase and return the tokens of the text.
    
    Argument:
    line -- string (text) to be preprocessed
    
    Returns:
    line - a list of tokens corresponding to the input text after the preprocessing
    """
    # define stemmer and reference lists
    line = build_terms_without_stemming(line)
    stemmer = PorterStemmer()
    line = [stemmer.stem(x) for x in line ] ## perform stemming (HINT: use List Comprehension)
    return line

def clean_query(line): #used to store the query terms in the wordcloud
    line = build_terms_without_stemming(line)      
    return line




def create_index_tfidf(collection, num_documents):
    """
    Implement the inverted index and compute tf, df and idf
    
    Argument:
    collection -- collection of tweets 
    num_documents -- total number of documents
    
    Returns:
    index - the inverted index (implemented through a Python dictionary) containing terms as keys and the corresponding
    list of document these keys appears in (and the positions) as values.
    tf - normalized term frequency for each term in each document
    df - number of documents each term appear in
    dl - dict with the length (counting only index terms) of each doc  
    adl - float with the average document length of the collection
    idf - inverse document frequency of each term
    """

    index = defaultdict(list)
    tf = defaultdict(list)  # term frequencies of terms in documents (documents in the same order as in the main index)
    df = defaultdict(int)  # document frequencies of terms in the corpus
    dl = defaultdict(int)
    title_index = defaultdict(str)
    idf = defaultdict(float)

    for key in collection:
        doc = collection[key]
        title_index[key] = doc.id
        terms = build_terms(doc.description) #retrieves a dict 
        dl[key] = len(terms)

        current_page_index = {}

        for position, term in enumerate(terms):
            try:
                current_page_index[term][1].append(position) # term already added in doc array 
            except:
                current_page_index[term]=[key, [position]]

        #normalize term frequencies
        #norm is the square root of the sum of the frequency of each term squared
        norm = 0
        for term, posting in current_page_index.items():
            norm += len(posting[1]) ** 2 #len(posting[1]) == number of times it appears in the doc (frecuency of a term)
        norm = math.sqrt(norm) 

        # compute the tf(dividing the term frequency by the above computed norm) and df weights
        for term, posting in current_page_index.items():
            tf[term].append(np.round(len(posting[1])/norm,4)) #tf is frecuency of the term / norm
            df[term] = df[term] + 1 # df is number of documents where that doc appears (we increment it by one)

        for term_page, posting_page in current_page_index.items():
            index[term_page].append(posting_page) #for each term add this doc and its position to the general index

        for term in df:
            idf[term] = np.round(np.log(float(num_documents/df[term])), 4) #idf of the term is log ( num_docs / df [term])
    
    #compute the avg doc length
    adl = sum(dl.values()) / len(dl)

    return index, tf, df, dl, adl, idf, title_index
