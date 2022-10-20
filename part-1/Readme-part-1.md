# Readme 

Code creators:

- Malena Díaz: u172961
- Cristina Galvez: u172954

The code is submitted in a *.ipynb* notebook. In order for it to work correctly it needs access to two documents which we assume the teacher already has. The two documents are:

- *tw_hurricane_data.json*
- *tweet_document_ids_map.csv*

The user will have to input the path of the two files in the variables:

-  the path of *tw_hurricane_data.json* in  *docs_path*
- the path of *tweet_document_ids_map.csv* in *map_path*

The place where these variables are defined is marked with the label IMPORTANT! 

#### Requirements
The notebook requires of some python libraries to be installed in the machine. They are the following:
	- *json*
	- *string*
	- *re*
	- *csv*
	- *word2number* (there is a cell in the code to install this library)
	- *nltk*
	- *datetime*
	- *google.colab*

#### Recommendations
This notebook has been created using *Google Colab*. It can be run from other python notebooks environments, but it is recommended to also use *Colab* to avoid unintentional errors.

The notebook is designed to be executed sequentially if the user wants to end up with the original *tw_hurricane_data.json* dataset pre-processed. The result of this preprocessing part is a python dictionnary. The keys are the document names appearing on  *tweet_document_ids_map.csv*. For each document we have another dictionnary with the fields *id*,*text*, *username*, *date*, *hashtags*, *likes*, *retweets* and *urls*. Text is the list of index terms. However, the two functions: *create_struct*, *build_terms* are designed to be part of the final search engine.

