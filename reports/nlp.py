import nltk
from nltk.corpus import stopwords
from nltk.tokenize import regexp_tokenize

stopword_spa = stopwords.words('spanish')
stopword_eng = stopwords.words('english')
stopword_idio=['author','title']
all_stopwords= stopword_spa + stopword_eng + stopword_idio

def collection_of_search_terms_str(df_search,term_col:str)->str:
    # Tokenize just words
    alpha = r"\w+"

    search_terms=''
    # iterate through the csv file
    for val in df_search[term_col]:
        
        # typecaste each val to string
        tokens = regexp_tokenize(val, alpha)
        
        lower=[t.lower() for t in tokens if t.isalpha()]

        no_stop=[t for t in lower if t not in all_stopwords]
        
        search_terms += " ".join(no_stop)+" "

        return search_terms



     
     