import numpy as np
import pandas as pd
from database import BkData, DbName
import nltk
from nltk.corpus import stopwords
from queries import Query, Template
from wordcloud import WordCloud
import matplotlib.pyplot as plt

search=BkData(database=DbName.STATS,
              query=Query(Template.SEARCH).compile_query).fetch_data


stopword_spa = stopwords.words('spanish')
stopword_eng = stopwords.words('english')
stopword_idio=['author','title']
all_stopwords= stopword_spa + stopword_eng + stopword_idio

comment_words=''
# iterate through the csv file
for val in search['termino']:
     
    # typecaste each val to string
    val = str(val)
    
    
    # split the value
    tokens = val.split()
        # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()

        comment_words += " ".join(tokens)+" "


wordcloud = WordCloud(width = 400, height = 400,
                background_color ='white',
                stopwords = all_stopwords,
                max_words=50,
                min_font_size = 10).generate(comment_words)
 
# plot the WordCloud image                      
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()
     
     
    

print(all_stopwords)