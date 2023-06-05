import os
import jieba
from whoosh import fields, index
from whoosh.qparser import QueryParser
from case.models import Case
from whoosh.index import open_dir
import whoosh.query.terms

MAX_NUM = 300

def search_cases(query_str):
    index_path = 'whoosh_index'
    index = open_dir(index_path)

    parser = QueryParser("text", index.schema)
    query = parser.parse(query_str)

    print("query", query, type(query))
    if isinstance(query, whoosh.query.terms.Term):
        split_words = [query.text]
    else:
        try:
            split_words = [i.text for i in query]
        except:
            split_words = []

    print("split queries", split_words)

    results_list = []
    with index.searcher() as searcher:
        results = searcher.search(query, limit=None)
        print("results", results)
        for hit in results:
            # print('hit_id', hit["id"], type(hit['id']))
            # hit['text'] = hit['text'].encode("utf-8").decode("unicode-escape")
            results_list.append(dict(hit))  # Convert the hit object to a dictionary and add it to the list
            # print("dict", hit.keys())

    return results_list[:MAX_NUM], split_words


from haystack.forms import SearchForm, SearchQuerySet

def search_cases_new(cd: dict):

    print("cd", cd)
    
    def get_valid_value(k):
        return k in cd.keys() and len(cd[k]) > 0
    
    split_words = []
    
    if get_valid_value("q"):
        query_str = cd['q']
        print("query q", query_str)
        # for k in [k for k in cd.keys() if k != 'page']:
        #     if get_valid_value(k):
        #         print(k, cd[k])
        # print([get_valid_value(k) for k in cd.keys() if k != "page"]))
        # if sum([get_valid_value(k) for k in cd.keys() if k != "page"]) == 1:
        #     print("use old search_case")
        #     return search_cases(query_str)

        index_path = 'whoosh_index'
        index = open_dir(index_path)

        parser = QueryParser("text", index.schema)
        query = parser.parse(query_str)

        print("query", query, type(query))
        if isinstance(query, whoosh.query.terms.Term):
            split_words = [query.text]
        else:
            try:
                split_words = [i.text for i in query]
            except:
                split_words = []
        results = SearchQuerySet().models(Case).filter(qw_value = cd['q'])
    else:
        results = Case.objects.all()
        

    if get_valid_value('note_name'):
        results = results.filter(note_name = cd['note_name'])
        split_words.append(cd['note_name'])
    if get_valid_value('judge_prop'):
        results = results.filter(judge_prop = cd['judge_prop'])
        split_words.append(cd['judge_prop'])
    if get_valid_value('case_reason'):
        results = results.filter(case_reason = cd['case_reason'])
        split_words.append(cd['case_reason'])
    if get_valid_value('province'):
        results = results.filter(province = cd['province'])
        split_words.append(cd['province'])
    if get_valid_value('year'):
        year = int(cd['year'])
        results = results.filter(year = year)
        split_words.append(cd['year'])

    if get_valid_value("q"):
        results = results.load_all()

    print("split_words", split_words)
    return results[:MAX_NUM], split_words
    
    

    
    

    
    # print("finish search_q", len(results), type(results[0]))
    
    
# def create_index():
#     # Define the schema for the index
#     schema = fields.Schema(qw_value=fields.TEXT(stored=True))
    
#     # Create the index directory if it doesn't exist
#     os.makedirs(index_dir, exist_ok=True)
    
#     # Open the index and create a writer
#     ix = index.create_in(index_dir, schema)
#     writer = ix.writer()

#     # Retrieve documents from the database and add them to the index
#     cases = Case.objects.all()
#     for case in cases:
#         qw_value = case.qw_value
#         # Perform word segmentation using Jieba
#         words = jieba.lcut(qw_value)
#         # Join the words into a space-separated string
#         indexed_text = " ".join(words)
#         writer.add_document(qw_value=indexed_text)

#     # Commit the changes and close the writer
#     writer.commit()

# def perform_search(query_string):
#     # Open the existing index
#     ix = index.open_dir(index_dir)
#     # Create a searcher to perform the search
#     searcher = ix.searcher()
#     # Parse the query using the QueryParser
#     parser = QueryParser("qw_value", schema=ix.schema)
#     query = parser.parse(query_string)
#     # Perform the search and retrieve the results
#     results = searcher.search(query)
#     # Access the stored field values from the results
#     search_results = [dict(hit) for hit in results]
#     return search_results

from haystack.query import SearchQuerySet
from case.models import Case
from case.search_indexes import CaseIndex

# def build_index():
#     # Create the index
#     SearchQuerySet().all().delete()
#     CaseIndex().update()

#     # Perform the search
#     search_results = SearchQuerySet().models(Case).all()
#     results = [result.object for result in search_results]
#     return results
