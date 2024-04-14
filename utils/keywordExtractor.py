from yake import KeywordExtractor
import re

def clean_text(txt):
    txt = ' '.join(txt.split('\n'))
    txt = txt.lower()
    txt = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", txt)
    return txt
def keyword_from_search_sentence(text) :
    '''
    This function takes a search sentence as input and returns the top 10 keywords from the sentence.
    '''
    if type(text) == str :
        if len(clean_text(text).split()) == 1 :
            return text
        para = clean_text(text)
        kw_extractor = KeywordExtractor(lan="en", n=1, top=10)
        list_of_keyword_tuples = kw_extractor.extract_keywords(text=para)
        list_of_keywords = [it[0] for it in list_of_keyword_tuples]
        if len(list_of_keywords) < 10 :
            return list_of_keywords
        return list_of_keywords[:10]
    else :
        return text