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
    
# Example usage
# text = """Python, created by Guido van Rossum and first released in 1991, is a high-level, 
#     interpreted programming language known for its readability and simplicity. 
#     It was designed to be highly readable and to emphasize code readability, 
#     making it a popular choice for beginners and experienced developers alike. 
#     Python's development was influenced by a variety of languages, including ABC, 
#     Modula-3, C, C++, and others. Over the years, Python has undergone several major releases, 
#     with the latest stable version being Python 3. Python 2, which was first released in 2000, 
#     reached its end of life in 2020, prompting developers to transition to Python 3."""
# keywords = keyword_from_search_sentence(text)