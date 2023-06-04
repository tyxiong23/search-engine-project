# import xml.etree.ElementTree as ET
# from case.models import Case

# import os
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'judicature_search.settings')
# django.setup()


# def import_cases_from_xml(file_path):
#     tree = ET.parse(file_path)
#     root = tree.getroot()

#     for case_elem in root.findall('case'):
#         title = case_elem.find('title').text
#         content = case_elem.find('content').text
#         judge = case_elem.find('judge').text
#         law = case_elem.find('law').text
#         tags = [tag.text for tag in case_elem.findall('tags/tag')]

#         case = Case(title=title, content=content, judge=judge, law=law, tags=tags)
#         case.save()

# import_cases_from_xml('/Users/ava/judicature_search/case/data/18798.xml')

import xml.etree.ElementTree as ET
import os
import django
from case.models import Case

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'judicature_search.settings')
django.setup()

def import_cases_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    file_name = os.path.splitext(os.path.basename(file_path))[0]
    id = int(file_name)

    qw_value = root.find('QW').get('value')
    ws_value = root.find('.//WS').get('value')
    jbfy_value = root.find('.//JBFY').get('value')
    xzqh_p_value = root.find('.//XZQH_P').get('value')
    xzqh_c_value = root.find('.//XZQH_C').get('value')
    land_value = root.find('.//LAND').get('value')

    case = Case(id = id, qw_value=qw_value, ws_value=ws_value, jbfy_value=jbfy_value, xzqh_p_value=xzqh_p_value,xzqh_c_value = xzqh_c_value, land_value=land_value)
    case.save()

def import_cases_from_xml_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.xml'):
            try:
                file_path = os.path.join(directory_path, filename)
                import_cases_from_xml(file_path)
            except:
                continue


import_cases_from_xml_directory('case/data')


