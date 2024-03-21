import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_top_matches(query, data, allergens=None, pref_ingredients=None):
    query_tokens = tokenize(query.lower())
    matches = []
   

    # for item_index, item in enumerate(data):
    #     ingredients_tokens = tokenize(item['ingredients'].lower())
    #     contains_allergen = any(allergen.lower() in ingredients_tokens for allergen in allergens) if allergens else False 
    #     contains_ingredients = all(pref_ingredient.lower() in ingredients_tokens for pref_ingredient in pref_ingredients) if pref_ingredients else True 
    #     if not contains_allergen and contains_ingredients:
    #         tokens = tokenize(item['title'].lower())
    #         jaccard_val = jaccard(tokens, query_tokens)
    #         matches.append((jaccard_val, item_index))
    # return sorted(matches, key=lambda x: x[0], reverse=True)


    # Preprocess the descriptions of the data items
    descriptions = [item['description'] for item in data]
    description_tokens = [tokenize(description.lower()) for description in descriptions]

    # Convert the text data into a matrix of token counts
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([' '.join(tokens) for tokens in description_tokens])

    # Compute cosine similarity between the query item's description and all descriptions in the data
    query_vector = vectorizer.transform([' '.join(query_tokens)])
    cos_similarities = cosine_similarity(query_vector, X)[0]

    
    for cos_similarity, item_index in zip(cos_similarities, range(len(data))):
        item = data[item_index]
        ingredients_tokens = tokenize(item['ingredients'].lower())
        contains_allergen = any(allergen.lower() in ingredients_tokens for allergen in allergens) if allergens else False 
        contains_ingredients = all(pref_ingredient.lower() in ingredients_tokens for pref_ingredient in pref_ingredients) if pref_ingredients else True 
        if not contains_allergen and contains_ingredients:
            jaccard_val = jaccard(query_tokens, description_tokens[item_index])
            matches.append((cos_similarity, jaccard_val, item_index))

    # Sort the items based on cosine similarity and Jaccard similarity
    return sorted(matches, key=lambda x: (x[0], x[1]), reverse=True)

   


def jaccard(tokens, query):
    tokens_set = set(tokens)
    query_set = set(query)
    return len(tokens_set.intersection(query_set)) / len(tokens_set.union(query_set))





def tokenize(text):
    """Returns a list of words that make up the text.

    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function

    Parameters
    ----------
    text : str
        The input string to be tokenized.

    Returns
    -------
    List[str]
        A list of strings representing the words in the text.
    """
    # TODO-2.1
    words = re.findall('[a-z]+', text.lower())
    return words
