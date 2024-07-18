def calculate_similarity(search_keywords, yake_list):
    '''
    Calculate similarity score between search keywords and yake list using Jaccard similarity
    '''
    intersection = set(search_keywords) & set(yake_list)
    union = set(search_keywords) | set(yake_list)
    similarity_score = len(intersection) / len(union)
    return similarity_score

def rank_documents(search_keywords, documents, users, search_filter=True):
    """
    Rank documents based on cosine similarity, NIRF factor, and location factor.
    """
    ranked_documents = []
    
    # Calculate min NIRF ranking
    max_nirf_ranking = max(user['nirf'] for user in users)
    
    # Create a dictionary to store location counts
    location_counts = {}
    for user in users:
        location_counts[user['location']] = location_counts.get(user['location'], 0) + 1
    
    # Iterate over documents
    for doc in documents:
        # Calculate similarity
        if search_filter==True:
            similarity = calculate_similarity(search_keywords, doc['yake_list'])
        else:
            similarity = 0
        
        # # Calculate NIRF factor
        filtered_data_username = [user for user in users if user.get('user_name') == doc['user']]
        current_nirf_ranking = filtered_data_username[0]['nirf']
        nirf_factor = (max_nirf_ranking - current_nirf_ranking) / max_nirf_ranking * 0.01
        
        # # Calculate location factor
        current_author_location = filtered_data_username[0]['location']
        location_factor = location_counts[current_author_location] / len(documents) *0.01
        
        # Calculate the overall ranking factor
        ranking_factor = similarity + nirf_factor + location_factor
        
        # Append document with ranking factor to the ranked documents list
        ranked_documents.append((doc['title'], doc['user'], doc['slug'], doc["image_url"], ranking_factor))
    
    # Sort documents by ranking factor in descending order
    ranked_documents.sort(key=lambda x: x[4], reverse=True)
    return ranked_documents
