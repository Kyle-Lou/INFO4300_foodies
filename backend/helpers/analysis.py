import re


def get_top_matches(query, data):
    query_tokens = tokenize(query.lower())
    matches = []
    for item_index, item in enumerate(data):
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
