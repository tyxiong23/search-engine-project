import xml.etree.ElementTree as ET
import os
import django
from case.models import Case
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
# from whoosh.analysis import CJKAnalyzer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'judicature_search.settings')
django.setup()

def import_cases_from_xml(file_path, index_writer):
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

    case = Case(id=id, qw_value=qw_value, ws_value=ws_value, jbfy_value=jbfy_value, 
                xzqh_p_value=xzqh_p_value, xzqh_c_value=xzqh_c_value, land_value=land_value)
    case.save()

    index_writer.add_document(
        id=str(case.id),
        qw_value=qw_value,
        ws_value=ws_value,
        jbfy_value=jbfy_value,
        xzqh_p_value=xzqh_p_value,
        xzqh_c_value=xzqh_c_value,
        land_value=land_value
    )

from jieba.analyse import ChineseAnalyzer
def import_cases_from_xml_directory(directory_path):

    schema = Schema(
        id=ID(stored=True, unique=True),
        qw_value=TEXT(analyzer=ChineseAnalyzer()),
        ws_value=TEXT(analyzer=ChineseAnalyzer()),
        jbfy_value=TEXT(analyzer=ChineseAnalyzer()),
        xzqh_p_value=TEXT(analyzer=ChineseAnalyzer()),
        xzqh_c_value=TEXT(analyzer=ChineseAnalyzer()),
        land_value=TEXT(analyzer=ChineseAnalyzer())
    )

    index_path = os.path.join(directory_path, 'whoosh_index')
    if not os.path.exists(index_path):
        os.makedirs(index_path)
    index = create_in(index_path, schema)
    index_writer = index.writer()

    for filename in os.listdir(directory_path):
        if filename.endswith('.xml'):
            try:
                file_path = os.path.join(directory_path, filename)
                import_cases_from_xml(file_path, index_writer)
            except:
                continue

    # Commit the changes to the Whoosh index
    index_writer.commit()


import_cases_from_xml_directory(os.path.join(os.path.dirname(__file__), "data"))
