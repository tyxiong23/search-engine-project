from django.shortcuts import render

from rest_framework import viewsets
from .models import Case
from .serializers import CaseSerializer
from haystack.query import SearchQuerySet
from django.http.request import HttpRequest

from case.models import Case, Law
from django.core.paginator import Paginator

import time


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
from haystack.query import SearchQuerySet

import random



def get_related_cases_summary(case: Case, num_return = 10):
    t1 = time.time()
    related_objs1 = list(Case.objects.all().filter(case_reason = case.case_reason).exclude(id=case.id))
    t2 = time.time()
    related_objs2 = list(case.laws.all()[0].cases.all())
    t3 = time.time()

    # random.shuffle(related_objs1)
    # random.shuffle(related_objs2)
    print("reason_realted", len(related_objs1), "law_related", len(related_objs2), t2 - t1, t3 - t2)

    related_objs = related_objs1[:num_return] + related_objs2[:num_return]
    random.shuffle(related_objs)

    selected_idx_set = set([case.id]); selected_summaries = []
    for obj in related_objs:
        if not obj.id in selected_idx_set:
            selected_idx_set.add(obj.id)
            selected_summaries.append(get_obj_summary(obj))
        if len(selected_summaries) >= num_return:
            break

    t4 = time.time()
    print(t4 - t3)

    return selected_summaries


def get_detail_info(case: Case):
    laws = case.laws.all()
    result_laws = [
        {"id": tmp.id, "name": tmp.name} for tmp in laws
    ]
    related_cases = get_related_cases_summary(case)

    response_data = {
        "code": 0,
        "data": dict({
            "id": case.id,
            "qw_value": case.qw_value,
            "head": case.head,
            "related_people": case.related_people,
            "judicial_record": case.judicial_record,
            "basic_info": case.basic_info,
            "judgement_process": case.judgement_process,
            "result": case.result,
            "tail": case.tail,

            "note_name": case.note_name,
            "case_reason": case.case_reason,
            "judge_prop": case.judge_prop,
            "court": case.court,
            "year": case.year,
            "laws": result_laws,
            "related_cases": related_cases
        })
        
    }

    return response_data


def get_obj_summary(obj, query_str = None):
    def summary_str(in_str: str, query_str = None):
        MAX_LEN = 100
        if query_str:
            index = in_str.find(query_str)
        else:
            index = MAX_LEN // 2
        prefix = ""; suffix = ""
        left = index - MAX_LEN // 2; right = index + MAX_LEN // 2
        if left >= 0:
            left = left + 3; prefix = "..."
        else:
            left = 0
        if right < len(in_str):
            right = right - 3; suffix = "..."
        else:
            right = len(in_str)

        return prefix + in_str[left: right] + suffix

    if isinstance(obj, dict):
        content: str = obj['text'][len(obj['head']):].strip()
        result_obj = {
            "id": obj['id'],
            "title": obj['head'], 
            "content": summary_str(content, query_str),
            "note_name": obj['note_name'],
            "year": obj['year'],
            "judge_prop": obj['judge_prop'],
            "case_reason": obj['case_reason']
        }
    else:
        print("type_obj -> summary", type(obj))
        content: str = obj.qw_value[len(obj.head):].strip()
        result_obj = {
            "id": obj.id,
            "title": obj.head, 
            "content": summary_str(content, query_str),
            "note_name": obj.note_name,
            "year": obj.year,
            "judge_prop": obj.judge_prop,
            "case_reason": obj.case_reason
        }

    return result_obj


def search_view(request: HttpRequest):
    t1 = time.time()
    
    query_str = request.GET.get('q', '')  # The 'q' parameter in the URL contains the query string
    print("query_str1", query_str)

    # MAX_NUM = 500
    results, split_words = search_cases(query_str) # [:MAX_NUM]
    total_results = len(results)
    print("total_num", total_results)
    
    
    time_delta = time.time() - t1
      # Call the search function
    # print("results", results[0]["text"])

    paginator = Paginator(results, per_page=10)
    page = request.GET.get("page", default='1')
    page_obj_list = paginator.get_page(page).object_list

    result_list = []
    for obj in page_obj_list:
        # print("type", type(obj), obj.keys())
        result_obj = get_obj_summary(obj, query_str)
        result_list.append(result_obj)

    response_data = {
        "total_objects": total_results,
        "time": time_delta,
        "results": result_list,
        "code": 0,
        "split_words": split_words
    }
    jsonResponse = JsonResponse(response_data)  # Return the results as a JSON response
    # jsonResponse["Access-Control-Allow-Origin"] = "http:/127.0.0.1:3333"
    print(jsonResponse)

    return jsonResponse


def case_detail_view(request: HttpRequest):

    case_id = request.GET.get("id", "-1")
    case_id = int(case_id)

    try:
        case = Case.objects.get(id = case_id)
        response_data = get_detail_info(case)
    except:
        response_data = {
            "code": -1,
            "data": {
                "msg": f"case id {case_id} not found!!"
            }
        }

    

    
    return JsonResponse(response_data)
