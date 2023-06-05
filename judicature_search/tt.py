from whoosh.index import open_dir
from whoosh.query import Every

index = open_dir('whoosh_index')

with index.searcher() as searcher:
    query = Every()  # Query that matches every document in the index
    results = searcher.search(query, limit=None)  # Don't limit the results
    print("num_results", results)
    print("id", results[0]['id'])

    # for hit in results:
    #     print(hit)  # Print each matching document