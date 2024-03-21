import re


def get_top_matches(query, data, allergens=None, pref_ingredients=None):
    query_tokens = tokenize(query.lower())
    matches = []

    for item_index, item in enumerate(data):
        ingredients_tokens = tokenize(item['ingredients'].lower())
        contains_allergen = any(allergen.lower() in ingredients_tokens for allergen in allergens) if allergens else False 
        contains_ingredients = all(pref_ingredient.lower() in ingredients_tokens for pref_ingredient in pref_ingredients) if pref_ingredients else True 
        if not contains_allergen and contains_ingredients:
            tokens = tokenize(item['title'].lower())
            jaccard_val = jaccard(tokens, query_tokens)
            matches.append((jaccard_val, item_index))
    return sorted(matches, key=lambda x: x[0], reverse=True)


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
