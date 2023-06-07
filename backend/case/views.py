from django.shortcuts import render

from rest_framework import viewsets
from .models import Case
from .serializers import CaseSerializer
from haystack.query import SearchQuerySet
from django.http.request import HttpRequest

from case.models import Case, Law
from django.core.paginator import Paginator

from haystack.forms import SearchForm
import xml.etree.ElementTree as ET

import time
import re

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

from django.http import JsonResponse, HttpResponse
from .search_index import search_cases, search_cases_new
from haystack.query import SearchQuerySet

import random

from .search_index import MAX_NUM

from django.conf import settings
import os


def upload_case_xml(request: HttpRequest):
    print(request)
    dir_name = os.path.dirname(settings.UPLOAD_PATH)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    if request.method == 'POST':
        xml_file = request.FILES['file'].read().decode('utf-8')
        print("finish upload", type(xml_file))
        with open(settings.UPLOAD_PATH, "w", encoding="utf-8") as save_f:
            save_f.write(xml_file)
            
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error"})

def get_related_cases_summary(case: Case, num_return = 5):
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



def related_cases_from_law(request: HttpRequest):
    t1 = time.time()
    law_id = request.GET.get('lid', '-1')
    
    try:
        law_id = int(law_id)
        law: Law = Law.objects.get(id = law_id)
        results = law.cases.all()
        total_results = len(results)
        # random.shuffle(results)
        results = results[:MAX_NUM]
        split_words = [law.name]       
        # print("total_num", total_results)
        paginator = Paginator(results, per_page=10)
        page = request.GET.get("page", default='1')
        page_obj_list = paginator.get_page(page).object_list

        result_list = []
        for obj in page_obj_list:
            # print("type", type(obj), obj.keys())
            result_obj = get_obj_summary(obj, law.name)
            result_list.append(result_obj)

        time_delta = time.time() - t1
        response_data = {
                "law_id": law.id,
                "law_name": law.name,
                "total_objects": total_results,
                "time": time_delta,
                "results": result_list,
                "code": 0,
                "split_words": split_words
            }
        jsonResponse = JsonResponse(response_data)  # Return the results as a JSON response
        # jsonResponse["Access-Control-Allow-Origin"] = "http:/127.0.0.1:3333"
        return jsonResponse

    except:
        return JsonResponse({
            "code": -1,
            "msg": f"law {law_id} doesn't exist!!"
        })

def get_keywords_from_text(content: str, max_num = 4):
    result_list = []
    COMMON_WORDS = [
        ["交通肇事","故意伤害","强奸","非法拘禁","抢劫","盗窃","诈骗","抢夺","职务侵占","敲诈勒索","妨害公务","聚众斗殴","寻衅滋事","走私","毒品","故意杀人","伤害"],
        ["一审","二审","再审","调解",'仲裁'],
        ["有限公司", "合同纠纷", "财产","违约","资产"],
        ["著作权","名誉","肖像","影视作品","传播"],
        ["借贷","股票","报酬","工资",'信用卡',"租赁"],
        ["无期徒刑", "死刑"]
    ]
    random.shuffle(COMMON_WORDS)
    for words in COMMON_WORDS:
        count = 0
        for word in words:
            if content.find(word) != -1:
                result_list.append(word)
                count += 1
            if count >= 2:
                break
        if len(result_list) >= max_num:
            break

    print("result_list", " ".join(result_list))
    return " ".join(result_list)
    # # print("get_keywords", content)
    # for re_pattern in RE_PATTERNS:
    #     match = re.match(re_pattern, content)
    #     print("re", re_pattern, match)
    #     if match:
    #         print("re_group", re_pattern, match)
    #         result_list.append(match.group())



def search_upload_xml():
    # Load the XML file
    try:
        tree = ET.parse(settings.UPLOAD_PATH)
        root = tree.getroot()
        print("root")
    except:
        with open(settings.UPLOAD_PATH, encoding='utf-8') as f:
            contents = f.readlines()
        content_str = ' '.join([i.strip() for i in contents])
        search_dict = dict()
        new_query = get_keywords_from_text(content_str, max_num=5)
        print("upload search_str", content_str)
        search_dict['q'] = new_query
        return search_cases_new(search_dict)
    
    # Extract the case_reason
    search_dict = dict()
    case_reason = None
    try:
        case_reason = root.find('.//AY').get('value'); assert len(case_reason) > 1
    except:
        try:
            case_reason = root.find(".//QSAY").get('value'); assert len(case_reason) > 1
        except:
            try:
                case_reason = root.find(".//QSZAY").get('value'); assert len(case_reason) > 1
            except:
                case_reason = None
    if case_reason:
        search_dict['case_reason'] = case_reason

    try:
        note_name= root.find('.//WSMC').get('value')
    except:
        note_name = None
    if note_name:
        search_dict['note_name'] = note_name

    print("upload_search_dict", search_dict)
    if len(search_dict) < 2:
        try: 
            text=root.find(".//QW").get("value")[:300]
            query = get_keywords_from_text(text, max_num=3)
            search_dict['q'] = query
        except:
            pass


    return search_cases_new(search_dict)
    
#     return JsonResponse({"status": "success", "case_reason": case_reason})
# else:
#     return JsonResponse({"status": "error"})

def search_view(request: HttpRequest):
    t1 = time.time()

    form = SearchForm(request.GET)
    try:
        cd = form.data
        
    except:
        response_data = {
            "code": -1,
            "data": {
                "msg": "view.search_view error!!"
            }
        }

    print("upload", cd.get('upload', ''))
    if cd.get('upload', '') == '1':
        results, split_words = search_upload_xml()
        query_str = '#' # split_words[0] if len(split_words) > 0 else "#"

    elif 'lid' in cd and cd['lid'].isnumeric():
        print("lid", cd['lid'])
        return related_cases_from_law(request)
    
    else:
        query_str = cd['q']  # The 'q' parameter in the URL contains the query string
        print("query_str1", query_str)
        # MAX_NUM = 500
        # results, split_words = search_cases(query_str) # [:MAX_NUM]
        results, split_words = search_cases_new(cd)

    total_results = len(results)
    print("total_num", total_results)
    # results = list(results)
    # random.shuffle(results)
    tt = time.time()
    results = results[:MAX_NUM]
    paginator = Paginator(results, per_page=10)
    page = request.GET.get("page", default='1')
    page_obj_list = paginator.get_page(page).object_list
    print("paginator_time", time.time() - tt)

    result_list = []
    for obj in page_obj_list:
        # print("type", type(obj), obj.keys())
        result_obj = get_obj_summary(obj, query_str)
        result_list.append(result_obj)

    time_delta = time.time() - t1
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
