from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from case.models import Case

@registry.register_document
class CaseDocument(Document):
    qw_value = fields.TextField(attr='qw_value')
    land_value = fields.KeywordField(attr='land_value')

    class Index:
        name = 'case_index'  # Specify the name for the Elasticsearch index
