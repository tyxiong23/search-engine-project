from django.shortcuts import render

from rest_framework import viewsets
from .models import Case
from .serializers import CaseSerializer
from haystack.query import SearchQuerySet

# class CaseViewSet(viewsets.ModelViewSet):
#     queryset = Case.objects.all()
#     serializer_class = CaseSerializer

#     def get_queryset(self):
#         queryset = Case.objects.all()
        
#         # Perform search if search query parameter is provided
#         search_query = self.request.query_params.get('q')
#         print("search_query", search_query)
#         if search_query:
#             search_results = SearchQuerySet().models(Case).filter(content=search_query)
#             queryset = [result.object for result in search_results]
        
#         return queryset


# In case/views.py

from django.http import JsonResponse
from .search_index import search_cases

def search_view(request):
    
    query_str = request.GET.get('q', '')  # The 'q' parameter in the URL contains the query string
    print("query_str1", query_str)
    results = search_cases(query_str)  # Call the search function
    # print("results", results[0]["text"])
    return JsonResponse(results, safe=False)  # Return the results as a JSON response
