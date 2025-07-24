import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

ip_sentence = "This is a sample sentence, with some punctuations! Let's see how it works. On this sentence we will perform various NLP tasks like tokenization, stop word removal, stemming, and vectorization. Done by SHWETANK SHEKHAR 22BEC1204"

# 1. Remove punctuations and other symbols
sentence_wo_punct = "".join([char for char in ip_sentence if char not in string.punctuation])

# Tokenize
words = word_tokenize(sentence_wo_punct)
print("Tokenized words (after punctuation removal): ")
for i in words:
    print(i)

# stop words definition:
stp_wrds = set(stopwords.words('english'))
print(f"There are {len(stp_wrds)} stop words in the given input sentence\n")
print("The stop words are: \n")
print(stp_wrds)
print()

#Remove stop words & lower case
words = [i.lower() for i in words if i.lower() not in stp_wrds]

print("\n Words in lower case listed without stop words: ")
for i in words:
    print(i)

#Porter Stemmer
p_s = PorterStemmer()
words  = [p_s.stem(w) for w in words]

print("Porter Stemmed Words:\n")
for i in words:
    print(i)

#Pos Tagging
print("\n PoS tagging of words")
print(nltk.pos_tag(words))

#Vectorization-1/ Bag of Words
vectorizer = CountVectorizer()
processed_sentz_for_vectorization = " ".join(words)
x = vectorizer.fit_transform([processed_sentz_for_vectorization])
print("\n Vectorization BoW")
print("Vocabulary:", vectorizer.get_feature_names_out())
print("BoW Vector:\n", x.toarray())


#Vectorization-2/ TF-IDF
print("\n Vectorization TF-IDF")
vectorizer = TfidfVectorizer()
x = vectorizer.fit_transform([processed_sentz_for_vectorization])

print("Vocabulary:", vectorizer.get_feature_names_out())
print("TF-IDF Vector:\n", x.toarray())