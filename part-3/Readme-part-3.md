# Readme 

Code creators:

- Malena Díaz: u172961
- Cristina Galvez: u172954

The code is submitted in a .ipynb notebook. In order for it to work correctly it needs access to two documents which we assume the teacher already has. The two documents are:

- *tw_hurricane_data.json*
- *tweet_document_ids_map.csv*

The user will have to input the path of the two files in the variables on the first code cell of the notebok.

-  the path of *tw_hurricane_data.json* in  *docs_path*
- the path of *tweet_document_ids_map.csv* in *map_path*

The notebook is designed to be executed sequentially. There are numerous sections:

- Preprocessing of the collection (reused code from previous labs).
- Index creation. 
- Ranking Algorithm: TF-IDF vector representation + cosine similarity. 
- Our score + Cosine Similarity.
- Ranking Algorithm: BM25.
- Word2vec + cosine similarity.

 The user can see the results of each ranking printed at the end of each section. In some sections there is also a comparison between ranking algorithms.  In the implementation of our score, we have done a previous study through distribution plots in order to determine which normalization would be the appropiate one for each variable. All these plots can also be visualized from the notebook itself. 

