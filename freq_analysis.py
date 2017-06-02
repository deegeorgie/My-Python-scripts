#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      bodiong
#
# Created:     12/08/2016
# Copyright:   (c) bodiong 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from my_creds import oauth_login
from collections import Counter
import json
from prettytable import PrettyTable

def twitter_search(twitter_api, q, max_results=200, **kw):
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets and
    # https://dev.twitter.com/docs/using-search for details on advanced
    # search criteria that may be useful for keyword arguments
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = twitter_api.search.tweets(q=q, count=100, **kw)
    statuses = search_results['statuses']
    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.
    # Enforce a reasonable limit
    max_results = min(1000, max_results)
    for _ in range(10): # 10*100 = 1000
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            break

    # Create a dictionary from next_results, which has the following form:
    # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=')
                        for kv in next_results[1:].split("&") ])
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
        if len(statuses) > max_results:
            break
    return statuses

def extract_tweet_entities(statuses):
    # See https://dev.twitter.com/docs/tweet-entities for more details on tweet
    # entities
    if len(statuses) == 0:
        return [], [], [], [], []
    screen_names = [ user_mention['screen_name']
                         for status in statuses
                            for user_mention in status['entities']['user_mentions'] ]

    hashtags = [ hashtag['text']
                     for status in statuses
                        for hashtag in status['entities']['hashtags'] ]
    urls = [ url['expanded_url']
                     for status in statuses
                        for url in status['entities']['urls'] ]
    symbols = [ symbol['text']
                   for status in statuses
                       for symbol in status['entities']['symbols'] ]

    # In some circumstances (such as search results), the media entity
    # may not appear
    if status['entities'].has_key('media'):
        media = [ media['url']
                         for status in statuses
                            for media in status['entities']['media'] ]
    else:
        media = []
    return screen_names, hashtags, urls, media, symbols


def get_common_tweet_entities (statuses, entity_threshold=3):
    tweet_entities = [e
                        for status in statuses
                            for entity_type in extract_tweet_entities([status])
                                for e in entity_type
                    ]
    c = Counter(tweet_entities).most_common()

    # Compute frequencies
    return [ (k,v)
             for (k,v) in c
                 if v >= entity_threshold
           ]

q = "PR_Paul_Biya"

def analyze_tweet_content(statuses):
    if len(statuses) == 0:
        print "No statuses to analyze"
        return
# A nested helper function for computing lexical diversity
    def lexical_diversity(tokens):
        return 1.0*len(set(tokens))/len(tokens)
# A nested helper function for computing the average number of words per tweet
    def average_words(statuses):
        total_words = sum([ len(s.split()) for s in statuses ])
        return 1.0*total_words/len(statuses)
    status_texts = [ status['text'] for status in statuses ]
    screen_names, hashtags, urls, media, _ = extract_tweet_entities(statuses)
# Compute a collection of all words from all tweets
words = [ w
          for t in status_texts
              for w in t.split() ]
print "Lexical diversity (words):", lexical_diversity(words)
print "Lexical diversity (screen names):", lexical_diversity(screen_names)
print "Lexical diversity (hashtags):", lexical_diversity(hashtags)
print "Averge words per tweet:", average_words(status_texts)

# Get some frequency data
twitter_api = oauth_login()
search_results = twitter_search(twitter_api, q, max_results=100)
common_entities = get_common_tweet_entities(search_results)

analyze_tweet_content(search_results)

#print "MOST COMMON TWEET ENTITIES"
#print common_entities

# Use PrettyTable to create a nice tabular display
pt = PrettyTable(field_names=['Entity', 'Count'])
[ pt.add_row(kv) for kv in common_entities ]
pt.align['Entity'], pt.align['Count'] = 'l', 'r' # Set column alignment
#print pt




def main():
    pass

if __name__ == '__main__':
    main()
