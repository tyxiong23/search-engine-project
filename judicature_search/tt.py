from whoosh.index import open_dir
from whoosh.query import Every

index = open_dir('whoosh_index')

with index.searcher() as searcher:
    query = Every()  # Query that matches every document in the index
    results = searcher.search(query, limit=None)  # Don't limit the results

    for hit in results:
        print(hit)  # Print each matching document