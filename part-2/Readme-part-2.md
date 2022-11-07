# Readme 

Code creators:

- Malena Díaz: u172961
- Cristina Galvez: u172954

The code is submitted in a .ipynb notebook. In order for it to work correctly it needs access to four documents. The first three are given by our teachers and thus we assume they already have them:

- *tw_hurricane_data.json*

- *tweet_document_ids_map.csv*
- *evaluation_gt.csv*

In addition, in this folder we have attached the file:

- *rel_assessments.csv*

Which contains the relevance assessments for each of the five queries we have proposed. 

To achieve a correct functioning of the notebook, the user will have to input the path of the these files in the first cell of the notebook. She/he will also have to input a path where a .txt document named *tf_idf_results.txt* will be created. 

The notebook is designed to be executed sequentially. The user will end up with:

-  the original *tw_hurricane_data.json* dataset pre-processed.

- an inverted index from the collection of tweets stored in the variable *index*.

- a function *search_tf_idf* that returns a ranked array of documents' ids for a given query and index. 

- a file *tf_idf_results.txt* where one can see the top 10 documents retrieved by the system for each query. It contains the doc_id, the id and the text of each tweet.  

- functions for each of the measures

  - Precision@K (P@K)
  - Recall@K (R@K)
  - Average Precision@K (P@K)
  - F1-Score
  - Mean Average Precision (MAP)
  - Mean Reciprocal Rank (MRR)
  - Normalized Discounted Cumulative Gain (NDCG)

  and the corresponding results for the defined queries printed in the notebook. 

- a two-dimensional representation of the tweets using the T-SNE (T-distributed Stochastic Neighbor
  Embedding) algorithm which can be visualized from the notebook itself. 

