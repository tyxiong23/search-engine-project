import os


# from whoosh.fields import Schema, TEXT, ID, NUMERIC
# from whoosh.index import create_in
# from whoosh.analysis import CJKAnalyzer
import xml.etree.ElementTree as ET
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'judicature_search.settings')
import django
django.setup()

from case.models import Case, Law

def is_valid(in_str: str):
    return isinstance(in_str, str) and len(in_str) > 0



from glob import glob
from tqdm import tqdm

def law_match(in_str):
    LAW_PATTERN1 = '.*条'
    LAW_PATTERN2 = '《.*》'
    law = re.match(LAW_PATTERN1, in_str)
    if law:
        return law.group()
    law = re.match(LAW_PATTERN2, in_str)
    if law:
        return law.group()
    return None


def import_cases_from_xml(file_path) -> bool:
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except:
        print(f"[parser] {file_path} parser error!!")
        return False

    try:
        qw_value = root.find('QW').get('value'); assert is_valid(qw_value)
    except:
        return False
    
    try:
        head = root.find('.//WS').get('value')
    except:
        print(f"[Head] {file_path} no head!!")
        return False
    try:
        related_people = root.find('.//DSR').get('value')
    except:
        print(f"[related people] {file_path} no 当事人!!")
        return False
    
    
    try:
        judicial_record = root.find('.//SSJL').get('value')
        basic_info = root.find('.//AJJBQK').get('value')
        judgement_process = root.find('.//CPFXGC').get('value')
        result = root.find('.//PJJG').get('value')
        tail = root.find('.//WW').get('value')
    except:
        return False

    try:
        note_name= root.find('.//WSMC').get('value')
    except:
        print("[note_name] {file_path} no 文书名称!!")
        return False

    try:
        judge_prop = root.find('.//SPCX').get('value')
    except:
        try:
            judge_prop = root.find('.//ZXCX').get('value') # 没有审判程序，则找执行程序
        except:
            print("[judge_prop] {file_path} no judge_prop!!")
    
    try:
        court = root.find('.//JBFY').get('value')
        province = root.find('.//XZQH_P').get('value')
        year = root.find('.//LAND').get('value')
    except:
        print(f"[Error] {file_path} error!!")
        return False
    try:
        case_reason = root.find('.//AY').get('value'); assert is_valid(case_reason)
    except:
        try:
            case_reason = root.find(".//QSAY").get('value'); assert is_valid(case_reason)
        except:
            try:
                case_reason = root.find(".//QSZAY").get('value'); assert is_valid(case_reason)
            except:
                try:
                    case_reason = root.find(".//CUS_AY").get('value'); assert is_valid(case_reason)
                except:
                    print("cannot find case_reason!!!", file_path)
                    return False
    
    law_pieces = [i.get('value') for i in root.findall(".//FT") if law_match(i.get('value'))]

    if len(law_pieces) == 0:
        print(f"[Laws] {file_path} have no laws")
        return False
    
    for idx, field in enumerate([
        qw_value, head, 
        # related_people, judicial_record, basic_info, judgement_process, result, tail,
        # judge_prop,
        court, province
    ]):  
        if not is_valid(field):
            print(f"[inValid field] {file_path, idx, field}")
            return False
    
    if not year.isnumeric():
        print("[year] ", year, " not numeric!!!")
        return False
    year = int(year)

    law_matches = [law_match(i) for i in law_pieces if law_match(i)]
    
    try:
        case = Case.objects.create(
            qw_value = qw_value,
            head = head,
            related_people = related_people,
            judicial_record = judicial_record,
            basic_info = basic_info,
            judgement_process = judgement_process,
            result = result,
            tail = tail,
            note_name = note_name,
            judge_prop = judge_prop,
            court = court,
            case_reason = case_reason,
            province = province,
            year = year,
        )

        for matched_law in law_matches:
            law, if_create = Law.objects.get_or_create(name = matched_law)
            case.laws.add(law)
        # case.save()

    except:
        return False
    
    
    return True

if __name__ == "__main__":
    print("laws: ", Law.objects.all().__len__(), "cases: ", Case.objects.all().__len__())

    Case.objects.all().delete()
    Law.objects.all().delete()

    print("laws: ", Law.objects.all().__len__(), "cases: ", Case.objects.all().__len__())

    # exit(0)
    # data_dir = os.path.join(os.path.dirname(__file__), "case/data")
    data_dir = "../../Legal_data"
    xml_files = glob(data_dir + "/*.xml")
    count = 0; bar = tqdm(xml_files)
    for i, xml_f in enumerate(bar):
        bar.set_description(f"{os.path.basename(xml_f)} {count}/{i+1} cases imported")
        if_created = import_cases_from_xml(xml_f)
        if if_created:
            count += 1

    print("laws: ", Law.objects.all().__len__(), "cases: ", Case.objects.all())
        
        
# from jieba.analyse import ChineseAnalyzer
# def import_cases_from_xml_directory(directory_path):

# def import_cases_from_xml(file_path, index_writer):
#     tree = ET.parse(file_path)
#     root = tree.getroot()

#     file_name = os.path.splitext(os.path.basename(file_path))[0]
#     id = int(file_name)

#     qw_value = root.find('QW').get('value')
#     head = root.find('.//WS').get('value')
#     related_people = root.find('.//WS').get('value')
#     judicial_record = root.find('.//WS').get('value')
#     judgement_process = root.find('.//WS').get('value')
#     result = root.find('.//WS').get('value')
#     tail = root.find('.//WS').get('value')

#     note_name= root.find('.//WSMC').get('value')
#     judge_process = root.find('.//SPCX').get('value')

#     court = root.find('.//JBFY').get('value')
#     province = root.find('.//XZQH_P').get('value')
#     case_reason = root.find('.//XZQH_C').get('value')
#     year = root.find('.//LAND').get('value')

#     law_list = []
    

#     case = Case(id=id, qw_value=qw_value, ws_value=ws_value, jbfy_value=jbfy_value, 
#                 xzqh_p_value=xzqh_p_value, xzqh_c_value=xzqh_c_value, land_value=land_value)
#     case.save()

#     index_writer.add_document(
#         id=str(case.id),
#         qw_value=qw_value,
#         ws_value=ws_value,
#         jbfy_value=jbfy_value,
#         xzqh_p_value=xzqh_p_value,
#         xzqh_c_value=xzqh_c_value,
#         land_value=land_value
#     )






# from jieba.analyse import ChineseAnalyzer
# def import_cases_from_xml_directory(directory_path):

#     schema = Schema(
#         id=ID(stored=True, unique=True),
#         qw_value=TEXT(analyzer=ChineseAnalyzer()),
#         ws_value=TEXT(analyzer=ChineseAnalyzer()),
#         jbfy_value=TEXT(analyzer=ChineseAnalyzer()),
#         xzqh_p_value=TEXT(analyzer=ChineseAnalyzer()),
#         xzqh_c_value=TEXT(analyzer=ChineseAnalyzer()),
#         land_value=
#     )

#     index_path = os.path.join(directory_path, 'whoosh_index')
#     if not os.path.exists(index_path):
#         os.makedirs(index_path)
#     index = create_in(index_path, schema)
#     index_writer = index.writer()

#     for filename in os.listdir(directory_path):
#         if filename.endswith('.xml'):
#             try:
#                 file_path = os.path.join(directory_path, filename)
#                 import_cases_from_xml(file_path, index_writer)
#             except:
#                 continue

#     # Commit the changes to the Whoosh index
#     index_writer.commit()


# import_cases_from_xml_directory(os.path.join(os.path.dirname(__file__), "data"))
