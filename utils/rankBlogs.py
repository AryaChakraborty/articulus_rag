def calculate_similarity(search_keywords, yake_list):
    '''
    Calculate similarity score between search keywords and yake list using Jaccard similarity
    '''
    intersection = set(search_keywords) & set(yake_list)
    union = set(search_keywords) | set(yake_list)
    similarity_score = len(intersection) / len(union)
    return similarity_score

def rank_documents(search_keywords, documents):
    '''
    doc format should be as follows:
    doc = {
        'id': 'Unique ID of the blog',
        ...,
        'location': 'Location of the author',
        'nirf_ranking': 'NIRF ranking of the college/university of the author',
        'yake_list': ['List', 'of', 'YAKE', 'keywords']
    }
    '''
    ranked_documents = []
    max_nirf_ranking = max(doc['nirf_ranking'] for doc in documents)
    total_entries = len(documents)

    # initialize location frequency dictionary
    location_frequency = {}
    for doc in documents:
        location = doc['location']
        if location in location_frequency:
            location_frequency[location] += 1
        else:
            location_frequency[location] = 1
    
    for doc in documents:
        # Calculate similarity between search keywords and yake list
        similarity_score = calculate_similarity(search_keywords, doc['yake_list'])
        
        # Calculate location-based weight
        location_weight = total_entries / location_frequency[doc['location']]
        # normalize location weight between 0 and 1
        location_weight = (location_weight - 1) / (total_entries - 1)
        
        # Calculate NIRF ranking-based weight
        nirf_weight = (max_nirf_ranking - doc['nirf_ranking']) / max_nirf_ranking
        
        # Calculate final ranking score
        ranking_score = similarity_score * location_weight * nirf_weight
        
        # Add document with ranking score to the list
        ranked_documents.append((doc, ranking_score))
    
    # Sort documents based on ranking score
    ranked_documents.sort(key=lambda x: x[1], reverse=True)
    
    return ranked_documents

# Example usage
# search_keywords = ['python', 'programming', 'learning']
# documents = [
#     {
#         'id': '1',
#         'location': 'India',
#         'nirf_ranking': 10,
#         'yake_list': ['python', 'programming', 'learning', 'tutorial']
#     },
#     {
#         'id': '2',
#         'location': 'USA',
#         'nirf_ranking': 5,
#         'yake_list': ['python', 'programming', 'tutorial']
#     },
#     {
#         'id': '3',
#         'location': 'India',
#         'nirf_ranking': 15,
#         'yake_list': ['programming', 'learning', 'tutorial']
#     }
# ]
# print(rank_documents(search_keywords, documents))